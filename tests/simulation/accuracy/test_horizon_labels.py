"""
Unit Tests for the Accuracy Horizon Labels Module

Covers simulation/accuracy/horizon_labels - the single definition of the accuracy
simulation's weekly horizon set, its cardinality, and the two operator-facing
banner label strings the CLI runner and AccuracySimulationManager share (T77 D1).
The consumer-side drift guards live in
tests/root_scripts/test_run_accuracy_simulation.py; this file covers the module
itself.

Author: Kai Mizuno
"""

# Standard library
import inspect

# Local
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.tests.simulation.accuracy import horizon_labels
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.horizon_labels import (
    HORIZON_COUNT,
    WEEK_RANGES,
    candidate_values_label,
    configs_per_param_label,
)


class TestWeekRanges:
    """The canonical horizon set (T77 D2 - moved here, content unchanged)."""

    def test_holds_exactly_the_four_weekly_horizons_in_order(self):
        # Assert
        assert list(WEEK_RANGES) == [
            'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17'
        ], f"horizon set changed: {list(WEEK_RANGES)}"

    def test_each_key_maps_to_its_inclusive_week_bounds(self):
        # Assert
        assert WEEK_RANGES == {
            'week_1_5': (1, 5),
            'week_6_9': (6, 9),
            'week_10_13': (10, 13),
            'week_14_17': (14, 17),
        }

    def test_accuracy_results_manager_re_exports_the_same_object(self):
        """T77 AC2: the re-export is an alias, not a second dict."""
        # Act
        from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.AccuracyResultsManager import WEEK_RANGES as re_exported

        # Assert
        assert re_exported is WEEK_RANGES, (
            "AccuracyResultsManager.WEEK_RANGES is no longer the canonical object - "
            "a copy would let the two drift apart"
        )


class TestHorizonCount:
    """HORIZON_COUNT is derived from WEEK_RANGES, never restated (T77 D5)."""

    def test_equals_the_number_of_week_ranges(self):
        # Assert
        assert HORIZON_COUNT == len(WEEK_RANGES) == 4

    def test_is_defined_as_len_week_ranges_not_as_a_literal(self):
        """A literal here would defeat the module's whole purpose (T77 AC1)."""
        # Act
        definition = [
            line for line in inspect.getsource(horizon_labels).splitlines()
            if line.startswith('HORIZON_COUNT')
        ]

        # Assert
        assert definition == ['HORIZON_COUNT = len(WEEK_RANGES)'], (
            f"HORIZON_COUNT is no longer derived from WEEK_RANGES: {definition}"
        )


class TestCandidateValuesLabel:
    """The first shared banner label."""

    def test_renders_the_pinned_operator_facing_text(self):
        # Assert - pinned as a LITERAL, never rebuilt from the builder (T77 AC6/D4)
        assert candidate_values_label(6) == (
            'Candidate values per parameter per horizon: 6'
        )

    def test_thousands_separates_large_counts(self):
        # Assert
        assert candidate_values_label(12345) == (
            'Candidate values per parameter per horizon: 12,345'
        )


class TestConfigsPerParamLabel:
    """The second shared banner label - the one carrying the horizon count."""

    def test_renders_the_pinned_operator_facing_text(self):
        # Assert - pinned as a LITERAL (T77 AC6/D4)
        assert configs_per_param_label(6, 24) == (
            'Configs per horizon-specific parameter: 6 × 4 horizons = 24'
        )

    def test_thousands_separates_both_counts(self):
        # Assert
        assert configs_per_param_label(1234, 4936) == (
            'Configs per horizon-specific parameter: 1,234 × 4 horizons = 4,936'
        )

    def test_takes_its_horizon_count_from_horizon_count(self):
        """The count in the text can never disagree with WEEK_RANGES."""
        # Act
        source = inspect.getsource(configs_per_param_label)

        # Assert
        assert '{HORIZON_COUNT}' in source, (
            "configs_per_param_label restated a horizon-count literal instead of "
            "reading HORIZON_COUNT"
        )


class TestWorkerImportWeight:
    """T77 AC12: every ProcessPoolExecutor worker pays this module's imports."""

    def test_imports_typing_and_nothing_else(self):
        # Act
        imports = [
            line for line in inspect.getsource(horizon_labels).splitlines()
            if line.startswith('import ') or line.startswith('from ')
        ]

        # Assert
        assert imports == ['from typing import Dict, Tuple'], (
            f"horizon_labels gained an import - the accuracy worker pays it: {imports}"
        )

    def test_pulls_in_no_heavyweight_accuracy_module(self):
        """A transitive import of ConfigGenerator would slow every worker start.

        Asserts on the module's actual IMPORT STATEMENTS via AST, not on its source
        text: the module docstring legitimately *names* ConfigGenerator while
        explaining why it is deliberately not imported, so a substring check over
        the source false-fails on the very comment that documents the constraint.
        """
        import ast

        tree = ast.parse(inspect.getsource(horizon_labels))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split('.')[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split('.')[0])

        assert imported <= {'typing'}, (
            f"horizon_labels must import only 'typing' so ProcessPoolExecutor workers "
            f"stay light; found imports of: {sorted(imported)}"
        )
