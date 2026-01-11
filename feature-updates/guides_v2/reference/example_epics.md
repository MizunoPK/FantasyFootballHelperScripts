# Example Epic Reference

**Purpose:** Canonical examples for documentation consistency

---

## Primary Example: improve_draft_helper

**Use this example for:**
- Multi-feature epics (3 features)
- End-to-end workflow demonstrations
- Stage transition examples

**KAI Number:** KAI-1 (always use as first epic example)

**Features:**
1. **feature_01_adp_integration** - Integrate Average Draft Position data
2. **feature_02_matchup_system** - Add matchup difficulty ratings
3. **feature_03_performance_tracker** - Track player accuracy vs projections

**Characteristics:**
- Medium complexity
- Clear dependencies (feature 2 depends on feature 1)
- Realistic for Fantasy Football domain
- 3 features (shows multi-feature coordination)

---

## Secondary Example: add_player_validation

**Use this example for:**
- Simple 2-feature epics
- Bug fix examples
- Quick demonstrations

**KAI Number:** KAI-2

**Features:**
1. **feature_01_name_validation** - Validate player names
2. **feature_02_stats_validation** - Validate player statistics

**Characteristics:**
- Low complexity
- Independent features
- Good for teaching basics

---

## Tertiary Example: integrate_matchup_data

**Use this example for:**
- Complex 4+ feature epics
- Advanced workflow scenarios
- Cross-feature dependency examples

**KAI Number:** KAI-3

**Features:**
1. **feature_01_data_fetcher** - Fetch matchup data from API
2. **feature_02_parser** - Parse and normalize data
3. **feature_03_calculator** - Calculate matchup difficulty scores
4. **feature_04_integration** - Integrate with existing systems

**Characteristics:**
- High complexity
- Sequential dependencies (linear chain)
- Realistic for data integration
- 4 features (shows complex coordination)

---

## Example File Names

**Original request:**
- `feature-updates/improve_draft_helper.txt`
- `feature-updates/add_player_validation.txt`
- `feature-updates/integrate_matchup_data.txt`

**Epic folders:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-2-add_player_validation/`
- `feature-updates/KAI-3-integrate_matchup_data/`

**Git branches:**
- `epic/KAI-1`
- `feat/KAI-2`
- `epic/KAI-3`

---

## When to Use Which Example

| Context | Example to Use | Reason |
|---------|----------------|--------|
| Stage 1 planning | improve_draft_helper | Shows feature breakdown |
| Stage 2 deep dive | improve_draft_helper | Shows multi-feature coordination |
| Stage 5 implementation | improve_draft_helper | Full workflow demonstration |
| Bug fix workflow | add_player_validation | Simple, clear |
| Cross-feature dependencies | integrate_matchup_data | Complex dependencies |
| Quick examples | add_player_validation | Least cognitive load |
| Comprehensive examples | improve_draft_helper | Most realistic |

---

## Consistency Guidelines

**When writing examples:**
1. Always use KAI-1 for improve_draft_helper
2. Always use KAI-2 for add_player_validation
3. Always use KAI-3 for integrate_matchup_data
4. Don't invent new example epics without updating this doc
5. Feature names should be descriptive (not generic "feature1", "feature2")

---

**END OF EXAMPLE EPIC REFERENCE**
