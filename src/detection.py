"""
Tree Crown Detection & Non-Maximum Suppression (NMS) Module
Handles boundary deduplication and vegetation stratification.
"""

from typing import List, Dict, Any


class SpatialNMS:
    """Consolidates duplicate tree crowns detected across overlapping tile boundaries."""

    @staticmethod
    def calculate_iou(box_a: List[float], box_b: List[float]) -> float:
        """
        Calculates Intersection-over-Union (IoU) between two bounding boxes: [xmin, ymin, xmax, ymax]
        """
        x_left = max(box_a[0], box_b[0])
        y_top = max(box_a[1], box_b[1])
        x_right = min(box_a[2], box_b[2])
        y_bottom = min(box_a[3], box_b[3])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
        box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])

        union_area = box_a_area + box_b_area - intersection_area
        return intersection_area / union_area if union_area > 0 else 0.0

    @classmethod
    def apply_nms(cls, detections: List[Dict[str, Any]], iou_threshold: float = 0.45) -> List[Dict[str, Any]]:
        """
        Suppresses redundant overlapping bounding boxes exceeding iou_threshold.
        """
        if not detections:
            return []

        # Sort detections descending by confidence score
        sorted_dets = sorted(detections, key=lambda d: d.get("confidence", 0.0), reverse=True)
        keep = []

        while sorted_dets:
            current = sorted_dets.pop(0)
            keep.append(current)

            remaining = []
            for det in sorted_dets:
                iou = cls.calculate_iou(current["bbox"], det["bbox"])
                if iou < iou_threshold:
                    remaining.append(det)
            sorted_dets = remaining

        return keep


class VegetationClassifier:
    """Classifies detections into mature shade trees vs median shrubs vs bare soil."""

    @staticmethod
    def stratify_vegetation(crown_area_sqm: float, is_in_median: bool = False) -> str:
        """
        Enforces Rule-AI-002:
        - Crown Area >= 12 sqm in outer verges -> Mature Shade Tree
        - In central median or area < 8 sqm -> Median Shrub / Ornamental
        - Otherwise Ground / Embankment
        """
        if is_in_median or crown_area_sqm < 8.0:
            return "Median Shrub / Ornamental"
        elif crown_area_sqm >= 12.0:
            return "Mature Highway Tree"
        else:
            return "Young Sapling / Semi-Mature"
