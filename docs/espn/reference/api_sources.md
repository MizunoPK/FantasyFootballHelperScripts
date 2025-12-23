# ESPN Fantasy Football API - Sources and References

**Last Updated:** 2025-12-23
**API Version:** v3

---

## Table of Contents

1. [Official ESPN API](#official-espn-api)
2. [Community Resources](#community-resources)
3. [GitHub Libraries and Tools](#github-libraries-and-tools)
4. [API Documentation Projects](#api-documentation-projects)
5. [Stat ID Mappings](#stat-id-mappings)
6. [Tutorials and Guides](#tutorials-and-guides)
7. [Important Notes](#important-notes)

---

## Official ESPN API

### Primary Endpoint

```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/
```

**Base URL Structure:**
```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/{LEAGUE_TYPE}
```

**Parameters:**
- `SEASON`: Year (e.g., 2024)
- `LEAGUE_TYPE`: Scoring format
  - `1` = Standard
  - `2` = Half PPR
  - `3` = Full PPR

**Common Views:**
- `view=kona_player_info` - Player data, stats, projections
- `view=mMatchup` - Matchup data
- `view=mRoster` - Roster data
- `view=mTeam` - Team data

### Important Headers

**Required for accessing all players (including defenses):**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
X-Fantasy-Filter: {"players":{"limit":2000,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}
```

**Critical Finding:** Without the `X-Fantasy-Filter` header with `limit:2000`, the API only returns ~50 players and omits DST/defense players entirely.

### Official ESPN Resources

- **ESPN Fantasy Football Homepage:** https://fantasy.espn.com/football/
- **ESPN Fan Support:** https://support.espn.com/hc/en-us
  - [Defense and Special Teams (D/ST) Scoring](https://support.espn.com/hc/en-us/articles/115003847231-Defense-and-Special-Teams-D-ST-Scoring)
  - [Scoring & Stat Corrections](https://support.espn.com/hc/en-us/articles/360000099732-Scoring-Stat-Corrections)
  - [Fantasy Football Acronyms](https://support.espn.com/hc/en-us/articles/115003862972-Fantasy-Football-Acronyms)
- **Stat Corrections Page:** https://fantasy.espn.com/football/statcorrections

**Note:** ESPN does not provide official public API documentation for their fantasy football API. All documentation has been reverse-engineered by the community.

---

## Community Resources

### Primary Stat ID Mapping Source

**cwendt94/espn-api**
- **Repository:** https://github.com/cwendt94/espn-api
- **Stat Mapping File:** https://github.com/cwendt94/espn-api/blob/master/espn_api/football/constant.py
- **Description:** Popular Python library (1,000+ stars) for ESPN Fantasy API
- **Coverage:** Football, Basketball, Hockey, Baseball
- **Key File:** `constant.py` contains `PLAYER_STATS_MAP`, `POSITION_MAP`, `PRO_TEAM_MAP`

**Important Note:** The stat ID mappings in this library appear to be partially outdated or from an older ESPN API version. Cross-validate with empirical data when possible.

### R Package for ESPN API

**dynastyprocess/ffscrapr**
- **Repository:** https://github.com/dynastyprocess/ffscrapr
- **Stat Map:** https://rdrr.io/github/dynastyprocess/ffscrapr/man/dot-espn_stat_map.html
- **CRAN Package:** https://rdrr.io/cran/ffscrapr/man/dot-espn_stat_map.html
- **Description:** R package for fantasy football data scraping
- **Coverage:** ESPN, Sleeper, MFL, Fleaflicker platforms

---

## GitHub Libraries and Tools

### Python Libraries

1. **cwendt94/espn-api** (Most Popular)
   - **URL:** https://github.com/cwendt94/espn-api
   - **Install:** `pip install espn-api`
   - **Stars:** 1,000+
   - **Documentation:** https://github.com/cwendt94/espn-api/wiki/Football-Intro
   - **Features:** League data, team stats, player stats, box scores

2. **DesiPilla/espn-api-v3**
   - **URL:** https://github.com/DesiPilla/espn-api-v3
   - **Description:** Advanced data analytics focused on ESPN API v3
   - **Features:** League, team, and player classes for data analysis

3. **rbarton65/espnff**
   - **URL:** https://github.com/rbarton65/espnff
   - **Description:** Interfaces with ESPN Fantasy Football private API
   - **Status:** Older library, may not be actively maintained

### JavaScript/Node.js Libraries

1. **mkreiser/ESPN-Fantasy-Football-API**
   - **URL:** https://github.com/mkreiser/ESPN-Fantasy-Football-API
   - **Description:** JS API client for web and NodeJS
   - **Install:** Available as npm package

2. **WictorWilnd/ESPN-Fantasy-Football-API**
   - **URL:** https://github.com/WictorWilnd/ESPN-Fantasy-Football-API
   - **Description:** Alternative JavaScript implementation

### R Libraries

1. **k5cents/fflr**
   - **URL:** https://github.com/k5cents/fflr
   - **Documentation:** https://k5cents.github.io/fflr/
   - **Description:** Retrieve ESPN Fantasy Football data in R

---

## API Documentation Projects

### Community-Maintained Documentation

1. **ESPN API Endpoints Gist**
   - **URL:** https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c
   - **Description:** Comprehensive list of NFL API endpoints from ESPN
   - **Coverage:** Statistics, play-by-plays, projections, schedules

2. **Public ESPN API Documentation**
   - **URL:** https://github.com/pseudo-r/Public-ESPN-API
   - **Description:** Community effort to document ESPN API endpoints
   - **Contents:** Available endpoints, parameters, response formats, examples

3. **ESPN Fantasy Football API Static Site**
   - **URL:** http://espn-fantasy-football-api.s3-website.us-east-2.amazonaws.com/
   - **Description:** Static site with API documentation

---

## Stat ID Mappings

### Confirmed Stat IDs (Empirically Validated)

**Defense Stats:**
- `95`: Interceptions (defensiveInterceptions)
- `99`: Fumbles Recovered (empirically validated) OR Sacks (per GitHub - conflict)
- `106`: Forced Fumbles (defensiveForcedFumbles)
- `107`: Assisted Tackles (defensiveAssistedTackles)
- `108`: Solo Tackles (defensiveSoloTackles)
- `109`: Total Tackles (defensiveTotalTackles) - Equals 107 + 108
- `112`: Sacks (empirically validated - not in GitHub mapping)
- `113`: Passes Defensed (defensivePassesDefensed)
- `118`: Punt Returns (puntsReturned - per GitHub)
- `120`: Points Allowed (defensivePointsAllowed) ✅ 100% validated
- `127`: Yards Allowed (defensiveYardsAllowed) ✅ 100% validated
- `187`: Duplicate of stat_120 (points allowed)

**Offensive Stats:**
- `0`: Passing Attempts
- `1`: Passing Completions
- `3`: Passing Yards
- `4`: Passing TDs
- `14`: Interceptions (thrown)
- `23`: Rushing Attempts
- `24`: Rushing Yards
- `25`: Rushing TDs
- `42`: Receiving Yards
- `43`: Receiving TDs
- `53`: Receptions
- `58`: Targets

**Kicker Stats:**
- `80`: FG Made <40 yards (per GitHub) OR XP Made (empirically uncertain)
- `81`: FG Attempted <40 yards (per GitHub) OR XP Attempted (empirically uncertain)
- `83`: Field Goals Made (total) ✅ 100% validated
- `84`: Field Goals Attempted (total) ✅ 100% validated
- `85`: Missed Field Goals (total)
- `86`: Extra Points Made
- `87`: Extra Points Attempted
- `88`: Missed Extra Points
- `214-234`: Field goal yardage increments (cumulative season stats)

### Stat ID Mapping Discrepancies

**GitHub Mapping vs Empirical Data:**

| Stat | GitHub (cwendt94) | Empirical Validation | Recommended |
|------|-------------------|---------------------|-------------|
| 99 | Sacks | Fumbles Recovered | Empirical |
| 112 | Not documented | Sacks | Empirical |
| 118 | Punt Returns | Safeties? | GitHub |

**Reason for Discrepancies:** ESPN may have changed stat IDs over time, or the GitHub mapping is from an older API version.

**Recommendation:** When conflicts exist, trust empirical validation over GitHub mapping.

### Discovering Stat IDs

**Method 1: ESPN Website Inspection**
- Visit https://fantasy.espn.com
- Inspect `/commons/main.js` file
- Look for `scoringSettings/scoringItems` with format: `{'statId': X, 'points': Y}`

**Method 2: API Response Analysis**
- Fetch player data from API
- Examine `stats` array in response
- Each stat object has `statSourceId` (0=actual, 1=projected) and `stats` dict

**Method 3: Community Mappings**
- Reference cwendt94/espn-api constant.py
- Cross-validate with ffscrapr R package mapping
- Verify with empirical game data

---

## Tutorials and Guides

### Comprehensive Tutorials

1. **Steven Morse - ESPN Fantasy API v3**
   - **URL:** https://stmorse.github.io/journal/espn-fantasy-v3.html
   - **Topics:** API structure, authentication, endpoints, data extraction
   - **Language:** Python
   - **Follow-up:** https://stmorse.github.io/journal/espn-fantasy-2-python.html (Boxscores)
   - **Additional:** https://stmorse.github.io/journal/espn-fantasy-python.html (Earlier version)

2. **Red Green Refactor - ESPN API Tutorial Series**
   - **Part 1:** https://red-green-refactor.com/2020/05/04/retrieve-fantasy-football-stats-using-espns-api-introduction/
   - **Part 2:** https://red-green-refactor.com/2020/06/02/retrieve-fantasy-football-stats-using-espns-api-part-2/
   - **Topics:** API basics, authentication, data retrieval

3. **Thomas Wilde Tech - ESPN Fantasy Football API**
   - **URL:** https://thomaswildetech.com/blog/category/espn-fantasy-football-api/
   - **Topics:** Various ESPN API tutorials and guides

4. **Dusty Turner - ESPN Fantasy Football API 2020**
   - **URL:** https://dustysturner.com/post/espn-fantasy-football-api-2020/
   - **Topics:** Accessing the API, authentication, data extraction

### Package Documentation

1. **ffscrapr - ESPN Get Endpoint**
   - **URL:** https://ffscrapr.ffverse.com/articles/espn_getendpoint.html
   - **CRAN:** https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_getendpoint.html
   - **Topics:** Using ffscrapr to access ESPN endpoints

2. **espn-api Wiki**
   - **URL:** https://github.com/cwendt94/espn-api/wiki/Football-Intro
   - **Topics:** Getting started, authentication, common operations

---

## Important Notes

### API Limitations and Considerations

1. **No Official Documentation**
   - ESPN does not provide official public API documentation
   - All community documentation is reverse-engineered
   - API may change without notice

2. **Authentication**
   - Public leagues: No authentication required
   - Private leagues: Requires ESPN credentials or cookies
   - Use `espn_s2` and `SWID` cookies for private league access

3. **Rate Limiting**
   - No official rate limits published
   - Community recommendation: Be respectful with request frequency
   - Use caching when possible

4. **API Versions**
   - Current version: v3
   - Previous versions (v1, v2) may still be accessible but deprecated
   - Stat IDs may differ between versions

5. **Stat ID Stability**
   - Stat IDs appear to change over time
   - Cross-validate mappings with current season data
   - Always verify critical stats empirically

6. **Data Availability**
   - Historical data available for past seasons
   - Projections typically available before season start
   - Actual stats populated after games are played

### Best Practices

1. **Always Include X-Fantasy-Filter Header**
   - Required for full player data (especially DST)
   - Set limit to 2000+ to get all players

2. **Verify Stat IDs Each Season**
   - ESPN may repurpose or change stat IDs
   - Validate against known game results

3. **Use Community Libraries When Possible**
   - Maintained libraries handle API changes
   - Built-in error handling and retries

4. **Cache API Responses**
   - Reduce API load
   - Faster development/testing
   - Respect ESPN's infrastructure

5. **Handle Errors Gracefully**
   - API may be temporarily unavailable
   - Network issues can occur
   - Implement retry logic with exponential backoff

---

## Additional Resources

### Community Discussions

- **GitHub Issues:** Check issues in cwendt94/espn-api for common problems
  - [statId lookup discussion](https://github.com/cwendt94/espn-api/issues/84)
  - [Getting Started Again](https://github.com/cwendt94/espn-api/discussions/499)

### API Response Examples

See `docs/espn/examples/` for sample JSON responses from various endpoints.

### Related Documentation

- **ESPN Player Data:** `docs/espn/espn_player_data.md`
- **ESPN Team Data:** `docs/espn/espn_team_data.md`
- **ESPN API Endpoints:** `docs/espn/espn_api_endpoints.md`
- **ESPN Reference Tables:** `docs/espn/espn_api_reference_tables.md`
- **Stat IDs Reference:** `docs/espn/reference/stat_ids.md`

---

## Contributing

If you discover new stat IDs, API endpoints, or corrections to this documentation:

1. Validate your findings with empirical data
2. Document the discovery process
3. Include source API responses (sanitized)
4. Update relevant documentation files
5. Note the date and season of discovery

**Last major update:** 2025-12-23 (Season 2024 data validation)

---

## License and Legal

**Disclaimer:** This documentation is for educational and personal use only. ESPN's Fantasy Football API is not officially public, and usage may be subject to ESPN's Terms of Service. Use responsibly and at your own risk.

**Fair Use:** This documentation references publicly available community resources and reverse-engineered API information. All ESPN trademarks and data belong to ESPN, Inc.
