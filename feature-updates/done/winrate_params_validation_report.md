# Win-Rate Simulation Parameter Validation Report
**Date**: 1766190137.843817
**Parameters Validated**: 6

## Parameters Under Test
1. `SAME_POS_BYE_WEIGHT`
2. `DIFF_POS_BYE_WEIGHT`
3. `PRIMARY_BONUS`
4. `SECONDARY_BONUS`
5. `ADP_SCORING_WEIGHT`
6. `PLAYER_RATING_SCORING_WEIGHT`

## Validation Results

### SAME_POS_BYE_WEIGHT

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[0.0, 0.5], precision=2

**✅ PASS** - req2_range_compliance
- Valid range [0.0, 0.5] with precision 2

**✅ PASS** - req3_precision_compliance
- Precision 2 (float (0.01 steps)) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: SAME_POS_BYE_WEIGHT)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

### DIFF_POS_BYE_WEIGHT

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[0.0, 0.3], precision=2

**✅ PASS** - req2_range_compliance
- Valid range [0.0, 0.3] with precision 2

**✅ PASS** - req3_precision_compliance
- Precision 2 (float (0.01 steps)) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: DIFF_POS_BYE_WEIGHT)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

### PRIMARY_BONUS

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[25, 150], precision=0

**✅ PASS** - req2_range_compliance
- Valid range [25, 150] with precision 0

**✅ PASS** - req3_precision_compliance
- Precision 0 (integer) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: DRAFT_ORDER_BONUSES)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

### SECONDARY_BONUS

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[25, 150], precision=0

**✅ PASS** - req2_range_compliance
- Valid range [25, 150] with precision 0

**✅ PASS** - req3_precision_compliance
- Precision 0 (integer) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: DRAFT_ORDER_BONUSES)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

### ADP_SCORING_WEIGHT

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[0.5, 7.0], precision=2

**✅ PASS** - req2_range_compliance
- Valid range [0.5, 7.0] with precision 2

**✅ PASS** - req3_precision_compliance
- Precision 2 (float (0.01 steps)) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: ADP_SCORING)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

### PLAYER_RATING_SCORING_WEIGHT

**✅ PASS** - req1_param_in_definitions
- Found in PARAM_DEFINITIONS: range=[0.5, 4.0], precision=2

**✅ PASS** - req2_range_compliance
- Valid range [0.5, 4.0] with precision 2

**✅ PASS** - req3_precision_compliance
- Precision 2 (float (0.01 steps)) - OK

**✅ PASS** - req4_param_classification
- Classified as BASE_CONFIG_PARAMS (section: PLAYER_RATING_SCORING)

**✅ PASS** - req5_config_generator_support
- ConfigGenerator generated 3 shared test values

## Summary Table

| Parameter | Definitions | Range | Precision | Classification | ConfigGen |
|-----------|-------------|-------|-----------|----------------|----------|
| SAME_POS_BYE_WEIGHT | ✅ | ✅ | ✅ | ✅ | ✅ |
| DIFF_POS_BYE_WEIGHT | ✅ | ✅ | ✅ | ✅ | ✅ |
| PRIMARY_BONUS | ✅ | ✅ | ✅ | ✅ | ✅ |
| SECONDARY_BONUS | ✅ | ✅ | ✅ | ✅ | ✅ |
| ADP_SCORING_WEIGHT | ✅ | ✅ | ✅ | ✅ | ✅ |
| PLAYER_RATING_SCORING_WEIGHT | ✅ | ✅ | ✅ | ✅ | ✅ |

