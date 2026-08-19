"""
Draft Mode Manager

Manages Draft Mode: the live draft cockpit. Once entered, the mode is a
LONG-RUNNING, NON-INTERACTIVE session that polls ESPN for the real draft board and
re-renders roster, board context and recommendations until the draft ends, the
operator interrupts, or an unrecoverable feed/auth error is surfaced.

Key features:
- Polls the real ESPN draft board every POLL_INTERVAL_SECONDS through the
  player_data_fetcher seam -- the League Helper's only sanctioned route to the
  network (ticket D18 TD1)
- Reads the board's geometry (current round, overall pick, snake direction,
  picks-until-our-next-turn) from the validated snapshot via the pure reader in
  league_helper/util/draft_geometry.py
- Feeds picks-until-our-next-turn into the survival estimate (scoring Step 15), so
  recommendations account for who will still be available at our next turn
- Reconciles COMPLETE pick state every poll rather than applying deltas, so a
  repeated, duplicated or out-of-order poll cannot corrupt the board
- Position-aware draft strategy (follows DRAFT_ORDER config)
- Roster display by draft rounds

ESPN IS THE SOLE WRITER OF DRAFT TRUTH HERE. This mode drafts nothing locally: it
has no player-choice prompt, calls neither PlayerManager.draft_player() nor
update_players_file(), and offers no per-pick return to the main menu. Our own picks
are made in the ESPN app exactly like every opponent's and arrive back through the
same poll. Ownership reaches the local pool only through the reconciliation in
player_data_fetcher/espn_attribution.py, in memory, and is never written to disk.

Author: Kai Mizuno
"""

import time
from datetime import datetime
from typing import Dict, List, Optional

import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.draft_geometry import DraftGeometry, read_geometry
from player_data_fetcher.espn_attribution import reconcile_espn_attribution_or_raise
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from player_data_fetcher.espn_league_snapshot_seam import (
    ESPNAPIError,
    get_league_snapshot_sync,
)
from player_data_fetcher.player_data_models import PlayerDataValidationError
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer

# Poll cadence. Comfortably inside the league's observed timePerSelection of 90s, with
# margin on both the "materially above ~10s risks lagging a full pick" edge and on ESPN
# rate-limit exposure across a multi-hour draft.
POLL_INTERVAL_SECONDS = 15

# Recent-pick window. FIXED, deliberately: a constant recent-pick count keeps each
# re-render's total line height identical poll to poll, which is what the board's
# column alignment depends on. A "last full round" window would vary the height.
RECENT_PICK_WINDOW = 5

ESPN_FAILURE_HEADLINE = "ESPN feed or authentication failure"
ESPN_FAILURE_ACTION = (
    "The fetch layer already exhausted its own retries before raising, so this will not "
    "clear by waiting. Check espn_s2/SWID in .env and your network, then re-enter Draft "
    "Mode. Keep drafting in the ESPN app meanwhile -- your picks are safe there."
)

GEOMETRY_FAILURE_HEADLINE = "Draft geometry could not be read from the ESPN snapshot"
GEOMETRY_FAILURE_ACTION = (
    "If a draft PICK TRADE was just made in your league, this is the known traded-pick "
    "limitation, not corrupt data: a traded pick makes a team select outside its slot, so "
    "the served order matches neither pickOrder nor its reverse and the corruption guard "
    "fires on a legitimate state. Otherwise check ESPN_TEAM_ID / ESPN_LEAGUE_ID in "
    "data/configs/league_config.json. Either way the cockpit cannot track the board -- "
    "use the ESPN app's own draft board for the rest of this draft."
)

OWNERSHIP_FAILURE_HEADLINE = "ESPN ownership reconciliation failed"
OWNERSHIP_FAILURE_ACTION = (
    "The snapshot names a drafted player or a team the local pool cannot resolve, so "
    "ownership was left untouched rather than partially applied. Re-run the player-data "
    "fetcher to refresh the local pool, then re-enter Draft Mode."
)

UNEXPECTED_FAILURE_HEADLINE = "Unexpected error in the draft cockpit"
UNEXPECTED_FAILURE_ACTION = (
    "This is a bug, not a recoverable draft state. Keep drafting in the ESPN app and "
    "report the error above."
)

# SETUP copy, deliberately worded and rendered apart from the four failure blocks above.
# A user who has never configured ESPN has nothing broken -- no feed failure, no corrupt
# board, no bug -- so the copy must not read like any of those.
ESPN_CONFIG_HEADLINE = "DRAFT MODE UNAVAILABLE: ESPN league identity is not configured"
ESPN_CONFIG_ACTION = (
    "This is a SETUP step, not a draft failure -- nothing is wrong with your league, "
    "your player data or the ESPN service. Add the key(s) named above to the "
    "\"parameters\" block of data/configs/league_config.json, then choose Draft Mode "
    "again. ESPN_LEAGUE_ID is the leagueId from your league's URL, as a STRING (e.g. "
    "\"138260302\"); ESPN_TEAM_ID is your own team's id in that league, as a positive "
    "INTEGER (the teamId in your team's URL). Every other mode works without them."
)


class DraftModeManager:
    """
    Manages Draft Mode (the draft assistant).

    This mode helps users build their fantasy roster by providing intelligent
    player recommendations that consider:
    - Current draft round and position strategy (PRIMARY/SECONDARY bonuses)
    - Team composition and positional needs
    - Player scores calculated via the 9-step algorithm
    - Availability and roster limits

    Attributes:
        config (ConfigManager): Configuration manager with draft strategy
        logger: Logger instance for tracking draft events
        player_manager (PlayerManager): Manages player data and scoring
        team_data_manager (TeamDataManager): Provides team rankings

    Example workflow:
        1. User enters Draft Mode from the main menu -- the last interactive step
        2. System shows current roster organized by draft rounds
        3. System polls ESPN, reads the board geometry, reconciles complete pick
           state, and renders board context plus recommendations
        4. On an unchanged poll it prints a one-line heartbeat instead of
           re-rendering; on a poll where a pick landed it prints a distinct two-line
           pick marker and then re-renders in full
        5. Steps 3-4 repeat every POLL_INTERVAL_SECONDS until the draft completes,
           the operator presses Ctrl+C, or a feed/auth failure is surfaced
        6. The user drafts in the ESPN app throughout; the helper never drafts
    """


    def __init__(self, config: ConfigManager, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Initialize Draft Mode Manager.

        Args:
            config (ConfigManager): Configuration with draft order strategy
            player_manager (PlayerManager): Manages players and scoring
            team_data_manager (TeamDataManager): Provides team data
        """
        self.config = config
        self.logger = get_logger()
        self.set_managers(player_manager, team_data_manager)

        # The set of completed overall pick numbers already rendered -- the ONLY state
        # carried between polls. Declared at construction, not merely reset when a
        # session starts, because the poll path reads it and _cockpit_poll is callable
        # independently of _run_cockpit_session: a freshly built manager whose poll is
        # driven directly must classify its first poll as "first render", never raise
        # AttributeError. _run_cockpit_session keeps its own reset, which is what makes a
        # RE-entered session start from a clean board rather than from the previous
        # session's last render.
        self._rendered_pick_ids: Optional[frozenset] = None


    def set_managers(self, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Update manager references with new instances.

        Called at the start of interactive mode to ensure we have the latest
        data after potentially returning from other modes.

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager


    def start_interactive_mode(self, player_manager, team_data_manager):
        """
        Enter Draft Mode: the live draft cockpit.

        The LAST interactive step is the main-menu selection that reached this method.
        From here the mode is a long-running, non-interactive session: it polls ESPN
        every POLL_INTERVAL_SECONDS, reconciles complete pick state, and re-renders the
        board until the draft ends, the operator interrupts, or a feed/auth failure is
        surfaced. It never prompts for a player, never drafts locally and never writes
        the player file -- our own picks are made in the ESPN app and arrive back
        through the same poll that carries every opponent's.

        EOFError: there is deliberately NO EOFError clause anywhere below. The clause
        this method used to carry guarded a player-choice input() that no longer
        exists; it was retired WITH that call rather than relocated to a call site that
        is gone. Nothing in the session loop reads stdin, so a dead stdin cannot be
        observed here at all. LeagueHelperManager.main() remains the sole owner of the
        notice and the exit status (LeagueHelperManager.py:240) -- unchanged, since the
        old local clause only ever re-raised to it.

        KeyboardInterrupt: likewise not handled here. main()'s own handler
        (LeagueHelperManager.py:248, exit 130) already wraps this call stack including
        the time.sleep() poll wait, and KeyboardInterrupt is not an Exception subclass,
        so the broad arm in _cockpit_poll cannot swallow it.

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
        self.set_managers(player_manager, team_data_manager)
        self.logger.info("Entering Draft Mode")

        # PRE-FLIGHT, before the cockpit banner and before _run_cockpit_session: an
        # unconfigured ESPN identity is a setup gap, not a draft failure, and must return
        # to the menu rather than crash the CLI.
        config_problem = self._espn_configuration_error()
        if config_problem is not None:
            self._render_espn_configuration_notice(config_problem)
            return

        print("\n" + "="*50)
        print("DRAFT MODE - LIVE COCKPIT")
        print("="*50)
        print(f"Polling ESPN every {POLL_INTERVAL_SECONDS}s. Draft in the ESPN app; "
              f"press Ctrl+C to stop.")

        self.logger.debug(f"Displaying roster for user ({self.player_manager.get_roster_len()}/{self.config.max_players} players)")
        self._display_roster_by_draft_rounds()

        self._run_cockpit_session()

    def _espn_configuration_error(self) -> Optional[str]:
        """Return why the ESPN identity config is unusable, or None when it is usable.

        Args:
            None.

        Returns:
            None when both keys are usable; otherwise a one-line detail naming EVERY
            offending key, so a user with neither set is not sent round the loop twice.
        """
        problems: List[str] = []

        league_id = self.config.espn_league_id.strip()
        if not league_id:
            problems.append("ESPN_LEAGUE_ID is not set")
        elif not league_id.isdigit():
            problems.append(
                f"ESPN_LEAGUE_ID is not a league number: {self.config.espn_league_id!r}"
            )

        if self.config.espn_team_id <= 0:
            problems.append(
                f"ESPN_TEAM_ID is not a team id: {self.config.espn_team_id!r}"
            )

        return "; ".join(problems) if problems else None

    def _render_espn_configuration_notice(self, detail: str) -> None:
        """Tell the operator this is a SETUP gap, distinguishably from a cockpit failure.

        Args:
            detail: The offending key(s), exactly as _espn_configuration_error phrased them.
        """
        print("\n" + "-" * 50)
        print(ESPN_CONFIG_HEADLINE)
        print(f"  {detail}")
        print(f"  {ESPN_CONFIG_ACTION}")
        print("-" * 50)
        self.logger.warning(
            f"Draft Mode not entered - ESPN configuration incomplete: {detail}"
        )

    def _run_cockpit_session(self) -> None:
        """Run the poll loop until one of its three terminal conditions fires.

        The three are exactly the ones the unit's Lifecycle criterion names: the draft
        completes, the operator interrupts (handled by main(), so it simply unwinds
        through here), or an unrecoverable error is surfaced. There is no per-pick exit
        to the main menu.

        The league identity is resolved ONCE, before the loop. ConfigManager.
        espn_league_id is a str (ConfigManager.py:337) while the fetch seam requires an
        int, and doing the cast here rather than per poll keeps a malformed
        ESPN_LEAGUE_ID from raising a ValueError inside _cockpit_poll, where it would be
        misreported as a draft-geometry failure. start_interactive_mode's pre-flight
        check now rejects a blank or malformed id BEFORE this method is reached, so the
        cast is a second line of defence rather than the only one; it is kept because
        this method is independently callable and the hoisting reason above is unchanged.
        """
        league_id = int(self.config.espn_league_id)
        season = self.config.nfl_season
        our_team_id = self.config.espn_team_id

        self._rendered_pick_ids: Optional[frozenset] = None

        while True:
            if self._cockpit_poll(league_id, season, our_team_id):
                return
            time.sleep(POLL_INTERVAL_SECONDS)

    def _cockpit_poll(self, league_id: int, season: int, our_team_id: int) -> bool:
        """Fetch, read the geometry, and render one poll's outcome.

        Args:
            league_id: ESPN league id, already cast to int by the session.
            season: Season year; the seam requires it explicitly and has no default.
            our_team_id: The configured ESPN_TEAM_ID.

        Returns:
            True when the session must end (draft complete, or an unrecoverable failure
            that has already been rendered); False to keep polling.
        """
        try:
            snapshot = get_league_snapshot_sync(league_id, season)
            geometry = read_geometry(snapshot, our_team_id)
        except ESPNAPIError as error:
            # No second retry layer: the transport already exhausted tenacity's 3
            # attempts (excluding the failures that cannot succeed on retry) before the
            # seam raised. Re-attempting here would silently retry an already-exhausted
            # failure, which is the "quietly stops updating" anti-pattern.
            self._render_cockpit_failure(ESPN_FAILURE_HEADLINE, error, ESPN_FAILURE_ACTION)
            return True
        except ValueError as error:
            # ALL FOUR of read_geometry's ValueError arms land here: our team absent
            # from pickOrder, a duplicate pickOrder entry, the round-parity corruption
            # guard, and the empty-picks[] error inherited from
            # LeagueSnapshot.round_count. None can be resolved by polling again, so all
            # four are terminal. The parity arm also fires on a LEGITIMATE mid-draft
            # pick trade -- a known, accepted limitation of the geometry reader -- which
            # is why GEOMETRY_FAILURE_ACTION names that case first.
            self._render_cockpit_failure(GEOMETRY_FAILURE_HEADLINE, error, GEOMETRY_FAILURE_ACTION)
            return True

        try:
            return self._render_cockpit_poll(snapshot, geometry, our_team_id)
        except PlayerDataValidationError as error:
            self._render_cockpit_failure(OWNERSHIP_FAILURE_HEADLINE, error, OWNERSHIP_FAILURE_ACTION)
            return True
        except Exception as error:
            # Loud, not silent, and terminal rather than looping: an unexpected error in
            # the render/score path repeats every poll, so continuing would scroll the
            # same traceback forever. KeyboardInterrupt is not an Exception subclass and
            # is deliberately NOT caught here. No EOFError clause is needed above this
            # one either: nothing on this path reads stdin.
            self._render_cockpit_failure(UNEXPECTED_FAILURE_HEADLINE, error, UNEXPECTED_FAILURE_ACTION)
            return True

    def _render_cockpit_poll(self, snapshot: LeagueSnapshot, geometry: DraftGeometry,
                             our_team_id: int) -> bool:
        """Classify one poll against the last rendered state and render its outcome.

        Complete-state reconciliation, never delta bookkeeping: the ONLY state carried
        between polls is the set of completed overall pick numbers already rendered,
        used solely to classify this poll as unchanged, advanced or stale. Every
        rendered value is re-derived from this snapshot in full.

        Args:
            snapshot: The freshly fetched, already-validated snapshot.
            geometry: The geometry read from it.
            our_team_id: The configured ESPN_TEAM_ID.

        Returns:
            True when the draft is genuinely complete; False to keep polling.
        """
        completed_picks = [pick for pick in snapshot.draftDetail.picks if pick.playerId != -1]
        pick_ids = frozenset(pick.overallPickNumber for pick in completed_picks)

        if geometry.current_round is None:
            # ALL-SENTINEL. The geometry reader cannot tell "draft over" from "ESPN has
            # not served the current pick row yet" and does not try -- it has no
            # network. draftDetail.inProgress is the draft-LEVEL state gate that
            # separates them; it is never used as a per-pick completeness predicate,
            # which is the only use the snapshot model's docstring bars.
            if not snapshot.draftDetail.inProgress:
                self._render_draft_complete(snapshot, completed_picks)
                return True
            self._render_heartbeat(None, None, "waiting for ESPN to serve the current pick")
            return False

        if self._rendered_pick_ids is not None and pick_ids < self._rendered_pick_ids:
            # Out-of-order arrival: a PROPER subset of what was already rendered. Skipped
            # entirely, because reconciling it would walk ownership backwards -- exactly
            # what the idempotence criterion forbids.
            self._render_heartbeat(geometry.overall_pick_number,
                                   geometry.picks_until_our_next_turn,
                                   "stale poll ignored")
            return False

        self._reconcile_ownership_from_snapshot(snapshot, our_team_id)

        if pick_ids == self._rendered_pick_ids:
            self._render_heartbeat(geometry.overall_pick_number,
                                   geometry.picks_until_our_next_turn,
                                   "no change")
            return False

        if self._rendered_pick_ids is None:
            print(f"\n[{self._clock()}] LIVE BOARD - pick {geometry.overall_pick_number}")
        else:
            newest = max(completed_picks, key=lambda pick: pick.overallPickNumber)
            self._render_pick_landed(snapshot, newest, geometry.picks_until_our_next_turn)

        self._display_roster_by_draft_rounds()
        self._render_board_context(snapshot, completed_picks, geometry)

        if geometry.picks_until_our_next_turn is None:
            # Field-level sentinel: our own draft is done while the board runs on. Board
            # context keeps rendering; there is nothing left to recommend for us.
            print("\nYour draft is complete - no further recommendations.")
        else:
            print("\nTop draft recommendations based on the live board:")
            for i, p in enumerate(self.get_recommendations(geometry), start=1):
                print(f"{i}. {p}")

        self._rendered_pick_ids = pick_ids
        return False

    def _reconcile_ownership_from_snapshot(self, snapshot: LeagueSnapshot,
                                           our_team_id: int) -> None:
        """Re-derive every local player's ownership from the complete snapshot.

        Delegates the whole join to reconcile_espn_attribution_or_raise -- exact-
        playerId reconciliation plus our-team normalization, fail-closed on any
        unresolvable id and on the FANTASY_TEAM_NAME collision guard. The cockpit shares
        that single owner rather than forking a partial copy of its gating contract.

        TOTAL assignment, not a merge: every player's drafted_by is written on every
        call, so a player absent from the map is reset to the free-agent "". That is what
        makes a repeated poll a provable no-op and a mis-ordered board recoverable.

        Nothing is persisted. ESPN is the writer of draft truth; the local player file is
        refreshed by the fetcher, never by this mode.

        Args:
            snapshot: The freshly fetched, already-validated snapshot.
            our_team_id: The configured ESPN_TEAM_ID.

        Raises:
            PlayerDataValidationError: propagated unchanged from the shared owner.
        """
        players = self.player_manager.players
        attribution = reconcile_espn_attribution_or_raise(
            snapshot, players, our_team_id, self.logger
        )

        for player in players:
            player.drafted_by = attribution.get(str(player.id), "")

        self.player_manager.load_team()

    @staticmethod
    def _clock() -> str:
        """Local wall-clock HH:MM:SS for the cockpit's timestamped lines.

        Returns:
            The current local time as HH:MM:SS -- no date, no timezone.
        """
        return datetime.now().strftime("%H:%M:%S")

    def _render_heartbeat(self, overall_pick_number: Optional[int],
                          picks_until_our_next_turn: Optional[int],
                          marker: str) -> None:
        """Print the ONE-LINE unchanged-poll heartbeat.

        Appended below the last full render, never redrawn in place and with no terminal
        control codes: the scrollback doubles as the poll log, which control codes would
        corrupt.

        Both trailing clauses are omitted rather than printed as "None" when their value
        is absent -- picks_until_our_next_turn is None at the geometry reader's
        field-level sentinel (our own draft is done), and both are None before ESPN has
        served the current pick row.

        Args:
            overall_pick_number: The current pick's overall number, or None.
            picks_until_our_next_turn: Picks remaining before our turn, or None.
            marker: The state word, e.g. "no change".
        """
        line = f"[{self._clock()}] {marker}"
        if overall_pick_number is not None:
            line += f" - pick {overall_pick_number}"
            if picks_until_our_next_turn is not None:
                line += f", {picks_until_our_next_turn} until your turn"
        print(line)

    def _render_pick_landed(self, snapshot: LeagueSnapshot, pick,
                            picks_until_our_next_turn: Optional[int]) -> None:
        """Print the TWO-LINE marker for a poll on which a pick landed.

        Deliberately a different shape from the heartbeat so the operator can never
        mistake one for the other at a glance. The full board/roster/recommendations
        re-render follows immediately; this is the line that opens it.

        The second line is indented to align under "PICK": len("[HH:MM:SS] ") == 11. It
        is omitted entirely at the field-level sentinel.

        Args:
            snapshot: The snapshot the pick came from, for team-name resolution.
            pick: The completed DraftPick row with the highest overallPickNumber.
            picks_until_our_next_turn: Picks remaining before our turn, or None.
        """
        player_name = self._player_names_by_local_id().get(
            str(pick.playerId), f"player {pick.playerId}")
        team_name = self._team_names_by_id(snapshot).get(
            pick.teamId, f"team {pick.teamId}")
        print(f"\n[{self._clock()}] PICK {pick.overallPickNumber}: "
              f"{player_name} -> {team_name}")
        if picks_until_our_next_turn is not None:
            print(f"           {picks_until_our_next_turn} until your turn")

    def _player_names_by_local_id(self) -> Dict[str, str]:
        """Local playerId (as str) -> player name, for rendering ESPN pick rows.

        Keyed on str because FantasyPlayer.id is an int while ESPN's playerId is
        normalized to str at this project's single int->str boundary; str is the side
        both agree on.

        Returns:
            A fresh map over the currently loaded player pool.
        """
        return {str(player.id): player.name for player in self.player_manager.players}

    @staticmethod
    def _team_names_by_id(snapshot: LeagueSnapshot) -> Dict[int, str]:
        """ESPN teamId -> team name, read fresh from the snapshot on every render.

        Args:
            snapshot: The snapshot being rendered.

        Returns:
            A map from each team's ESPN id to its display name.
        """
        return {team.id: team.name for team in snapshot.teams}

    def _render_board_context(self, snapshot: LeagueSnapshot, completed_picks: List,
                              geometry: Optional[DraftGeometry]) -> None:
        """Render the live board: recent picks, who is on the clock, our countdown.

        The recent-pick window is FIXED at RECENT_PICK_WINDOW rows once that many picks
        exist, and shows the true count (never padded) when fewer do, so the block's
        height is constant through the body of the draft. That constancy is what the
        column alignment depends on.

        The countdown is geometry.picks_until_our_next_turn stated verbatim as a PICK
        COUNT. It is never converted to a duration: timePerSelection is an upper bound,
        not an observed average, so a derived time estimate could mislead materially
        during a live draft.

        Args:
            snapshot: The snapshot being rendered.
            completed_picks: Its completed pick rows (playerId != -1).
            geometry: The read geometry, or None at the draft-complete render, where
                there is no current pick and no next turn.
        """
        player_names = self._player_names_by_local_id()
        team_names = self._team_names_by_id(snapshot)

        print(f"\nRecent picks (last {RECENT_PICK_WINDOW}):")
        print("-" * 50)
        recent = sorted(completed_picks,
                        key=lambda pick: pick.overallPickNumber)[-RECENT_PICK_WINDOW:]
        if not recent:
            print("No picks made yet.")
        for pick in recent:
            name = player_names.get(str(pick.playerId), f"player {pick.playerId}")
            team = team_names.get(pick.teamId, f"team {pick.teamId}")
            print(f"Pick {pick.overallPickNumber:3d}: {name:24s} -> {team}")

        if geometry is None:
            return

        on_the_clock = next(
            (pick for pick in snapshot.draftDetail.picks
             if pick.overallPickNumber == geometry.overall_pick_number),
            None
        )
        clock_team = (team_names.get(on_the_clock.teamId, f"team {on_the_clock.teamId}")
                      if on_the_clock is not None else "unknown team")
        print(f"On the clock: pick {geometry.overall_pick_number} "
              f"(round {geometry.current_round}) - {clock_team}")
        if geometry.picks_until_our_next_turn is not None:
            print(f"{geometry.picks_until_our_next_turn} until your turn")

    def _render_cockpit_failure(self, headline: str, error: Exception, action: str) -> None:
        """Surface an unrecoverable cockpit failure LOUDLY and ACTIONABLY.

        A cockpit that quietly stops updating during a live draft is worse than one that
        stops, so this is deliberately hard to miss and always names what to do next --
        never only what went wrong.

        Args:
            headline: The failure class, one short line.
            error: The caught exception; its type and message are printed verbatim.
            action: What the operator should do now.
        """
        print("\n" + "!" * 50)
        print(f"DRAFT MODE STOPPED: {headline}")
        print(f"  {type(error).__name__}: {error}")
        print(f"  {action}")
        print("!" * 50)
        self.logger.error(
            f"Draft Mode cockpit halted in _cockpit_poll - {headline}: "
            f"{type(error).__name__}: {error}"
        )

    def _render_draft_complete(self, snapshot: LeagueSnapshot,
                               completed_picks: List) -> None:
        """Render the end-of-draft summary and let the session end normally.

        Reached only at the ALL-SENTINEL boundary with draftDetail.inProgress False --
        the disambiguation that separates a finished draft from a snapshot ESPN has not
        yet caught up on. Uses the same board-context surface as every other render, in
        its final state, plus the roster.

        Args:
            snapshot: The final snapshot.
            completed_picks: Its completed pick rows.
        """
        print("\n" + "=" * 50)
        print("DRAFT COMPLETE")
        print("=" * 50)
        self._render_board_context(snapshot, completed_picks, None)
        self._display_roster_by_draft_rounds()
        self.logger.info(
            f"Draft Mode cockpit exiting - draft complete "
            f"({len(completed_picks)} picks recorded)"
        )

    def get_recommendations(self, geometry: Optional[DraftGeometry] = None) -> List[ScoredPlayer]:
        """
        Generate top player recommendations for the current draft round.

        Uses the complete scoring algorithm plus draft round bonuses to rank all
        available players. Returns the top Constants.RECOMMENDATION_COUNT
        recommendations sorted by score.

        Args:
            geometry: The live board geometry, supplied by the cockpit poll loop. When
                present it drives BOTH the round used for the draft-order bonus AND the
                survival estimate's picks-until-our-next-turn input (scoring Step 15) --
                the join that makes the survival signal live. When absent (the
                roster-only path) the round falls back to _get_current_round()'s
                slot-fill scan and picks_until_next_turn is None, so Step 15 is skipped
                and scoring is byte-identical to before the cockpit cutover.

        Returns:
            List[ScoredPlayer]: Top recommended players (or fewer if less available)

        Scoring includes:
            - Step 1: Normalized fantasy points (base score)
            - Step 2: ADP multiplier (draft value adjustment)
            - Step 3: Player rating multiplier (expert consensus)
            - Step 4: Team quality multiplier (offensive/defensive ranks)
            - Step 5: Performance deviation (recent form)
            - Step 6: Matchup multiplier (weekly opponent strength)
            - Step 7: Draft order bonus (position-specific PRIMARY/SECONDARY bonuses)
            - Step 8: Bye week penalty (roster overlap conflicts)
            - Step 9: Injury penalty (health risk assessment)

        Note:
            Under point-in-time (e.g. week-1) projections, the positive-value player pool
            for a position can be exhausted before every roster slot for that position is
            filled (T42) — real early-season projections are sparser than season-end ones,
            and unconstrained opponent drafting can accelerate the exhaustion. When that
            happens and a roster slot is still open, this method falls back to roster-legal
            candidates with zero/negative projections rather than returning no
            recommendations, so the draft can still complete the roster.
        """
        if geometry is not None:
            current_round = geometry.current_round
            picks_until_next_turn = geometry.picks_until_our_next_turn
        else:
            current_round = self._get_current_round()
            picks_until_next_turn = None

        # Roster-full guard: _get_current_round() returns None when the roster is full
        # (15/15). Without this, `draft_round=current_round - 1` below would raise
        # TypeError if any draftable player still remained. Return no recommendations,
        # matching the existing "roster full / no pick available" semantics.
        if current_round is None:
            self.logger.debug("Roster is full (no current draft round) - no recommendations")
            return []

        available_players = self.player_manager.get_player_list(drafted_vals=[0], can_draft=True)

        if not available_players:
            # T42 fallback: no positive-value candidates remain for the open slot(s).
            # Relax the positive-points requirement so the roster can still be
            # completed with the best roster-legal (if zero-value) player available.
            available_players = self.player_manager.get_player_list(
                drafted_vals=[0], can_draft=True, require_positive_points=False
            )
            if available_players:
                self.logger.warning(
                    f"No positive-value draftable players available for round {current_round} - "
                    f"falling back to {len(available_players)} zero/negative-value roster-legal candidates"
                )

        self.logger.debug(f"Found {len(available_players)} draftable players for recommendations")

        scored_players : List[ScoredPlayer] = []

        for p in available_players:
            scored_player = self.player_manager.score_player(
                p,
                draft_round=current_round - 1,
                adp=True,
                player_rating=True,
                team_quality=False,
                performance=False,
                matchup=False,
                schedule=False,
                bye=True,
                injury=True,
                use_draft_normalization=True,
                nfl_team_penalty=True,
                picks_until_next_turn=picks_until_next_turn
            )
            scored_players.append(scored_player)

        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        self.logger.debug(f"Recommended next picks: {[p.player.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")

        return ranked_players[:Constants.RECOMMENDATION_COUNT]


    def _display_roster_by_draft_rounds(self):
        """
        Display current roster organized by draft round order.

        Shows all 15 draft rounds with either the player assigned to that round
        or [EMPTY SLOT] if the round is unfilled. Each round displays the ideal
        position from the DRAFT_ORDER config to guide draft strategy.

        The display helps users understand:
        - Which positions they've already filled
        - Which rounds are empty and need players
        - What positions should be prioritized next (based on ideal position)
        - Overall draft progress (X/15 players drafted)

        Returns:
            None: Prints roster display to console
        """
        print(f"\nCurrent Roster by Draft Round:")
        print("-" * 50)

        if not self.player_manager.team.roster:
            print("No players in roster yet.")
            return

        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, self.config.max_players + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            if round_num in round_assignments:
                player = round_assignments[round_num]
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {player.name} ({player.position}) - {player.fantasy_points:.1f} pts")
            else:
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): [EMPTY SLOT]")

        print(f"\nRoster Status: {self.player_manager.get_roster_len()}/{self.config.max_players} players drafted")


    def _match_players_to_rounds(self) -> Dict[int, FantasyPlayer]:
        """
        Match current roster players to draft round slots using optimal fit strategy.

        Uses a greedy algorithm to assign each roster player to their optimal draft round
        based on the DRAFT_ORDER config. Players are matched to rounds where their position
        perfectly matches the ideal position, ensuring they would have received PRIMARY
        bonuses if drafted in that round.

        The algorithm prioritizes:
        1. Perfect position matches (e.g., QB to QB-ideal rounds)
        2. FLEX conversion for RB/WR/DST (these can match FLEX-ideal rounds)
        3. Sequential processing to avoid conflicts

        Returns:
            Dict[int, FantasyPlayer]: Dictionary mapping round numbers (1-15) to FantasyPlayer objects.
                           Only rounds with assigned players are included as keys.
                           Empty rounds are omitted from the dictionary.

        Example:
            If roster has QB, RB, WR with 3 players total:
            {1: FantasyPlayer(RB1), 2: FantasyPlayer(WR1), 3: FantasyPlayer(QB1)}
        """
        round_assignments = {}

        available_players = list(self.player_manager.team.roster)

        for round_num in range(1, self.config.max_players + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            for player in available_players:
                if self._position_matches_ideal(player.position, ideal_position):
                    round_assignments[round_num] = player

                    available_players.remove(player)

                    break

        self.logger.debug(f"Matched {len(round_assignments)} players to draft rounds using optimal fit algorithm")
        return round_assignments

    def _position_matches_ideal(self, player_position: str, ideal_position: str) -> bool:
        """
        Check if a player's position can fill a round with the given ideal position.

        For FLEX-eligible positions (defined in config.flex_eligible_positions,
        typically RB and WR), players can match both their native position rounds
        AND FLEX-ideal rounds.

        For non-FLEX positions (QB, TE, K, DST), players must match exactly.

        Args:
            player_position: Player's actual position ("RB", "WR", "QB", etc.)
            ideal_position: Ideal position for the round from DRAFT_ORDER

        Returns:
            True if player can fill this round, False otherwise

        Examples:
            >>> self._position_matches_ideal("RB", "RB")     # True (native match)
            >>> self._position_matches_ideal("RB", "FLEX")   # True (FLEX-eligible)
            >>> self._position_matches_ideal("RB", "WR")     # False (different position)
            >>> self._position_matches_ideal("QB", "QB")     # True (exact match)
            >>> self._position_matches_ideal("QB", "FLEX")   # False (QB not FLEX-eligible)
        """
        if player_position in self.config.flex_eligible_positions:
            return player_position == ideal_position or ideal_position == "FLEX"
        else:
            return player_position == ideal_position

    def _get_current_round(self) -> int:
        """
        Calculate which draft round we're currently in based on roster composition.

        Returns:
            int: The current draft round number (1-15), or None if roster is full

        Logic:
            - Matches existing roster players to their optimal rounds
            - Returns the first round number that doesn't have a player assigned
            - If all 15 rounds have players, returns None (roster is full)

        Example:
            If roster has 5 players matched to rounds 1-5, returns 6
        """
        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, self.config.max_players + 1):
            if round_num not in round_assignments:
                self.logger.debug(f"Calculated current round: {round_num} (roster has {len(round_assignments)} players)")
                return round_num

        self.logger.debug("Roster is full (15/15 players) - no current round")

