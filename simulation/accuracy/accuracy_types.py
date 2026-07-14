from dataclasses import dataclass
from typing import Optional


@dataclass
class RankingMetrics:
    """
    Ranking-based accuracy metrics for a configuration.

    Attributes:
        pairwise_accuracy (Optional[float]): % of pairwise comparisons correct (0.0-1.0), or None if zero valid weeks
        top_5_accuracy (Optional[float]): % overlap in top-5 predictions (0.0-1.0), or None if zero valid weeks
        top_10_accuracy (Optional[float]): % overlap in top-10 predictions (0.0-1.0), or None if zero valid weeks
        top_20_accuracy (Optional[float]): % overlap in top-20 predictions (0.0-1.0), or None if zero valid weeks
        spearman_correlation (Optional[float]): Rank correlation coefficient (-1.0 to +1.0), or None if zero valid weeks
    """
    pairwise_accuracy: Optional[float]
    top_5_accuracy: Optional[float]
    top_10_accuracy: Optional[float]
    top_20_accuracy: Optional[float]
    spearman_correlation: Optional[float]
