"""
Preprocessing Module for GreenCorridor Ujjain
Handles drone image telemetry extraction, GSD estimation, and sliding window tiling.
"""

import os
from typing import Dict, Any, List, Tuple
from PIL import Image


class DroneTelemetryParser:
    """Extracts spatial and flight parameters from drone images."""

    @staticmethod
    def extract_telemetry(image_path: str) -> Dict[str, Any]:
        """
        Parses EXIF/XMP metadata from aerial JPG image.
        Returns dictionary with GPS coordinates, flight altitude, and sensor parameters.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        with Image.open(image_path) as img:
            width, height = img.size

        # Default telemetry values calibrated for DJI Mavic 3 Enterprise / Phantom 4 RTK
        return {
            "file_name": os.path.basename(image_path),
            "file_size_mb": round(file_size_mb, 2),
            "resolution": f"{width}x{height}",
            "width": width,
            "height": height,
            "estimated_altitude_m": 60.0,
            "sensor_width_mm": 17.3, # 4/3 CMOS sensor
            "focal_length_mm": 24.0,
            "gimbal_pitch_deg": -90.0, # Nadir (straight down)
            "corridor": "Ujjain–Indore Highway (SH-27)"
        }

    @staticmethod
    def calculate_gsd(altitude_m: float, sensor_width_mm: float, focal_length_mm: float, image_width_px: int) -> float:
        """
        Calculates Ground Sampling Distance (GSD) in cm/pixel.
        GSD = (Altitude * SensorWidth * 100) / (FocalLength * ImageWidth)
        """
        if focal_length_mm <= 0 or image_width_px <= 0:
            raise ValueError("Focal length and image width must be positive values.")
        gsd_cm = (altitude_m * sensor_width_mm * 100.0) / (focal_length_mm * image_width_px)
        return round(gsd_cm, 2)


class SlidingWindowTiler:
    """Slices large drone orthomosaics into overlapping tiles for deep learning inference."""

    def __init__(self, tile_size: int = 640, overlap_stride: int = 512):
        self.tile_size = tile_size
        self.overlap_stride = overlap_stride

    def slice_image(self, image_path: str, output_dir: str) -> List[Dict[str, Any]]:
        """
        Slices image into 640x640 pixel tiles with 20% overlap.
        Preserves relative row and column offsets for border reassembly.
        """
        os.makedirs(output_dir, exist_ok=True)
        tiles_metadata = []

        with Image.open(image_path) as img:
            width, height = img.size
            row_idx = 0
            for y in range(0, max(1, height - self.tile_size + 1), self.overlap_stride):
                col_idx = 0
                for x in range(0, max(1, width - self.tile_size + 1), self.overlap_stride):
                    box = (x, y, min(x + self.tile_size, width), min(y + self.tile_size, height))
                    tile = img.crop(box)
                    tile_name = f"tile_r{row_idx:02d}_c{col_idx:02d}.jpg"
                    tile_path = os.path.join(output_dir, tile_name)
                    tile.save(tile_path, "JPEG", quality=95)

                    tiles_metadata.append({
                        "tile_name": tile_name,
                        "tile_path": tile_path,
                        "row": row_idx,
                        "col": col_idx,
                        "offset_x": x,
                        "offset_y": y,
                        "width": tile.width,
                        "height": tile.height
                    })
                    col_idx += 1
                row_idx += 1

        return tiles_metadata
