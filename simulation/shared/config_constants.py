BASE_CONFIG_PARAMS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'NFL_SCORING_FORMAT',
    'DRAFT_NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'INJURY_PENALTIES',
    'DRAFT_ORDER_BONUSES',
    'DRAFT_ORDER',
    'MAX_POSITIONS',
    'FLEX_ELIGIBLE_POSITIONS',
    'ADP_SCORING',
    'PLAYER_RATING_SCORING',
    'OPPONENT_TEAMS',
    # D17.8 G1: ESPN league identity. Added by D17.1 to league_config.json but
    # omitted from this list, so extract_base_params dropped both keys from every
    # promoted payload -- and, being absent from PRESERVE_KEYS too, an accuracy
    # --promote silently DELETED the user's league identity and broke ownership
    # fetching entirely. Same live-only, user-maintained shape as OPPONENT_TEAMS
    # above; both lists are required (see AccuracyResultsManager.PRESERVE_KEYS).
    'ESPN_LEAGUE_ID',
    'ESPN_TEAM_ID',
    # D17.8 G7: the SAME bug as the ESPN keys above, with different keys. Both
    # live only in league_config.json, are read and validated by ConfigManager,
    # and were in neither list -- so every accuracy promote deleted them and
    # ConfigManager silently fell back to [] and 1.0. Named in the very
    # test_config_constants message this ticket read three times and classified
    # as cosmetic drift: that `unexpected=` list is not test noise, it is an
    # INVENTORY of keys the promote will drop.
    'NFL_TEAM_PENALTY',
    'NFL_TEAM_PENALTY_WEIGHT',
    # D18.5: the same live-only, user-maintained shape as the precedents above.
    # SURVIVAL_SCORING is added to data/configs/league_config.json by the draft-cockpit
    # cutover and exists in no source folder, so without membership here
    # extract_base_params drops it from every promoted payload -- and without the twin
    # entry in AccuracyResultsManager.PRESERVE_KEYS an accuracy --promote deletes the
    # user's survival ladder outright. Both lists are required.
    'SURVIVAL_SCORING'
]

WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING',
    'PERFORMANCE_SCORING',
    'MATCHUP_SCORING',
    'SCHEDULE_SCORING',
    'TEMPERATURE_SCORING',
    'WIND_SCORING',
    'LOCATION_MODIFIERS'
]
