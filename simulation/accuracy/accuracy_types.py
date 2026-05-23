from dataclasses import dataclass


@dataclass
class RankingMetrics:
    """
    Ranking-based accuracy metrics for a configuration.

    Attributes:
        pairwise_accuracy (float): % of pairwise comparisons correct (0.0-1.0)
        top_5_accuracy (float): % overlap in top-5 predictions (0.0-1.0)
        top_10_accuracy (float): % overlap in top-10 predictions (0.0-1.0)
        top_20_accuracy (float): % overlap in top-20 predictions (0.0-1.0)
        spearman_correlation (float): Rank correlation coefficient (-1.0 to +1.0)
    """
    pairwise_accuracy: float
    top_5_accuracy: float
    top_10_accuracy: float
    top_20_accuracy: float
    spearman_correlation: float
