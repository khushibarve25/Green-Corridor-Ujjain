"""
Corridor Segmentation & Spatial Canopy Analytics Module
Discretizes the 45-55 km highway into 500m linear intervals and computes canopy metrics.
"""

from typing import Dict, Any, List


class HighwaySegmentationEngine:
    """Computes canopy coverage, tree density, and shade gaps per 500m segment."""

    CORRIDOR_WIDTH_M = 70.0
    SEGMENT_LENGTH_M = 500.0
    SEGMENT_TOTAL_AREA_SQM = CORRIDOR_WIDTH_M * SEGMENT_LENGTH_M # 35,000 sqm (3.5 ha)

    @classmethod
    def compute_canopy_percentage(cls, total_crown_area_sqm: float) -> float:
        """
        Computes Canopy Coverage Percentage: (Sum of Crown Areas / 35,000 sqm) * 100
        """
        cov = (total_crown_area_sqm / cls.SEGMENT_TOTAL_AREA_SQM) * 100.0
        return round(min(100.0, max(0.0, cov)), 1)

    @staticmethod
    def classify_shade_zone(canopy_pct: float) -> Dict[str, Any]:
        """
        Classifies segment into High Shade vs Moderate vs Critical Gap.
        """
        if canopy_pct >= 25.0:
            return {
                "classification": "High Shade (सुरक्षित छाया)",
                "priority_rank": 3,
                "heat_risk_index": round(max(0.1, 1.0 - (canopy_pct / 35.0)), 2),
                "is_critical_gap": False
            }
        elif canopy_pct >= 10.0:
            return {
                "classification": "Moderate Shade (मध्यम छाया)",
                "priority_rank": 2,
                "heat_risk_index": round(0.40 + (25.0 - canopy_pct) * 0.02, 2),
                "is_critical_gap": False
            }
        else:
            return {
                "classification": "Critical Shade Gap (अत्यधिक धूप क्षेत्र)",
                "priority_rank": 1,
                "heat_risk_index": round(min(1.0, 0.70 + (10.0 - canopy_pct) * 0.03), 2),
                "is_critical_gap": True
            }

    @staticmethod
    def estimate_carbon_stock(tree_count: int, avg_crown_area_sqm: float = 28.0) -> float:
        """
        Exploratory allometric estimate of carbon stock in tonnes of Carbon (tC).
        Biomass (kg) approx = a * (Crown Area)^b
        """
        # Average Malwa mature tree ~180-220 kg carbon
        return round(tree_count * 0.18, 1)
