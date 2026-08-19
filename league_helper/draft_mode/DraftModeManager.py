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
player_data_fetcher/espn_attribution.py, in memory, and THIS MODE never writes it to
disk.

That last sentence is scoped to this mode ON PURPOSE, because the unscoped version of
it -- "ESPN-derived ownership is never written to disk" -- is a claim about the whole
PROCESS and it is false without the restore below. PlayerManager is a single instance
shared by every mode, so the reconciliation writes drafted_by across the pool that
Modify Player Data, Trade Simulator and Starter Helper also hold, and Modify Player
Data's update_players_file() persists whatever that pool says. The mode that dirties
the shared state is therefore the mode that restores it: every exit from the cockpit
runs a FORCED PlayerManager.reload_player_data(force=True), because the ordinary
menu-loop reload short-circuits on unchanged file mtimes and this mode deliberately
changes none. See _restore_shared_player_state.

CREDENTIALS: this mode calls load_espn_env() on entry, before its own pre-flight reads
the environment. Nothing else on the League Helper path does, so without it the
repository-root .env -- the place this mode's own setup copy sends the operator -- was
never read and Draft Mode was unreachable on the project's documented credential route.

Author: Kai Mizuno
"""

import time
from datetime import datetime
from typing import Dict, List, NamedTuple, Optional, Tuple

import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.draft_geometry import DraftGeometry, read_geometry
from player_data_fetcher.espn_attribution import reconcile_espn_attribution_or_raise
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
# TD1 binding #1: league_helper/ names the D18.4 seam and NOTHING below it. The two
# credential helpers are imported from the seam's re-export rather than from
# espn_credentials directly for exactly the reason ESPNAPIError already is -- naming
# espn_credentials here is a TD1 breach, not an implementation choice.
from player_data_fetcher.espn_league_snapshot_seam import (
    ESPNAPIError,
    get_league_snapshot_sync,
    load_espn_env,
    missing_espn_credentials,
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

# NOT a failure block, and deliberately not worded as one. ESPN is the source of truth
# for WHAT WAS DRAFTED; MAX_POSITIONS in data/configs/league_config.json is a LOCAL
# lineup model, and a real ESPN draft is constrained by ESPN's roster settings, not by
# that file. So an ESPN roster the local slot ladder cannot lay out (a third QB, a
# 5RB/5WR shape) is a legitimate board state the local model does not describe -- never
# a reason to stop tracking a live draft. The cockpit keeps polling: ownership, recent
# picks, board context and recommendations are all still correct, and only the local
# slot VIEW is degraded.
ROSTER_OVERFLOW_HEADLINE = (
    "Note: your ESPN roster does not fit the local lineup slots"
)
ROSTER_OVERFLOW_ACTION = (
    "The cockpit is STILL RUNNING and the board above is accurate -- only the local "
    "'Current Roster by Draft Round' view is degraded, and it now shows the last "
    "layout that fit. ESPN's roster settings, not this app, decide what you may draft; "
    "MAX_POSITIONS in data/configs/league_config.json is only the local lineup model. "
    "Widen MAX_POSITIONS there if you want the local view to follow your real roster. "
    "This notice is printed once per session, not once per poll."
)

OWNERSHIP_FAILURE_HEADLINE = "ESPN ownership reconciliation failed"
OWNERSHIP_FAILURE_ACTION = (
    "The snapshot names a drafted player or a team the local pool cannot resolve, so "
    "ownership was left untouched rather than partially applied. Re-run the player-data "
    "fetcher to refresh the local pool, then re-enter Draft Mode."
)

UNEXPECTED_FAILURE_HEADLINE = "Unexpected error in the draft cockpit"
UNEXPECTED_FAILURE_ACTION = (
    "The cockpit could not classify this, so it cannot know that polling again would "
    "help -- it is either a bug or an environment problem (credentials, network or "
    "configuration) below the fetch seam. Keep drafting in the ESPN app and report the "
    "error above."
)

# SETUP copy, deliberately worded and rendered apart from the four failure blocks above.
# A user who has never configured ESPN has nothing broken -- no feed failure, no corrupt
# board, no bug -- so the copy must not read like any of those.
#
# TWO SETUP CLASSES, TWO HOMES, AND THAT IS THE WHOLE REASON THEY ARE SEPARATE CONSTANTS.
# The IDENTITY keys live in the "parameters" block of data/configs/league_config.json;
# the CREDENTIALS live in the process environment or a local .env file and are NEVER
# written to that config file. Re-using the identity copy for a missing credential would
# send the operator to a file that must not contain it, so each class carries its own
# headline and its own action line, and a run missing both prints both action lines.
ESPN_CONFIG_HEADLINE = "DRAFT MODE UNAVAILABLE: ESPN league identity is not configured"
ESPN_CONFIG_ACTION = (
    "This is a SETUP step, not a draft failure -- nothing is wrong with your league, "
    "your player data or the ESPN service. Add the identity key(s) named above to the "
    "\"parameters\" block of data/configs/league_config.json, then choose Draft Mode "
    "again. ESPN_LEAGUE_ID is the leagueId from your league's URL, as a STRING (e.g. "
    "\"138260302\"); ESPN_TEAM_ID is your own team's id in that league, as a positive "
    "INTEGER (the teamId in your team's URL). Every other mode works without them."
)

ESPN_CREDENTIAL_HEADLINE = "DRAFT MODE UNAVAILABLE: ESPN credentials are not configured"
ESPN_CREDENTIAL_ACTION = (
    "This is a SETUP step, not a draft failure -- nothing is wrong with your league, "
    "your player data or the ESPN service. Set the credential(s) named above in your "
    "PROCESS ENVIRONMENT or in a local .env file at the repository root, then choose "
    "Draft Mode again. They do NOT belong in data/configs/league_config.json -- that "
    "file never holds a credential. espn_s2 and SWID are the two cookies from a browser "
    "session signed in to ESPN (SWID includes its surrounding braces). Every other mode "
    "works without them."
)

ESPN_IDENTITY_AND_CREDENTIAL_HEADLINE = (
    "DRAFT MODE UNAVAILABLE: ESPN league identity and credentials are not configured"
)


class ESPNSetupProblem(NamedTuple):
    """One pre-flight verdict: what is unconfigured, and where to configure it.

    The action lines are a TUPLE rather than one string because identity and
    credentials have different homes (see the setup copy above): a run missing both
    must be told about both files in one pass, not sent round the loop twice.

    Attributes:
        detail: Every offending key, one line, names only -- never a value.
        headline: The headline matching WHICH classes are unconfigured.
        actions: One action line per unconfigured class, in identity-then-credential
            order to match `detail`.
    """

    detail: str
    headline: str
    actions: Tuple[str, ...]


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

        # Latch for the once-per-session roster-overflow notice, declared here for the
        # same reason _rendered_pick_ids is: _report_roster_overflow is reachable from a
        # directly-driven poll, so it must never AttributeError on a freshly built
        # manager. _run_cockpit_session keeps its own reset, which is what makes a
        # RE-entered session report the condition again.
        self._roster_overflow_reported: bool = False


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

        # .ENV BEFORE THE PRE-FLIGHT, and that ORDER is the whole point. Nothing else on
        # the run_league_helper.py -> LeagueHelperManager -> Draft Mode path calls
        # load_espn_env(): its only other production caller is the corpus generator, so
        # before this line the League Helper process NEVER saw a .env file. Both the
        # pre-flight below and get_espn_credentials() deep under the fetch seam read
        # os.environ and nothing else, so an operator whose espn_s2/SWID live in the
        # repository-root .env -- the place this mode's own ESPN_CREDENTIAL_ACTION tells
        # them to put it -- was told to do the thing they had already done, and Draft
        # Mode was unreachable on the project's documented credential route.
        #
        # override=False (the loader's default) is deliberate and load-bearing: a
        # credential exported into the process environment still wins over .env, so this
        # call can only ADD names that were absent, never replace an operator's explicit
        # override. It reads names and values into os.environ and returns nothing; no
        # credential value is read, printed or logged here.
        load_espn_env()

        # PRE-FLIGHT, before the cockpit banner and before _run_cockpit_session: an
        # unconfigured ESPN identity OR credential is a setup gap, not a draft failure,
        # and must return to the menu rather than crash the CLI.
        config_problem = self._espn_configuration_error()
        if config_problem is not None:
            self._render_espn_configuration_notice(config_problem)
            # NO state restore on this path, and that is a claim about reachability
            # rather than an omission: the pre-flight only reads config and the
            # environment, and the notice only prints. No poll ran, so
            # _reconcile_ownership_from_snapshot never touched the shared pool and there
            # is nothing to restore. The restore below is scoped to the session for
            # exactly that reason -- it costs a full re-read of six position files, so
            # it runs where state can actually have been dirtied.
            return

        print("\n" + "="*50)
        print("DRAFT MODE - LIVE COCKPIT")
        print("="*50)
        print(f"Polling ESPN every {POLL_INTERVAL_SECONDS}s. Draft in the ESPN app; "
              f"press Ctrl+C to stop.")

        self.logger.debug(f"Displaying roster for user ({self.player_manager.get_roster_len()}/{self.config.max_players} players)")
        self._display_roster_by_draft_rounds()

        try:
            self._run_cockpit_session()
        finally:
            # EVERY exit path, which is why this is a finally and not a trailing call:
            # a completed draft, any of the four terminal failure arms, and an exception
            # unwinding through here (EOFError, KeyboardInterrupt) all leave the shared
            # pool holding ESPN-derived ownership. See _restore_shared_player_state.
            self._restore_shared_player_state()

    def _restore_shared_player_state(self) -> None:
        """Hand the shared player pool back to disk state on the way out of the cockpit.

        THE MODE THAT DIRTIED THE SHARED STATE IS THE MODE THAT RESTORES IT.
        `self.player_manager` is a single instance shared by every mode
        (LeagueHelperManager.py:87,90,93), and
        `_reconcile_ownership_from_snapshot` writes `drafted_by` on EVERY player in it.
        Before the cutover the menu loop's own `reload_player_data()`
        (LeagueHelperManager.py:118) undid that on the way back, because the old mode
        wrote the position files and so changed their mtimes. This mode deliberately
        writes nothing, the mtimes therefore do not change, and that reload
        SHORT-CIRCUITS (PlayerManager.py:489-491) -- so ESPN-derived ownership survived
        in memory until the next `update_players_file()` (Modify Player Data) flushed it
        over the user's locally-recorded picks. That is silent data loss of exactly the
        state the app exists to track, and it is why this call passes `force=True`.

        `force=True` bypasses ONLY the mtime optimization, and only for this caller: the
        parameter defaults to False, so the menu loop and the Trade Simulator keep the
        optimization untouched.

        `reload_player_data` handles its own exceptions and returns None, so this cannot
        raise out of the `finally` that calls it and mask the session's own outcome.

        Args:
            None.

        Returns:
            None.
        """
        self.logger.debug(
            "Cockpit exiting - forcing a reload so ESPN-derived in-memory ownership "
            "cannot outlive the mode that wrote it"
        )
        self.player_manager.reload_player_data(force=True)

    def _espn_configuration_error(self) -> Optional[ESPNSetupProblem]:
        """Return why the ESPN setup is unusable, or None when the cockpit can be entered.

        Checks BOTH classes the cockpit needs, because both are read before a single
        pick can be rendered and either one missing crashes the mode without this gate:

        - IDENTITY (ESPN_LEAGUE_ID / ESPN_TEAM_ID), read from the league config file.
        - CREDENTIALS (espn_s2 / SWID), read from the process environment by
          `missing_espn_credentials()` -- the same read, with the same blank rule, that
          `get_espn_credentials()` performs deep inside the fetch, so this pre-flight
          cannot disagree with it. A repository-root .env reaches that environment
          because `start_interactive_mode` calls `load_espn_env()` FIRST; this method
          does not load it itself, so a caller driving the pre-flight directly sees the
          process environment alone. Without this half a credential-less
          run raised ConfigurationError from espn_credentials.py INSIDE the poll and
          killed the CLI at exit 1 (D18.5 user test plan scenario 7) -- precisely the
          failure mode this notice exists to eliminate, reached through the adjacent
          door.

        Credential VALUES are never read here, only their presence, so no value can
        reach the notice, the log or a stack frame.

        Args:
            None.

        Returns:
            None when the whole setup is usable; otherwise an ESPNSetupProblem naming
            EVERY offending key across both classes, so a user with neither configured
            is not sent round the loop twice.
        """
        identity_problems: List[str] = []

        league_id = self.config.espn_league_id.strip()
        if not league_id:
            identity_problems.append("ESPN_LEAGUE_ID is not set")
        elif not league_id.isdigit():
            identity_problems.append(
                f"ESPN_LEAGUE_ID is not a league number: {self.config.espn_league_id!r}"
            )

        if self.config.espn_team_id <= 0:
            identity_problems.append(
                f"ESPN_TEAM_ID is not a team id: {self.config.espn_team_id!r}"
            )

        credential_problems: List[str] = [
            f"{name} is not set" for name in missing_espn_credentials()
        ]

        if not identity_problems and not credential_problems:
            return None

        if identity_problems and credential_problems:
            headline = ESPN_IDENTITY_AND_CREDENTIAL_HEADLINE
            actions = (ESPN_CONFIG_ACTION, ESPN_CREDENTIAL_ACTION)
        elif identity_problems:
            headline = ESPN_CONFIG_HEADLINE
            actions = (ESPN_CONFIG_ACTION,)
        else:
            headline = ESPN_CREDENTIAL_HEADLINE
            actions = (ESPN_CREDENTIAL_ACTION,)

        return ESPNSetupProblem(
            detail="; ".join(identity_problems + credential_problems),
            headline=headline,
            actions=actions,
        )

    def _render_espn_configuration_notice(self, problem: ESPNSetupProblem) -> None:
        """Tell the operator this is a SETUP gap, distinguishably from a cockpit failure.

        Args:
            problem: The pre-flight verdict from _espn_configuration_error -- its detail,
                its matching headline, and one action line per unconfigured class.
        """
        print("\n" + "-" * 50)
        print(problem.headline)
        print(f"  {problem.detail}")
        for action in problem.actions:
            print(f"  {action}")
        print("-" * 50)
        self.logger.warning(
            f"Draft Mode not entered - ESPN configuration incomplete: {problem.detail}"
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
        self._roster_overflow_reported: bool = False

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
        except EOFError:
            # ABOVE the broad arm below, and that ORDER is the whole point: EOFError is
            # an Exception subclass, so a broad arm placed first would swallow it and
            # silently take ownership of a contract this mode deliberately does not own.
            # Nothing on this path reads stdin, so an EOFError here can only have
            # ARRIVED from below; LeagueHelperManager.main() remains the sole owner of
            # the notice and the exit status (LeagueHelperManager.py:240), so it
            # propagates untouched.
            raise
        except Exception as error:
            # THE FETCH PATH'S SAFETY NET, and it is not decorative. This half of the
            # poll talks to the network, the filesystem and the credential store, which
            # is the widest exposure to unexpected exception types in the whole mode --
            # yet before D18.5's polish it was the only half guarded by specific types
            # alone, while the narrower render half already had a broad net. A missing
            # credential proved it: ConfigurationError, raised by get_espn_credentials()
            # under the seam, escaped every arm and killed the CLI mid-draft at exit 1
            # (user test plan scenario 7). A DNS failure or an asyncio error would have
            # done the same. The pre-flight now catches the credential case with a much
            # better message, so what reaches here is genuinely unexpected -- rendered
            # loudly and TERMINAL rather than looped, on the same reasoning as the
            # render arm: an unclassifiable fetch error repeats every poll.
            # LAST, after the specific arms, so ESPNAPIError and ValueError keep their
            # tailored headlines. KeyboardInterrupt is not an Exception subclass and is
            # deliberately NOT caught.
            self._render_cockpit_failure(UNEXPECTED_FAILURE_HEADLINE, error, UNEXPECTED_FAILURE_ACTION)
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
            # one either: nothing BELOW this line reads stdin, and every call that could
            # relay one from further down -- the fetch -- is in the try above, whose own
            # EOFError arm re-raises.
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

        if self._rendered_pick_ids is not None and not pick_ids >= self._rendered_pick_ids:
            # Out-of-order arrival: NOT A SUPERSET of what was already rendered -- i.e.
            # this poll has LOST at least one pick we have already shown. Skipped
            # entirely, because reconciling it would walk ownership backwards -- exactly
            # what the idempotence criterion forbids.
            #
            # NON-SUPERSET, not proper-subset, and the difference is a real hole rather
            # than a stylistic one. A proper-subset test ({1,2} < {1,2,3}) misses the
            # DIVERGENT arrival -- rendered {1,2,3} against an incoming {1,2,4}, which is
            # neither a subset nor equal. That fell through to the TOTAL reconciliation
            # below, which reset pick 3's player to free agent, and line 525 then latched
            # the reduced set as the new baseline so the board could not self-correct.
            # Nothing in this repository documents any monotonicity property of
            # draftDetail.picks -- the codebase's whole posture toward this feed is that
            # it is untrusted (hence the geometry reader's parity guard, hence
            # complete-state reconciliation over delta bookkeeping) -- so the guard is
            # written to the criterion's unconditional wording rather than to an
            # undocumented ordering assumption. `not (a >= b)` subsumes the proper-subset
            # case exactly and adds the divergent one.
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

        try:
            self.player_manager.load_team()
        except ValueError as error:
            # THE LOCAL SLOT LADDER LOST, AND THE DRAFT DID NOT. load_team() builds a
            # FantasyTeam from every player attributed to us, and
            # FantasyTeam._assign_player_to_slot (FantasyTeam.py:634) raises ValueError
            # when a position exceeds the local MAX_POSITIONS. The pre-cutover path
            # could not reach that state -- it drafted through
            # PlayerManager.draft_player() -> FantasyTeam.draft_player(), gated by
            # can_draft(), which RETURNS FALSE rather than raising. Reconciling from
            # ESPN bypasses that gate by design, because ESPN already decided what we
            # own. Uncaught, this ValueError reached _cockpit_poll's render broad arm
            # and TERMINATED the cockpit mid-draft under "either a bug or an environment
            # problem" -- none of which is true of a legitimate roster shape, and at the
            # exact moment the board is most valuable. Caught here instead: ownership is
            # already applied above and stands, and self.player_manager.team keeps its
            # last successful layout because the failing `self.team = FantasyTeam(...)`
            # never rebound it. ValueError ONLY -- anything else from load_team() is
            # still genuinely unexpected and still reaches the broad arm.
            self._report_roster_overflow(error)

    def _report_roster_overflow(self, error: ValueError) -> None:
        """Tell the operator the local slot view degraded, ONCE, and keep polling.

        Latched rather than per-poll: reconciliation runs on every non-stale poll, so an
        unlatched notice would print every POLL_INTERVAL_SECONDS and destroy the fixed
        line height the board's column alignment depends on -- the same reason
        RECENT_PICK_WINDOW is a constant. The latch is declared in __init__ AND reset in
        _run_cockpit_session, mirroring _rendered_pick_ids' own two-site ownership: a
        directly-driven poll must not AttributeError, and a re-entered session must
        report the condition again rather than inherit the previous session's silence.

        Args:
            error: The ValueError raised by load_team(), reproduced verbatim so the
                operator sees which position overflowed and by how much.

        Returns:
            None.
        """
        if self._roster_overflow_reported:
            return
        self._roster_overflow_reported = True

        print("\n" + "-" * 50)
        print(ROSTER_OVERFLOW_HEADLINE)
        print(f"  {error}")
        print(f"  {ROSTER_OVERFLOW_ACTION}")
        print("-" * 50)
        self.logger.warning(
            f"ESPN roster exceeds local MAX_POSITIONS - local slot view degraded, "
            f"cockpit continuing: {error}"
        )

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
            # TRUNCATE as well as pad. `:24s` alone is a MINIMUM width, so a name longer
            # than 24 characters pushes the `->` column right and breaks the alignment
            # this fixed-height window exists to preserve. Slicing first makes the field
            # exactly 24 wide for every name.
            print(f"Pick {pick.overallPickNumber:3d}: {name[:24]:24s} -> {team}")

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

