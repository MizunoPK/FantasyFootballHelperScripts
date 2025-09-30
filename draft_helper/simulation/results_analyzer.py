"""
Results analysis and report generation for draft simulations.

Analyzes simulation results and generates comprehensive reports with optimal configurations.
"""

import statistics
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import datetime
import os

from config_optimizer import ConfigResult

@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics for a configuration"""
    win_percentage: float
    total_points: float
    points_per_game: float
    consistency_score: float
    avg_ranking: float
    win_rate_vs_conservative: float
    win_rate_vs_aggressive: float
    win_rate_vs_positional: float
    win_rate_vs_value: float
    win_rate_vs_draft_helper: float

class ResultsAnalyzer:
    """Analyzes simulation results and generates reports"""

    def __init__(self):
        self.analysis_results: List[ConfigResult] = []

    def analyze_all_results(self, config_results: List[ConfigResult]) -> Dict[str, Any]:
        """Perform comprehensive analysis of all configuration results"""

        self.analysis_results = config_results

        analysis = {
            'optimal_config': self._find_optimal_config(),
            'top_10_configs': self._get_top_configs(10),
            'parameter_analysis': self._analyze_parameter_effects(),
            'strategy_comparison': self._analyze_strategy_effectiveness(),
            'performance_distribution': self._analyze_performance_distribution(),
            'statistical_summary': self._generate_statistical_summary(),
            'analysis_metadata': self._generate_metadata()
        }

        return analysis

    def _find_optimal_config(self) -> Optional[Dict[str, Any]]:
        """Find the single best performing configuration"""

        if not self.analysis_results:
            return None

        # Sort by win percentage first, then by total points
        best_result = max(self.analysis_results,
                         key=lambda x: (x.avg_win_percentage, x.avg_total_points))

        return {
            'config_params': best_result.config_params,
            'performance': {
                'win_percentage': best_result.avg_win_percentage,
                'total_points': best_result.avg_total_points,
                'points_per_game': best_result.avg_points_per_game,
                'consistency': best_result.avg_consistency,
                'simulations_run': best_result.simulations_run,
                'avg_ranking': statistics.mean(best_result.user_team_rankings) if best_result.user_team_rankings else 0
            }
        }

    def _get_top_configs(self, count: int) -> List[Dict[str, Any]]:
        """Get top N performing configurations"""

        sorted_results = sorted(self.analysis_results,
                              key=lambda x: (x.avg_win_percentage, x.avg_total_points),
                              reverse=True)

        top_configs = []
        for i, result in enumerate(sorted_results[:count]):
            config_info = {
                'rank': i + 1,
                'config_params': result.config_params,
                'win_percentage': result.avg_win_percentage,
                'total_points': result.avg_total_points,
                'points_per_game': result.avg_points_per_game,
                'consistency': result.avg_consistency,
                'avg_ranking': statistics.mean(result.user_team_rankings) if result.user_team_rankings else 0
            }
            top_configs.append(config_info)

        return top_configs

    def _analyze_parameter_effects(self) -> Dict[str, Dict[str, float]]:
        """Analyze the effect of different parameter values on performance"""

        parameter_effects = {}

        # Group results by parameter values
        param_groups = {}
        for result in self.analysis_results:
            for param_name, param_value in result.config_params.items():
                if param_name == 'DRAFT_ORDER':  # Skip complex object
                    continue

                if param_name not in param_groups:
                    param_groups[param_name] = {}

                if param_value not in param_groups[param_name]:
                    param_groups[param_name][param_value] = []

                param_groups[param_name][param_value].append(result)

        # Calculate average performance for each parameter value
        for param_name, value_groups in param_groups.items():
            parameter_effects[param_name] = {}

            for param_value, results in value_groups.items():
                avg_win_pct = statistics.mean([r.avg_win_percentage for r in results])
                parameter_effects[param_name][param_value] = avg_win_pct

        return parameter_effects

    def _analyze_strategy_effectiveness(self) -> Dict[str, float]:
        """Analyze effectiveness against different opponent strategies"""

        # This would require detailed matchup data from simulations
        # For now, return placeholder analysis
        strategy_analysis = {
            'vs_conservative_teams': 0.0,
            'vs_aggressive_teams': 0.0,
            'vs_positional_teams': 0.0,
            'vs_value_teams': 0.0,
            'vs_draft_helper_teams': 0.0
        }

        return strategy_analysis

    def _analyze_performance_distribution(self) -> Dict[str, Any]:
        """Analyze the distribution of performance metrics"""

        if not self.analysis_results:
            return {}

        win_percentages = [r.avg_win_percentage for r in self.analysis_results]
        total_points = [r.avg_total_points for r in self.analysis_results]
        consistencies = [r.avg_consistency for r in self.analysis_results]

        distribution = {
            'win_percentage': {
                'mean': statistics.mean(win_percentages),
                'median': statistics.median(win_percentages),
                'std_dev': statistics.stdev(win_percentages) if len(win_percentages) > 1 else 0,
                'min': min(win_percentages),
                'max': max(win_percentages),
                'range': max(win_percentages) - min(win_percentages)
            },
            'total_points': {
                'mean': statistics.mean(total_points),
                'median': statistics.median(total_points),
                'std_dev': statistics.stdev(total_points) if len(total_points) > 1 else 0,
                'min': min(total_points),
                'max': max(total_points),
                'range': max(total_points) - min(total_points)
            },
            'consistency': {
                'mean': statistics.mean(consistencies),
                'median': statistics.median(consistencies),
                'std_dev': statistics.stdev(consistencies) if len(consistencies) > 1 else 0,
                'min': min(consistencies),
                'max': max(consistencies),
                'range': max(consistencies) - min(consistencies)
            }
        }

        return distribution

    def _generate_statistical_summary(self) -> Dict[str, Any]:
        """Generate statistical summary of results"""

        if not self.analysis_results:
            return {}

        total_configs_tested = len(self.analysis_results)
        total_simulations = sum(r.simulations_run for r in self.analysis_results)

        # Find best and worst performers
        best_config = max(self.analysis_results, key=lambda x: x.avg_win_percentage)
        worst_config = min(self.analysis_results, key=lambda x: x.avg_win_percentage)

        performance_improvement = best_config.avg_win_percentage - worst_config.avg_win_percentage

        summary = {
            'total_configurations_tested': total_configs_tested,
            'total_simulations_run': total_simulations,
            'best_win_percentage': best_config.avg_win_percentage,
            'worst_win_percentage': worst_config.avg_win_percentage,
            'performance_improvement_range': performance_improvement,
            'configs_above_50_percent': len([r for r in self.analysis_results if r.avg_win_percentage > 0.5]),
            'configs_above_60_percent': len([r for r in self.analysis_results if r.avg_win_percentage > 0.6]),
            'configs_above_70_percent': len([r for r in self.analysis_results if r.avg_win_percentage > 0.7])
        }

        return summary

    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate analysis metadata"""

        metadata = {
            'analysis_timestamp': datetime.datetime.now().isoformat(),
            'total_results_analyzed': len(self.analysis_results),
            'analysis_version': '1.0.0'
        }

        return metadata

    def generate_results_report(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive results report in Markdown format"""

        report_lines = []

        # Header
        report_lines.append("# Draft Simulation Results")
        report_lines.append("")
        report_lines.append(f"**Analysis Date**: {analysis['analysis_metadata']['analysis_timestamp']}")
        report_lines.append(f"**Total Configurations Tested**: {analysis['statistical_summary']['total_configurations_tested']}")
        report_lines.append(f"**Total Simulations Run**: {analysis['statistical_summary']['total_simulations_run']}")
        report_lines.append("")

        # Optimal Configuration
        if analysis['optimal_config']:
            optimal = analysis['optimal_config']
            report_lines.append("## Optimal Configuration")
            report_lines.append("")
            report_lines.append("**Configuration Parameters:**")

            for param, value in optimal['config_params'].items():
                if param != 'DRAFT_ORDER':  # Skip complex object
                    report_lines.append(f"- `{param}`: {value}")

            report_lines.append("")
            report_lines.append("**Performance Metrics:**")
            perf = optimal['performance']
            report_lines.append(f"- **Win Percentage**: {perf['win_percentage']:.1%}")
            report_lines.append(f"- **Average Total Points**: {perf['total_points']:.1f}")
            report_lines.append(f"- **Points Per Game**: {perf['points_per_game']:.1f}")
            report_lines.append(f"- **Score Consistency**: {perf['consistency']:.1f}")
            report_lines.append(f"- **Average Ranking**: {perf['avg_ranking']:.1f}")
            report_lines.append(f"- **Simulations**: {perf['simulations_run']}")
            report_lines.append("")

        # Top 10 Configurations
        report_lines.append("## Top 10 Configurations")
        report_lines.append("")
        report_lines.append("| Rank | Win % | Total Pts | PPG | Consistency | Key Parameters |")
        report_lines.append("|------|-------|-----------|-----|-------------|----------------|")

        for config in analysis['top_10_configs']:
            key_params = []
            for param, value in config['config_params'].items():
                # DEPRECATED: POS_NEEDED_SCORE no longer used
                if param in ['INJURY_PENALTIES_MEDIUM', 'INJURY_PENALTIES_HIGH']:
                    key_params.append(f"{param.split('_')[-1]}={value}")

            key_params_str = ", ".join(key_params[:3])  # Show first 3
            report_lines.append(f"| {config['rank']} | {config['win_percentage']:.1%} | "
                              f"{config['total_points']:.0f} | {config['points_per_game']:.1f} | "
                              f"{config['consistency']:.1f} | {key_params_str} |")

        report_lines.append("")

        # Parameter Analysis
        report_lines.append("## Parameter Analysis")
        report_lines.append("")

        for param_name, param_effects in analysis['parameter_analysis'].items():
            if param_name == 'DRAFT_ORDER':
                continue

            report_lines.append(f"### {param_name}")
            report_lines.append("")

            # Sort by performance
            sorted_effects = sorted(param_effects.items(), key=lambda x: x[1], reverse=True)

            for value, win_rate in sorted_effects:
                report_lines.append(f"- **{value}**: {win_rate:.1%} win rate")

            report_lines.append("")

        # Performance Distribution
        if analysis['performance_distribution']:
            report_lines.append("## Performance Distribution")
            report_lines.append("")

            dist = analysis['performance_distribution']
            report_lines.append("### Win Percentage Statistics")
            report_lines.append(f"- **Mean**: {dist['win_percentage']['mean']:.1%}")
            report_lines.append(f"- **Median**: {dist['win_percentage']['median']:.1%}")
            report_lines.append(f"- **Range**: {dist['win_percentage']['min']:.1%} - {dist['win_percentage']['max']:.1%}")
            report_lines.append(f"- **Standard Deviation**: {dist['win_percentage']['std_dev']:.3f}")
            report_lines.append("")

        # Statistical Summary
        report_lines.append("## Statistical Summary")
        report_lines.append("")
        stats = analysis['statistical_summary']
        report_lines.append(f"- **Performance Improvement Range**: {stats['performance_improvement_range']:.1%}")
        report_lines.append(f"- **Configurations Above 50% Win Rate**: {stats['configs_above_50_percent']}")
        report_lines.append(f"- **Configurations Above 60% Win Rate**: {stats['configs_above_60_percent']}")
        report_lines.append(f"- **Configurations Above 70% Win Rate**: {stats['configs_above_70_percent']}")
        report_lines.append("")

        # Key Insights
        report_lines.append("## Key Insights")
        report_lines.append("")
        report_lines.append("1. **Configuration optimization can significantly improve draft performance**")

        if analysis['optimal_config']:
            improvement = stats['performance_improvement_range']
            report_lines.append(f"2. **Best configuration achieved {improvement:.1%} better win rate than worst**")

        if stats['configs_above_60_percent'] > 0:
            pct = stats['configs_above_60_percent'] / stats['total_configurations_tested'] * 100
            report_lines.append(f"3. **{pct:.1f}% of configurations achieved >60% win rate**")

        report_lines.append("4. **Parameter tuning has measurable impact on draft success**")
        report_lines.append("")

        # Recommendations
        report_lines.append("## Recommendations")
        report_lines.append("")
        if analysis['optimal_config']:
            report_lines.append("**Use the optimal configuration parameters identified above for best results.**")
            report_lines.append("")
            report_lines.append("**Key parameter adjustments:**")

            optimal_params = analysis['optimal_config']['config_params']
            for param, value in optimal_params.items():
                if param != 'DRAFT_ORDER':
                    report_lines.append(f"- Set `{param}` to `{value}`")

        report_lines.append("")
        report_lines.append("**Monitor these high-impact parameters:**")

        # Find parameters with highest variance in performance
        high_impact_params = []
        for param_name, param_effects in analysis['parameter_analysis'].items():
            if param_name == 'DRAFT_ORDER':
                continue
            values = list(param_effects.values())
            if len(values) > 1:
                param_range = max(values) - min(values)
                high_impact_params.append((param_name, param_range))

        high_impact_params.sort(key=lambda x: x[1], reverse=True)
        for param_name, impact in high_impact_params[:3]:
            report_lines.append(f"- `{param_name}` (impact range: {impact:.1%})")

        report_lines.append("")

        return "\n".join(report_lines)

    def save_results_to_file(self, analysis: Dict[str, Any], file_path: str) -> None:
        """Save analysis results to markdown file"""

        report_content = self.generate_results_report(analysis)

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Results saved to: {file_path}")