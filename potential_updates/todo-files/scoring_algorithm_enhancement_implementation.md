# Scoring Algorithm Enhancement - Implementation TODO

## [SUMMARY] Objective Overview
Enhance the fantasy football scoring algorithm to improve accuracy by incorporating market wisdom and contextual factors from ESPN API. Based on analysis of player discrepancies (Hunt vs Henderson case), integrate Average Draft Position, ESPN Player Ratings, and Team Quality data to better align scoring with real fantasy manager evaluations.

## [TARGET] Master Plan

### Phase 1: Analysis and Design
- [x] **1.1** Analyze current scoring algorithm limitations with Hunt vs Henderson case study
- [x] **1.2** Identify key ESPN API data points for enhancement (ADP, player rating, team quality)
- [x] **1.3** Design two-phase implementation approach (data collection + scoring enhancement)
- [ ] **1.4** Plan new CSV column structure and FantasyPlayer class modifications
- [ ] **1.5** Design scoring adjustment algorithms with configurable weights and caps

**Analysis Results:**
- Current system: Hunt 135.54 pts vs Henderson 121.97 pts (Hunt +13.57)
- Reality: Henderson has higher roster rates despite lower projection
- Missing factors: Market wisdom (ADP), expert ratings, team context, age/opportunity

### Phase 2: Data Collection Enhancement (player_data_fetcher)
- [ ] **2.1** Update FantasyPlayer class to include new fields (adp, player_rating, team_offensive_rank, team_defensive_rank)
- [ ] **2.2** Enhance ESPN client to fetch ownership.averageDraftPosition during existing API calls
- [ ] **2.3** Enhance ESPN client to fetch playerPoolEntry.playerRating during existing API calls
- [ ] **2.4** Add team quality data collection (offensive/defensive rankings from ESPN team data)
- [ ] **2.5** Update CSV export functionality to include new columns in players.csv
- [ ] **2.6** Ensure no additional API overhead - integrate with existing API call patterns

### Phase 3: Scoring Algorithm Enhancement (draft_helper)
- [ ] **3.1** Add configuration options for enabling/disabling each adjustment factor
- [ ] **3.2** Implement ADP-based market wisdom scoring adjustment with configurable weights
- [ ] **3.3** Implement ESPN player rating scoring adjustment with reasonable caps
- [ ] **3.4** Implement team quality context adjustments (offensive for skill positions, defensive for DEF/DST)
- [ ] **3.5** Update draft_helper scoring algorithm to apply adjustments in sequence
- [ ] **3.6** Add graceful handling for missing data (backward compatibility with older CSV files)

### Phase 4: Configuration and Integration
- [ ] **4.1** Add configuration constants for adjustment weights and caps
- [ ] **4.2** Create enable/disable toggles for each enhancement factor
- [ ] **4.3** Update load_players_from_csv to handle new columns
- [ ] **4.4** Ensure integration with existing roster construction and trade analysis
- [ ] **4.5** Add logging for scoring adjustments when debugging is enabled

### Phase 5: Testing and Validation
- [ ] **5.1** Test player_data_fetcher with enhanced ESPN API data collection
- [ ] **5.2** Verify new CSV columns are populated correctly
- [ ] **5.3** Test draft_helper with enhanced scoring algorithm
- [ ] **5.4** Validate Hunt vs Henderson scoring adjustment (Henderson should rank higher than Hunt after enhancements)
- [ ] **5.5** Test backward compatibility with existing CSV files
- [ ] **5.6** Run existing unit tests to ensure no regressions

### Phase 6: Documentation and Cleanup
- [ ] **6.1** Update configuration documentation for new scoring options
- [ ] **6.2** Update FantasyPlayer class documentation
- [ ] **6.3** Update CLAUDE.md with new scoring algorithm features
- [ ] **6.4** Move scoring_algorithm_enhancement.txt to done folder
- [ ] **6.5** Create example configuration showing recommended settings

## [NOTE] Context Notes

**Current Issue**: Scoring algorithm only uses fantasy point projections, missing contextual factors that drive real fantasy manager decisions, causing discrepancies between projections and actual roster rates.

**Enhancement Benefits**:
- Better alignment with fantasy manager evaluations
- Incorporation of market wisdom through ADP
- Expert evaluation through ESPN player ratings
- Team context consideration for opportunity assessment
- Maintains statistical foundation while adding contextual intelligence

**Key Technical Requirements**:
- No additional API calls beyond existing patterns
- Backward compatibility with current CSV structure
- Configurable weights to prevent over-adjustment
- Sequential application of adjustment factors
- Graceful degradation when data unavailable

## [OK] Implementation Strategy

**Data Flow Architecture**:
1. **player_data_fetcher**: Fetch enhanced data -> Export to enhanced CSV
2. **draft_helper**: Read enhanced CSV -> Apply scoring adjustments -> Use in recommendations

**New CSV Column Structure**:
```csv
id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,adp,player_rating,team_offensive_rank,team_defensive_rank
```

**Scoring Adjustment Algorithm**:
```
enhanced_score = base_fantasy_points
                 ? adp_adjustment_factor
                 ? player_rating_factor
                 ? team_quality_factor
```

## ? Key Technical Changes

1. **FantasyPlayer Class**: Add adp, player_rating, team_offensive_rank, team_defensive_rank fields
2. **ESPN Client**: Enhanced data collection during existing API calls
3. **CSV Export**: Additional columns in all export formats
4. **Draft Helper Scoring**: Sequential adjustment application with configuration options
5. **Configuration**: New settings for adjustment weights, caps, and enable/disable flags

## ? Progress Tracking

### Session History
#### Session 1 (Current)
- [x] Created comprehensive TODO file based on scoring_algorithm_enhancement.txt
- [x] Analyzed current limitations with Hunt vs Henderson case study
- [x] Designed two-phase implementation approach
- [ ] **Next**: Begin Phase 1 design tasks (1.4-1.5)

## [WARNING] Important Notes

- Preserve all existing scoring functionality when enhancements are disabled
- Maintain API efficiency - no additional ESPN API calls beyond current patterns
- Ensure conservative adjustment factors to enhance rather than override projections
- Test thoroughly with various player types and team contexts
- Validate that enhanced scoring better correlates with actual fantasy manager behavior

## [IMPROVEMENT] Expected Results

After implementation, players like Henderson should score closer to their market value:
- **Before**: Hunt scoring higher than Henderson despite Henderson having higher roster rates
- **After**: Henderson should rank higher than Hunt, reflecting market sentiment
- Better alignment between projections and roster rates
- More accurate draft and trade recommendations