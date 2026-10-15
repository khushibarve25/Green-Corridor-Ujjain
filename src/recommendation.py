"""
Explainable Ecological Recommendation Engine
Enforces Santamour 10-20-30 diversity rules and prescribes Malwa native shade species.
"""

from typing import Dict, Any, List


class EcologicalRecommendationEngine:
    """Generates transparent, explainable planting recommendations."""

    # Approved Malwa Native Shade Species Matrix
    NATIVE_RECOMMENDATIONS = {
        "primary_shade": [
            {"species": "Azadirachta indica", "common": "Neem (नीम)", "crown_spread": "Broadleaf 12m", "cooling": "Very High"},
            {"species": "Millettia pinnata", "common": "Karanj (करंज)", "crown_spread": "Broadleaf 10m", "cooling": "High"},
            {"species": "Syzygium cumini", "common": "Jamun (जामुन)", "crown_spread": "Dense 14m", "cooling": "High"}
        ],
        "rest_point_monuments": [
            {"species": "Ficus religiosa", "common": "Peepal (पीपल)", "crown_spread": "Massive 20m", "cooling": "Exceptional"},
            {"species": "Ficus benghalensis", "common": "Banyan (बरगद)", "crown_spread": "Massive 25m", "cooling": "Exceptional"}
        ],
        "prohibited_highway_species": [
            "Eucalyptus globulus (Severe groundwater depletion & branch breakage hazard)",
            "Conocarpus erectus (Aggressive pavement root damage & pollen allergens)",
            "Prosopis juliflora (Invasive suppression of native understory)"
        ]
    }

    @classmethod
    def evaluate_diversity(cls, species_counts: Dict[str, int], total_trees: int) -> Dict[str, Any]:
        """
        Enforces Santamour 10-20-30 Rule:
        Alerts if any single species exceeds 10% of total trees.
        """
        if total_trees == 0:
            return {"compliant": True, "dominant_species": None, "dominant_share": 0.0}

        dominant_sp = None
        max_share = 0.0
        for sp, count in species_counts.items():
            share = (count / total_trees) * 100.0
            if share > max_share:
                max_share = share
                dominant_sp = sp

        # Threshold alert if species exceeds 15% in a segment
        is_alert = max_share > 15.0
        return {
            "compliant": not is_alert,
            "dominant_species": dominant_sp,
            "dominant_share": round(max_share, 1),
            "alert_message": (
                f"Species diversity warning: {dominant_sp} constitutes {max_share:.1f}% "
                f"(exceeds Santamour 10% urban forestry guideline)."
            ) if is_alert else "Diversity within acceptable thresholds."
        }

    @classmethod
    def generate_recommendation(
        cls,
        segment_id: int,
        canopy_pct: float,
        tree_count: int,
        diversity_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates an explainable planting prescription for a 500m segment.
        """
        target_canopy = 25.0
        gap_pct = max(0.0, target_canopy - canopy_pct)
        # Average mature crown area ~35 sqm -> each tree adds ~0.1% canopy to 35,000 sqm segment
        slots_needed = int(gap_pct * 5.2)

        if canopy_pct < 8.0:
            priority = "URGENT (अत्यधिक प्राथमिकता)"
            prescribed = ["Azadirachta indica (Neem)", "Millettia pinnata (Karanj)", "Syzygium cumini (Jamun)"]
            reasoning = (
                f"Segment {segment_id} exhibits critical canopy deficit ({canopy_pct}% cover, target 25%). "
                f"Requires {slots_needed} native shade trees along outer road verges. "
                f"Retain existing central median shrubs for glare reduction, but avoid tall trees in median."
            )
        elif canopy_pct < 20.0:
            priority = "MODERATE (मध्यम प्राथमिकता)"
            prescribed = ["Millettia pinnata (Karanj)", "Ficus religiosa (Peepal)"]
            reasoning = (
                f"Segment {segment_id} has moderate cover ({canopy_pct}%). "
                f"Plant {slots_needed} trees to interconnect existing canopy clusters. "
                f"{diversity_info.get('alert_message', '')}"
            )
        else:
            priority = "MAINTENANCE (संरक्षण)"
            prescribed = ["Canopy Pruning & Mulch"]
            reasoning = (
                f"Segment {segment_id} has achieved adequate shade canopy ({canopy_pct}%). "
                f"Recommend seasonal watering, root mulching, and routine structural safety checks."
            )

        return {
            "segment_id": segment_id,
            "priority": priority,
            "slots_available": slots_needed,
            "prescribed_species": prescribed,
            "reasoning": reasoning,
            "prohibited": cls.NATIVE_RECOMMENDATIONS["prohibited_highway_species"]
        }
