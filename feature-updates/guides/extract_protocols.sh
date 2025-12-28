#!/bin/bash

# Standard Verification Protocol (lines 382-454)
sed -n '382,454p' protocols_reference.md > protocols/standard_verification.md

# Skeptical Re-verification Protocol (lines 455-582)
sed -n '455,582p' protocols_reference.md > protocols/skeptical_reverification.md

# Integration Gap Check Protocol (lines 583-662)
sed -n '583,662p' protocols_reference.md > protocols/integration_gap_check.md

# Algorithm Traceability Matrix Protocol (lines 663-690)
sed -n '663,690p' protocols_reference.md > protocols/algorithm_traceability_matrix.md

# TODO Specification Audit Protocol (lines 691-786)
sed -n '691,786p' protocols_reference.md > protocols/todo_specification_audit.md

# End-to-End Data Flow Protocol (lines 787-832)
sed -n '787,832p' protocols_reference.md > protocols/end_to_end_data_flow.md

# Fresh Eyes Review Protocol (lines 833-883)
sed -n '833,883p' protocols_reference.md > protocols/fresh_eyes_review.md

# Edge Case Verification Protocol (lines 884-917)
sed -n '884,917p' protocols_reference.md > protocols/edge_case_verification.md

# Test Coverage Planning Protocol (lines 918-1150)
sed -n '918,1150p' protocols_reference.md > protocols/test_coverage_planning.md

# Pre-Implementation Spec Audit Protocol (lines 1151-1376)
sed -n '1151,1376p' protocols_reference.md > protocols/pre_implementation_spec_audit.md

# Implementation Readiness Protocol (lines 1377-1435)
sed -n '1377,1435p' protocols_reference.md > protocols/implementation_readiness.md

# Interface Verification Protocol (lines 1436-1579)
sed -n '1436,1579p' protocols_reference.md > protocols/interface_verification.md

# Requirement Verification Protocol (lines 1580-1725)
sed -n '1580,1725p' protocols_reference.md > protocols/requirement_verification.md

# Smoke Testing Protocol (lines 1726-1742 + next section until QC)
sed -n '1726,1867p' protocols_reference.md > protocols/smoke_testing.md

# Quality Control Review Protocol (lines 1868-1890)
sed -n '1868,1890p' protocols_reference.md > protocols/quality_control_review.md

# Lessons Learned Protocol (lines 1891-1952)
sed -n '1891,1952p' protocols_reference.md > protocols/lessons_learned.md

# Guide Update Protocol (lines 1953-1997)
sed -n '1953,1997p' protocols_reference.md > protocols/guide_update.md

# Pre-commit Validation Protocol (lines 1998-2066)
sed -n '1998,2066p' protocols_reference.md > protocols/pre_commit_validation.md

echo "Protocols extracted successfully!"
