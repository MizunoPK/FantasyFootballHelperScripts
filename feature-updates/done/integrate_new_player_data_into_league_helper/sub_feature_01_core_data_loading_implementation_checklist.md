# Implementation Checklist - Sub-Feature 1: Core Data Loading

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

**Reference Files:**
- Specs: `sub_feature_01_core_data_loading_spec.md`
- TODO: `sub_feature_01_core_data_loading_todo.md`

---

## From Traceability Matrix:

### Phase 1: Add Fields to FantasyPlayer

- [ ] **Task 1.1**: Add projected_points and actual_points arrays
      Spec: sub_feature_01_core_data_loading_spec.md lines 6, 32-37
      Requirements: NEW-6, NEW-7
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 1.2**: Add position-specific stat fields (7 Optional[Dict] fields)
      Spec: sub_feature_01_core_data_loading_spec.md lines 39-49
      Requirements: NEW-31 through NEW-37
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **QA CHECKPOINT 1**: Field additions verified
      Status: Pending
      Verified: [date/time]

### Phase 2: Implement FantasyPlayer.from_json()

- [ ] **Task 2.1**: Create from_json() classmethod
      Spec: sub_feature_01_core_data_loading_spec.md lines 161-240
      Requirements: CORE-1, CORE-2
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.2**: Implement array loading with validation
      Spec: sub_feature_01_core_data_loading_spec.md lines 186-191
      Requirements: NEW-12, NEW-13, NEW-14, NEW-15, CORE-3
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.3**: Implement drafted_by → drafted conversion
      Spec: sub_feature_01_core_data_loading_spec.md lines 193-200
      Requirements: Hybrid approach
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.4**: Load locked as boolean
      Spec: sub_feature_01_core_data_loading_spec.md lines 202-204
      Requirements: Phase 6 resolution
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.5**: Calculate fantasy_points from projected_points
      Spec: sub_feature_01_core_data_loading_spec.md lines 205-206
      Requirements: Calculated field
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.6**: Load position-specific nested stats
      Spec: sub_feature_01_core_data_loading_spec.md lines 208-216
      Requirements: NEW-38, CORE-4
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.7**: Return FantasyPlayer instance with all fields
      Spec: sub_feature_01_core_data_loading_spec.md lines 217-239
      Requirements: Complete initialization
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 2.8**: Add comprehensive docstring to from_json()
      Spec: sub_feature_01_core_data_loading_spec.md lines 164-177
      Requirements: CORE-5
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **QA CHECKPOINT 2**: from_json() method complete
      Status: Pending
      Verified: [date/time]

### Phase 3: Implement PlayerManager.load_players_from_json()

- [ ] **Task 3.1**: Create load_players_from_json() method
      Spec: sub_feature_01_core_data_loading_spec.md lines 242-265
      Requirements: CORE-6, CORE-7
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 3.2**: Implement position file iteration
      Spec: sub_feature_01_core_data_loading_spec.md lines 267-280
      Requirements: CORE-6, CORE-7
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 3.3**: Implement JSON parsing with error handling
      Spec: sub_feature_01_core_data_loading_spec.md lines 281-306
      Requirements: CORE-7, CORE-8
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 3.4**: Implement post-loading calculations
      Spec: sub_feature_01_core_data_loading_spec.md lines 308-318
      Requirements: CORE-8
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 3.5**: Add import statement for json module
      Spec: sub_feature_01_core_data_loading_spec.md (implicit)
      Requirements: Syntax
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **QA CHECKPOINT 3**: load_players_from_json() complete
      Status: Pending
      Verified: [date/time]

### Phase 4: Comprehensive Unit Testing

- [ ] **Task 4.1**: Test from_json() with complete data
      Spec: sub_feature_01_core_data_loading_spec.md lines 325-337
      Requirements: TEST-1, TEST-2
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 4.2**: Test from_json() array handling edge cases
      Spec: sub_feature_01_core_data_loading_spec.md lines 334-337
      Requirements: TEST-3
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 4.3**: Test from_json() error cases
      Spec: sub_feature_01_core_data_loading_spec.md lines 336-337
      Requirements: TEST-4
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 4.4**: Test load_players_from_json() success path
      Spec: sub_feature_01_core_data_loading_spec.md lines 340-344
      Requirements: TEST-5
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 4.5**: Test load_players_from_json() error handling
      Spec: sub_feature_01_core_data_loading_spec.md lines 346-363
      Requirements: TEST-6
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **Task 4.6**: Test round-trip preservation
      Spec: sub_feature_01_core_data_loading_spec.md lines 348-354
      Requirements: NEW-40
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] **QA CHECKPOINT 4**: All unit tests passing
      Status: Pending
      Verified: [date/time]

---

## Verification Log:

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| Task 1.1 | spec:6,32-37 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 1.2 | spec:39-49 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.1 | spec:161-240 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.2 | spec:186-191 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.3 | spec:193-200 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.4 | spec:202-204 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.5 | spec:205-206 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.6 | spec:208-216 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.7 | spec:217-239 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 2.8 | spec:164-177 | utils/FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 3.1 | spec:242-265 | league_helper/util/PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 3.2 | spec:267-280 | league_helper/util/PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 3.3 | spec:281-306 | league_helper/util/PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 3.4 | spec:308-318 | league_helper/util/PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 3.5 | spec:implicit | league_helper/util/PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.1 | spec:325-337 | tests/utils/test_FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.2 | spec:334-337 | tests/utils/test_FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.3 | spec:336-337 | tests/utils/test_FantasyPlayer.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.4 | spec:340-344 | tests/league_helper/util/test_PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.5 | spec:346-363 | tests/league_helper/util/test_PlayerManager.py:TBD | ⏳ | ⏳ | Pending |
| Task 4.6 | spec:348-354 | tests/utils or integration:TBD | ⏳ | ⏳ | Pending |

---

## Completion Summary

**Total Tasks:** 25 (21 implementation + 4 QA checkpoints)
**Completed:** 0
**Remaining:** 25

**Ready for Post-Implementation QC:** NO (implementation not started)
