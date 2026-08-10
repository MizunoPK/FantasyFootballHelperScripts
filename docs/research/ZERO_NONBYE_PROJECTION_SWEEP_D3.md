# Zero-Valued Non-Bye Projected Week-Slots — Sweep and Disposition (D3)

**Delivery ticket:** D3-bye-week-phantom-projections — unit D3.3
**Date:** 2026-08-10
**Scope:** characterization only. **This document fixes nothing.** No production code, no data file
and no behaviour is changed by the commit that adds it.

Every figure below names the tree it was measured against and the selection rule that produced it.
Every figure derived from the offline ESPN fixture rather than from the live player pool carries the
marker `[fixture-scoped]` in the table row or paragraph that states it, because those two populations
are different snapshots and the distinction is load-bearing — see §6.

---

## 1. Answer

The live player pool carries a large population of projected week-slots stored as `0.0` on weeks the
player's team **is scheduled to play**. The bye-week and schedule explanations are eliminated
outright (§4). Attributed offline against a tracked real ESPN payload, **zeroes of this kind arise by
at least three distinct mechanisms**, all three reachable through this exact code path:

- **Genuine ESPN zeroes occur in the payload.** ESPN really does return `appliedTotal: 0.0` on a
  current-season projection row for some weeks.
- **ESPN omissions occur in the payload.** For some weeks there is no `statSourceId == 1` row at all, and the
  exporter's `float(projected) if projected else 0.0` stores that absence as `0.0` — indistinguishable
  afterwards from a real zero.
- **A parse miss occurs, and it is this repository's own defect.** `_get_projected_points_array`
  applies **no `seasonId` filter** and breaks on its first match, so a **prior-season** row can occupy
  that first-match slot and a real current-season projection is discarded.

**Disposition: mixed — explicitly NOT "all genuine ESPN zeroes."** Both candidate mechanisms named at
design time are proven reachable through this exact code path against a real payload. Under the
ticket's filing rule that fires a follow-up on anything other than an all-genuine-zeroes result, a
follow-up ticket is filed: **D21-projection-zero-slot-parse-miss-and-omission-guard**.

**What this document does not establish.** It does not attribute any *individual live slot* to a
class, and it does not state how much of the live pool each class accounts for. That limit is a
consequence of the evidence source and is stated in full in §6; the exact command that would settle
it is recorded, unexecuted, in §7.

---

## 2. The population

### 2.1 Selection rule (the whole of what "zero-valued non-bye projected week" means)

- A **slot** is week `i+1` of a record's 17-element `projected_points` array.
- A slot is **excluded** when the record's own `bye_week` field equals that week.
- A record whose **entire** `projected_points` array is zero is excluded from the affected counts and
  reported as its own population.
- The remaining slots whose value is `0` are the population.
- A player's zero set is a **leading block** when its weeks form a contiguous run from week 1, and a
  **trailing block** when they form a contiguous run to week 17 — in both cases treating the player's
  own bye week as skipped rather than as breaking the run, and testing leading before trailing.
  Everything else is **scattered**.

### 2.2 Baselines

Two baselines are reported, not one. The sweep's per-slot result is unaffected by D3.2's bye-week
repair — bye slots are identified from each record's own `bye_week` field, not from whether the bye
has already been zeroed — but two **derived aggregates** are affected, and both are reported rather
than one silently replacing the other.

| Measure | pre-repair (`f1f187e0^`) | post-repair (`origin/main` = `ac3a8216`) |
|---|---|---|
| records | 799 | 799 |
| all-zero-projection players (reported separately, excluded from the two rows below) | 149 | 152 |
| players with at least one zero-valued non-bye projected week | 438 | 435 |
| zero-valued non-bye week-slots | 2,443 | 2,395 |
| top 100 by season projection — affected players / slots | 60 / 88 | 59 / 94 |
| records with a missing or out-of-range `bye_week` | 0 | 0 |
| phantom bye values remaining | 203 | 0 |

**Which column discharges what.** The pre-repair column reproduces the ticket-design sizing exactly
and is reported for that reason only. **The post-repair column is the live baseline**; every other
statement in this document, and everything downstream of this unit, quotes it.

**Why the two columns differ, arithmetic closed.** Three players (Travis Homer, Jack Westover, Jared
Wayne) had exactly one non-zero projected week and it was their bye. Zeroing the bye made their whole
array zero, so the selection rule moved them into the separately-reported all-zero population:
149 → 152 all-zero, 438 → 435 affected, and their 3 × 16 = 48 non-bye slots left the slot count,
2,443 → 2,395. Separately, 203 season totals dropped by their phantom bye value, so the ranking by
season projection re-ordered and the top-100 cut moved, 60 / 88 → 59 / 94. Neither column is a
correction of the other.

### 2.3 Shape of the population (post-repair, live pool only)

- 2,395 of the 10,352 non-bye projected week-slots carried by the 647 records the §2.1 rule admits
  are zero — **23.14%**. (Counting the 152 all-zero records in the denominator instead gives 2,395 of
  12,784 — 18.73%; that denominator does not match the numerator's population and is not the
  document's rate.)
- The 435 affected players carry between 1 and 15 zero slots each; 150 of them carry exactly one.
- Per affected player the zero set is **scattered** across the season for 351 players, a leading
  block from week 1 for 61, and a trailing block to week 17 for 23. The population is therefore not
  a season-truncation artifact.
- Affected players by position: QB 63, RB 99, WR 163, TE 88, K 22, **DST 0** — no defense record
  carries a single zero-valued non-bye slot.
- The population reaches the players that drive decisions: 59 of the top 100 by season projection,
  across 94 slots. Bijan Robinson (week 5), Jahmyr Gibbs (week 8), Jalen Hurts (week 9) and Puka
  Nacua (weeks 7 and 8) are all in it.

---

## 3. The two candidate mechanisms in the code

Both are read-only context here. Neither is changed by this unit.

### 3.1 The gap/zero collapse

`player_data_fetcher/player_data_exporter.py`, `_get_projected_points_array` (`:348`):

```python
for stat in espn_data.raw_stats:
    if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1:   # :368
        projected = stat.get('appliedTotal')
        break
projected_points.append(float(projected) if projected else 0.0)                 # :371
```

`projected` stays `None` when no row matched, and `float(x) if x else 0.0` maps `None`, `0.0` and a
missing field to the same stored `0.0`. Once written, the array **cannot** distinguish *"ESPN
returned nothing for this week"* from *"ESPN returned a real zero."*

### 3.2 The missing `seasonId` filter — an asymmetry, not a house convention

The scan at `:368` matches on `scoringPeriodId` and `statSourceId` only, and `break`s on the first
hit. Its sibling extractor in the same package does filter on season:

```python
# player_data_fetcher/espn_client.py, _extract_raw_espn_week_points (:530)
if season_id == self.settings.season and scoring_period == week:               # :587
```

And the list being scanned is the untouched multi-season list ESPN returned:

```python
# player_data_fetcher/espn_client.py:1728
raw_stats=player_info.get('stats', [])
```

So where a prior-season `statSourceId == 1` row for the same `scoringPeriodId` precedes the
current-season one, the prior-season row wins the first match. Where its `appliedTotal` is falsy, the
slot stores `0.0` while a correct current-season projection sits further down the same list.

---

## 4. The bye and schedule explanations are eliminated

Each of the 2,395 post-repair slots was joined to `data/season_schedule.csv` on `(team, week)`. That
file encodes a bye as an **empty `opponent`** — the same signal `_derive_bye_weeks_from_schedule`
(`player_data_fetcher/player_data_fetcher_main.py:180`) reads.

| Result | Count |
|---|---|
| slot falls on a week the team **has** a scheduled opponent | 2,395 |
| slot falls on a week with an empty `opponent` (a bye) | 0 |
| team/week pair absent from the schedule | 0 |

All 2,395 slots fall on weeks the player's team is scheduled to play. This is the full-population
result, not the top-100 subset the ticket design checked.

---

## 5. Offline attribution against the tracked ESPN fixture

### 5.1 Evidence source, and why this one

Attribution runs against `tests/fixtures/espn_api/season_projections_2025.json` — a tracked, 60 MB,
real `kona_player_info` response carrying the full raw `stats` list per player (`seasonId`,
`scoringPeriodId`, `statSourceId`, `statSplitTypeId`, `appliedTotal`). **No network call is made by
this unit.** The fixture ships in the repository, so every claim below is re-checkable by a reviewer
rather than taken on trust.

### 5.2 Mechanism class inventory

Each slot the exporter's rule renders `0.0` was classified by re-deriving the same scan and asking
what the first match actually was. The population is every zero slot in the fixture's exporter-derived
array. **Unlike §2.1's live population it applies neither the bye-week exclusion nor the all-zero-record
exclusion, so its total is not commensurable with §2's 2,395.** Both count columns below are therefore
`[fixture-scoped]`, and the second reports the same classification restricted to the sub-population
§2.1's all-zero-record rule would admit.

| Class | What it is | Which mechanism | Count `[fixture-scoped]` | §2.1-comparable `[fixture-scoped]` |
|---|---|---|---|---|
| **C1** | No `statSourceId == 1` row for that week in **any** season | ESPN omission, stored as `0.0` by the collapse (§3.1) | 959 `[fixture-scoped]` | 226 `[fixture-scoped]` |
| **C2a** | Current-season row present, `appliedTotal` exactly `0.0` | **Genuine ESPN zero** | 967 `[fixture-scoped]` | 566 `[fixture-scoped]` |
| **C2b** | Current-season row present, `appliedTotal` absent/`None` | Would be the collapse's other arm | 0 `[fixture-scoped]` | 0 `[fixture-scoped]` |
| **C3** | A prior-season row matched first; a **non-zero** current-season projection exists and is discarded | **Parse miss — this repo's defect** (§3.2) | 1,466 `[fixture-scoped]` | 1,233 `[fixture-scoped]` |
| **C4** | A prior-season row matched first; the current-season row is also zero | Parse miss, no value lost | 2,313 `[fixture-scoped]` | 1,421 `[fixture-scoped]` |
| **C5** | A prior-season row matched first; there is no current-season row at all | ESPN omission behind a shadowing row | 5,040 `[fixture-scoped]` | 1,060 `[fixture-scoped]` |
| | | **total zero slots classified** | 10,745 `[fixture-scoped]` | 4,506 `[fixture-scoped]` |

**The two columns differ sharply, and that difference is itself evidence.** 6,239 of the 10,745
classified slots — 58.1% — belong to the 367 fixture players whose whole exporter-derived array is
zero, exactly the class §2.1 removes from the live counts `[fixture-scoped]`. Applying that rule drops
C5 from 5,040 to 1,060 and C1 from 959 to 226, because a player with no current-season projection rows
at all is precisely the one that generates omission-class slots in every week. **All five occupied
classes remain occupied in the comparable column, and C3 — the class that loses real data — largely
survives (1,466 → 1,233), so the inventory claim and the mixed disposition below are unchanged by the
restriction.** Neither column is a live-pool magnitude; see §6.2.

**All five occupied classes occur.** Genuine ESPN zeroes are one class among several, not the whole
population. Both design-time candidates are therefore confirmed reachable through this exact code
path against a real payload: the collapse (C1) and the missing `seasonId` filter (C3, C4, C5).

**C3 is the class that loses data.** In C3 a correct current-season projection exists in the payload
and is thrown away. Magnitudes of the discarded values: median 4.91, mean 6.47, maximum 26.70 fantasy
points; 726 of the 1,466 discarded values are 5.0 points or more `[fixture-scoped]`.

**Ordering is what makes C3/C4/C5 reachable at all.** In this payload the first `statSourceId == 1`
row is a prior-season row for 767 of the 1,074 players that have one `[fixture-scoped]`.

### 5.3 A worked C3 case, re-checkable in the tracked fixture

Mason Rudolph (ESPN id `3116407`), week 12. Scanning `stats` in order, the first row with
`scoringPeriodId == 12` and `statSourceId == 1` carries `seasonId: 2024` and `appliedTotal: 0.0`, so
`projected` is falsy and the slot stores `0.0`. Further down the same list, the row with
`seasonId: 2025`, `statSplitTypeId: 1`, `scoringPeriodId: 12`, `statSourceId: 1` carries
`appliedTotal: 16.3581`. One filter clause is the entire difference between storing `16.36` and
storing `0.0`. This is a single record in the fixture snapshot `[fixture-scoped]`; it illustrates the
mechanism and attributes no live slot.

---

## 6. Evidentiary reach — what this establishes and what it does not

This section is a requirement of the unit, not a caveat appended to it.

### 6.1 What the fixture **does** establish

An **existence-and-reachability** claim: which mechanism classes **occur** in a real ESPN payload of
this shape, parsed by this exact builder. That is a property of the **payload shape and the parse**,
not of any one snapshot's values, and it is what §5.2 asserts and all it asserts. It is re-checkable
by anyone, because the fixture is tracked.

### 6.2 What the fixture **cannot** establish

**Attribution of any individual live slot, and the proportion each class accounts for in the live
pool.** The fixture is a **different snapshot** from the live pool:

| Overlap between fixture and live pool | Count |
|---|---|
| fixture players | 1,090 `[fixture-scoped]` |
| live records present in the fixture | 715 of 799 `[fixture-scoped]` |
| of those, records whose `projected_points` array reproduces the live array exactly | 104 `[fixture-scoped]` |
| same zero/non-zero **pattern**, different magnitudes | 57 `[fixture-scoped]` |
| **different** zero/non-zero **pattern** | 554 `[fixture-scoped]` |

For 554 of the 715 overlapping players the fixture does not even agree with the live pool about
*which* weeks are zero. The disagreement is not confined to the zeroes either: of the non-bye slots
that are non-zero in the live pool for those overlapping players, only 3,340 of 6,964 carry exactly
the value the fixture's current-season row holds `[fixture-scoped]`. And the shadowing mechanism is
itself **order-dependent**, so a per-slot verdict derived from the fixture would not transfer even
for a player present in both.

There is a **third, independent** reason the mix does not transfer, and it is definitional rather than
empirical: §5.2's population is selected by a **different rule** from §2.1's, applying neither the
bye-week nor the all-zero-record exclusion. 58.1% of its classified slots come from players §2.1
removes outright `[fixture-scoped]`, and restricting to the comparable sub-population moves the mix
sharply (§5.2's second column). So even a fixture that *were* the same snapshot as the live pool would
not yield §2's population from §5.2's rule.

Consequently, and as a hard rule this document obeys:

> **No count, rate or proportion marked `[fixture-scoped]` anywhere in this document is a live-pool
> magnitude.** The class *inventory* transfers; the class *mix* does not. Every marked figure —
> in §5.2, in §5.3 and in the overlap table above — describes the fixture and nothing else.

### 6.3 Explicitly open

1. **Per-slot live attribution.** Which class each of the live pool's 2,395 slots belongs to is
   **unproven** and is not claimed anywhere above.
2. **The live class mix.** What proportion of the live pool's 2,395 slots each class accounts for is
   **unproven** and is not claimed anywhere above.

Both are closable by running the probe in §7 — which this unit deliberately did not run — or by the
follow-up ticket in §8.

---

## 7. Live probe — recorded, NOT EXECUTED

**NOT EXECUTED.** The commands below were **not run** by this unit and **no result anywhere in this
document derives from them**. They are recorded so the reader can close §6.3 themselves. The ticket
scope forbids a network call from any of its units, and that posture is intact: nothing in D3.3
touches the network, and the default test suite remains offline.

Step 1 — fetch a fresh payload of the same shape the fixture holds:

```bash
curl -sS -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' \
  -H 'X-Fantasy-Filter: {"players":{"limit":1500,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}' \
  'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3?view=kona_player_info&scoringPeriodId=0' \
  -o /tmp/espn_live_probe.json
```

Step 2 — attribute the live pool's own zero slots against that fresh payload:

```bash
.venv/bin/python - /tmp/espn_live_probe.json <<'PY'
import json, sys
from collections import Counter
SEASON = 2025
payload = json.load(open(sys.argv[1]))
stats_by_id = {str(e['player']['id']): e['player'].get('stats', []) for e in payload['players']}
counts = Counter()
skipped = 0          # live records absent from the probe payload — never silently dropped
examined = 0         # live zero-valued non-bye slots actually classified; check against 2,395
for pos in ('qb', 'rb', 'wr', 'te', 'k', 'dst'):
    for rec in json.load(open(f'data/player_data/{pos}_data.json'))[f'{pos}_data']:
        stats = stats_by_id.get(str(rec['id']))
        if stats is None:
            skipped += 1
            continue
        bye = rec.get('bye_week')
        pp = rec['projected_points']
        if all(v == 0 for v in pp):
            continue
        for i, v in enumerate(pp):
            week = i + 1
            if v != 0 or (bye and week == bye):
                continue
            examined += 1
            matches = [s for s in stats
                       if s.get('scoringPeriodId') == week and s.get('statSourceId') == 1]
            current = [s for s in matches
                       if s.get('seasonId') == SEASON and s.get('statSplitTypeId') == 1]
            cur_val = float(current[0]['appliedTotal']) if current and current[0].get('appliedTotal') else 0.0
            if not matches:
                counts['C1 no row'] += 1
            elif matches[0].get('seasonId') == SEASON and matches[0].get('statSplitTypeId') == 1:
                # Mirrors §9.2: an absent appliedTotal is C2b, NOT a genuine zero.
                counts['C2b current row, appliedTotal absent'
                       if matches[0].get('appliedTotal') is None
                       else 'C2a genuine zero'] += 1
            elif cur_val != 0.0:
                counts['C3 shadowed, value lost'] += 1
            elif current:
                counts['C4 shadowed, current also zero'] += 1
            else:
                counts['C5 shadow only, no current row'] += 1
for key, n in counts.most_common():
    print(f'{key:36s} {n:6d}')
print(f'{"TOTAL":36s} {sum(counts.values()):6d}')
print(f'{"slots examined":36s} {examined:6d}   (compare against the live 2,395 of §2.2)')
print(f'{"live records absent from payload":36s} {skipped:6d}')
PY
```

The output of Step 2 **is** the live class mix §6.3 leaves open. Running it requires network access
and is the reader's decision, not this unit's.

---

## 8. Disposition and follow-up

The result is **not** "all genuine ESPN zeroes" (§5.2), so the ticket's filing rule fires. The
follow-up is filed as **D21-projection-zero-slot-parse-miss-and-omission-guard**, and carries the finding, this document as its evidence, and
the scope question — a fetcher-side `seasonId` filter, an omission guard, a loud warning, or a
deliberate decision to do nothing. **Choosing among those remedies is that ticket's own design work,
not this document's**, and no fix is attempted here.

The null-result arm does not apply: it fires only on an all-genuine-zeroes disposition, and this
disposition is mixed.

---

## 9. Reproduction

No analysis script is committed. Both snippets below are self-contained, run from the repository
root, and re-derive every figure in §2.2, §4, §5 and §6. §2.3's aggregates (the per-player
zero-count distribution, the block classification, the position tally and the rate) are stated from
the same data but are **not** emitted by these snippets.

### 9.1 Population, baselines and the schedule cross-check (§2, §4)

Pass a git ref to measure a historical tree (`f1f187e0^` for the pre-repair column) or no argument to
measure the working tree.

```python
# BEGIN POPULATION SNIPPET
import csv, json, subprocess, sys
POSITIONS = ('qb', 'rb', 'wr', 'te', 'k', 'dst')
ref = sys.argv[1] if len(sys.argv) > 1 else None
records = []
for pos in POSITIONS:
    rel = f'data/player_data/{pos}_data.json'
    text = (subprocess.run(['git', 'show', f'{ref}:{rel}'], capture_output=True, text=True,
                           check=True).stdout if ref else open(rel).read())
    records += [(pos, r) for r in json.loads(text)[f'{pos}_data']]
all_zero, affected, slots, bad_bye, phantom = [], [], [], 0, 0
for pos, rec in records:
    pp, bye = rec['projected_points'], rec.get('bye_week')
    if not bye or not (1 <= bye <= 17):
        bad_bye += 1
    elif pp[bye - 1] != 0:
        phantom += 1
    if all(v == 0 for v in pp):
        all_zero.append(rec)
        continue
    weeks = [i + 1 for i, v in enumerate(pp) if v == 0 and not (bye and i + 1 == bye)]
    if weeks:
        affected.append((rec, weeks))
        slots += [(rec['team'], w) for w in weeks]
top = {r['id'] for _, r in sorted(records, key=lambda pr: sum(pr[1]['projected_points']),
                                  reverse=True)[:100]}
hit = [a for a in affected if a[0]['id'] in top]
print(f'records {len(records)} | all-zero {len(all_zero)} | affected {len(affected)} | '
      f'slots {len(slots)} | top100 {len(hit)}/{sum(len(a[1]) for a in hit)} | '
      f'bad bye_week {bad_bye} | phantom byes {phantom}')
sched = {(r['team'], int(r['week'])): r['opponent']
         for r in csv.DictReader(open('data/season_schedule.csv'))}
has = sum(1 for k in slots if sched.get(k, '').strip())
empty = sum(1 for k in slots if k in sched and not sched[k].strip())
print(f'schedule: has_opponent {has} | empty_opponent {empty} | unknown {len(slots) - has - empty}')
# END POPULATION SNIPPET
```

### 9.2 Fixture mechanism classes and the transfer bound (§5, §6)

```python
# BEGIN FIXTURE SNIPPET
import json, statistics
from collections import Counter
SEASON = 2025
POSITIONS = ('qb', 'rb', 'wr', 'te', 'k', 'dst')
fixture = json.load(open('tests/fixtures/espn_api/season_projections_2025.json'))
players = {str(e['player']['id']): e['player'].get('stats', []) for e in fixture['players']}
live = {}
for pos in POSITIONS:
    for rec in json.load(open(f'data/player_data/{pos}_data.json'))[f'{pos}_data']:
        live[str(rec['id'])] = rec


def exporter_array(stats):
    out = []
    for week in range(1, 18):
        projected = None
        for stat in stats:
            if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1:
                projected = stat.get('appliedTotal')
                break
        out.append(float(projected) if projected else 0.0)
    return out


def current_row(stats, week):
    for stat in stats:
        if (stat.get('seasonId') == SEASON and stat.get('statSplitTypeId') == 1
                and stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1):
            return stat
    return None


classes, lost = Counter(), []
for pid, stats in players.items():
    for i, value in enumerate(exporter_array(stats)):
        if value != 0.0:
            continue
        week = i + 1
        matches = [s for s in stats
                   if s.get('scoringPeriodId') == week and s.get('statSourceId') == 1]
        cur = current_row(stats, week)
        cur_val = float(cur['appliedTotal']) if cur and cur.get('appliedTotal') else 0.0
        if not matches:
            classes['C1'] += 1
        elif matches[0].get('seasonId') == SEASON and matches[0].get('statSplitTypeId') == 1:
            classes['C2b' if matches[0].get('appliedTotal') is None else 'C2a'] += 1
        elif cur_val != 0.0:
            classes['C3'] += 1
            lost.append(cur_val)
        elif cur:
            classes['C4'] += 1
        else:
            classes['C5'] += 1
print('classes', dict(sorted(classes.items())), 'total', sum(classes.values()))
print(f'C3 lost values: median {statistics.median(lost):.2f} mean {statistics.mean(lost):.2f} '
      f'max {max(lost):.2f} | >=5.0 pts {sum(1 for v in lost if v >= 5.0)}')
first_prior = sum(1 for s in players.values()
                  if [r.get('seasonId') for r in s if r.get('statSourceId') == 1]
                  and [r.get('seasonId') for r in s if r.get('statSourceId') == 1][0] != SEASON)
have_row = sum(1 for s in players.values() if any(r.get('statSourceId') == 1 for r in s))
print(f'players whose first statSourceId=1 row is a prior season: {first_prior}/{have_row}')
exact = same = diff = match = seen = 0
for pid, rec in live.items():
    if pid not in players:
        continue
    fa, la = exporter_array(players[pid]), rec['projected_points']
    bye = rec.get('bye_week')
    if bye and 1 <= bye <= 17:
        fa[bye - 1] = 0.0
    if all(abs(a - b) < 1e-9 for a, b in zip(fa, la)):
        exact += 1
    elif [a == 0 for a in fa] == [b == 0 for b in la]:
        same += 1
    else:
        diff += 1
    if all(v == 0 for v in la):
        continue
    for i, v in enumerate(la):
        if v == 0 or (bye and i + 1 == bye):
            continue
        seen += 1
        cur = current_row(players[pid], i + 1)
        cur_val = float(cur['appliedTotal']) if cur and cur.get('appliedTotal') else 0.0
        if abs(cur_val - v) < 1e-6:
            match += 1
print(f'fixture players {len(players)} | overlap {exact + same + diff} of {len(live)} | '
      f'exact {exact} | same pattern {same} | different pattern {diff}')
print(f'live non-zero non-bye slots matching the fixture current-season value: {match} of {seen}')
# END FIXTURE SNIPPET
```
