"""
Mock Dataset Generator for GreenCorridor Ujjain
Generates realistic drone top-view imagery with EXIF metadata and georeferenced spatial layers.
Corridor: Ujjain to Indore Highway (SH-27)
"""

import os
import json
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# Corridor coordinates (Ujjain Zero Point towards Sanwer/Indore)
# Ujjain start: 23.1765° N, 75.7885° E
# Direction towards Indore: ~165 degrees south-southeast
UJJAIN_LAT = 23.1765
UJJAIN_LNG = 75.7885
INDORE_LAT = 22.7196
INDORE_LNG = 75.8577

# Malwa Native Species pool
SPECIES_POOL = [
    {"name": "Azadirachta indica", "common": "Neem / नीम", "type": "Dense Broadleaf", "native": True, "cooling_score": 0.95},
    {"name": "Ficus religiosa", "common": "Peepal / पीपल", "type": "Spreading Canopy", "native": True, "cooling_score": 0.98},
    {"name": "Ficus benghalensis", "common": "Banyan / बरगद", "type": "Spreading Canopy", "native": True, "cooling_score": 0.99},
    {"name": "Millettia pinnata", "common": "Karanj / करंज", "type": "Dense Broadleaf", "native": True, "cooling_score": 0.88},
    {"name": "Syzygium cumini", "common": "Jamun / जामुन", "type": "Dense Broadleaf", "native": True, "cooling_score": 0.90},
    {"name": "Cassia fistula", "common": "Amaltas / अमलतास", "type": "Sparse Deciduous", "native": True, "cooling_score": 0.75},
    {"name": "Phoenix sylvestris", "common": "Khajoor / खजूर", "type": "Columnar Palm", "native": True, "cooling_score": 0.40},
    {"name": "Eucalyptus globulus", "common": "Nilgiri / यूकेलिप्टस", "type": "Columnar Tall", "native": False, "cooling_score": 0.50}
]

SHRUB_POOL = [
    {"name": "Bougainvillea spectabilis", "common": "Bougainvillea / बोगनवेलिया", "type": "Median Shrub"},
    {"name": "Nerium oleander", "common": "Kaner / कनेर", "type": "Median Shrub"},
    {"name": "Tecoma stans", "common": "Yellow Bells / पीली टिकोमा", "type": "Median Shrub"}
]

AMENITY_TEMPLATES = [
    {"type": "water", "name_en": "Simhastha Seva Pyaau Booth", "name_hi": "सिंहस्थ सेवा शीतल जल प्याऊ", "icon": "droplet"},
    {"type": "medical", "name_en": "Emergency First Aid Camp", "name_hi": "प्राथमिक चिकित्सा एवं ओआरएस केंद्र", "icon": "cross"},
    {"type": "shade_hub", "name_en": "Mahakal Chhaya Rest Shed", "name_hi": "महाकाल छाया एवं विश्राम स्थल", "icon": "tent"},
    {"type": "toilet", "name_en": "Public Sanitation Block", "name_hi": "सुलभ जन सुविधा एवं शौचालय", "icon": "bath"},
    {"type": "police", "name_en": "Simhastha Pilgrim Assistance Post", "name_hi": "सिंहस्थ यात्री सहायता एवं पुलिस चौकी", "icon": "shield"}
]


def generate_drone_topview_image(file_path: str, crown_count: int = 12, has_median: bool = True):
    """
    Generates a realistic top-view aerial drone image (640x640)
    showing asphalt lanes, road shoulders, central median, and tree crowns.
    """
    width, height = 640, 640
    img = Image.new("RGB", (width, height), color=(195, 185, 160)) # Malwa agricultural soil
    draw = ImageDraw.Draw(img)

    # 1. Agricultural field textures on sides
    for _ in range(40):
        fx1 = random.randint(0, width)
        fy1 = random.randint(0, height)
        fx2 = fx1 + random.randint(60, 200)
        fy2 = fy1 + random.randint(40, 150)
        shade = random.randint(160, 215)
        draw.rectangle([fx1, fy1, fx2, fy2], fill=(shade - 15, shade, shade - 30))

    # 2. Highway corridor (vertical orientation across image)
    # Total road width ~240 px, centered at x=320
    road_left = 200
    road_right = 440
    road_center = 320

    # Paved and earthen shoulders
    draw.rectangle([road_left - 30, 0, road_left, height], fill=(160, 150, 140)) # Left shoulder
    draw.rectangle([road_right, 0, road_right + 30, height], fill=(160, 150, 140)) # Right shoulder

    # Asphalt lanes (Dark Charcoal)
    draw.rectangle([road_left, 0, road_right, height], fill=(55, 58, 62))

    # White lane dash markings
    for y in range(0, height, 40):
        draw.line([(road_left + 55, y), (road_left + 55, y + 20)], fill=(240, 240, 240), width=2)
        draw.line([(road_right - 55, y), (road_right - 55, y + 20)], fill=(240, 240, 240), width=2)

    # 3. Central Median (18 px wide)
    median_left = road_center - 9
    median_right = road_center + 9
    draw.rectangle([median_left, 0, median_right, height], fill=(75, 85, 70)) # Greenish soil/curb

    # Median Shrubs (Bougainvillea / Nerium)
    if has_median:
        for my in range(25, height, 45):
            if random.random() > 0.2:
                shrub_r = random.randint(6, 9)
                # Pink/magenta or deep green flowering shrub
                shrub_col = random.choice([
                    (180, 45, 90), # Bougainvillea magenta
                    (34, 110, 50), # Deep green
                    (220, 160, 30) # Yellow bells
                ])
                draw.ellipse(
                    [road_center - shrub_r, my - shrub_r, road_center + shrub_r, my + shrub_r],
                    fill=shrub_col,
                    outline=(20, 50, 20)
                )

    # 4. Tree Crowns along road edges (Pedestrian verge and adjoining fields)
    for _ in range(crown_count):
        # Place crowns primarily on roadside verges: x in [40, 160] or x in [460, 580]
        if random.random() < 0.5:
            cx = random.randint(40, road_left - 35)
        else:
            cx = random.randint(road_right + 35, 600)
        cy = random.randint(30, height - 30)

        crown_radius = random.randint(18, 42)
        # Tree shadow (offset slightly northeast, simulating morning/afternoon sun)
        shadow_offset = (12, 10)
        draw.ellipse(
            [cx - crown_radius + shadow_offset[0], cy - crown_radius + shadow_offset[1],
             cx + crown_radius + shadow_offset[0], cy + crown_radius + shadow_offset[1]],
            fill=(40, 40, 35, 120)
        )

        # Crown canopy layers (multi-shade realistic foliage)
        base_green = random.randint(35, 75)
        draw.ellipse(
            [cx - crown_radius, cy - crown_radius, cx + crown_radius, cy + crown_radius],
            fill=(base_green - 15, base_green + 45, base_green - 10),
            outline=(base_green - 25, base_green + 20, base_green - 20),
            width=2
        )
        # Inner crown texture highlight
        inner_r = int(crown_radius * 0.65)
        draw.ellipse(
            [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
            fill=(base_green, base_green + 65, base_green)
        )

    # Subtle blur to simulate aerial camera optics
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    img.save(file_path, "JPEG", quality=92)


def generate_mock_geospatial_corridor():
    """
    Generates synthetic geospatial corridor datasets:
    - Highway Centerline
    - 500m Segments with canopy, gap, and heat stats
    - Detected Tree Crowns
    - Simhastha Amenities
    """
    os.makedirs("dataset/raw_frames", exist_ok=True)
    os.makedirs("dataset/geojson", exist_ok=True)

    # 1. Generate 3 representative drone sample frames
    print("Generating simulated drone orthomosaic sample frames...")
    generate_drone_topview_image("dataset/raw_frames/DJI_UJJ_001_KM01.jpg", crown_count=16, has_median=True)
    generate_drone_topview_image("dataset/raw_frames/DJI_UJJ_002_KM04_GAP.jpg", crown_count=3, has_median=True)
    generate_drone_topview_image("dataset/raw_frames/DJI_UJJ_003_KM08_DENSE.jpg", crown_count=24, has_median=True)

    # 2. Highway alignment: 30 linear segments of 500m each = 15 km pilot corridor
    num_segments = 30
    corridor_coords = []
    segments_features = []
    crowns_features = []
    amenity_features = []

    # Calculate step vector from Ujjain towards Indore
    dlat = (INDORE_LAT - UJJAIN_LAT)
    dlng = (INDORE_LNG - UJJAIN_LNG)
    total_dist_est = math.sqrt(dlat**2 + dlng**2)
    step_lat = (dlat / total_dist_est) * (0.5 / 111.0) # ~500m per step
    step_lng = (dlng / total_dist_est) * (0.5 / 102.0)

    # Perpendicular vector for 70m corridor buffer (approx 35m each side)
    perp_lat = -step_lng * (0.035 / 0.5)
    perp_lng = step_lat * (0.035 / 0.5)

    cur_lat = UJJAIN_LAT
    cur_lng = UJJAIN_LNG
    corridor_coords.append([cur_lng, cur_lat])

    crown_id_counter = 1
    amenity_id_counter = 1

    total_trees_corridor = 0
    total_shrubs_corridor = 0

    print("Synthesizing 500m segments, crown detections, and amenities...")
    for seg_idx in range(num_segments):
        start_km = seg_idx * 0.5
        end_km = (seg_idx + 1) * 0.5
        seg_num = seg_idx + 1

        p1_lat, p1_lng = cur_lat, cur_lng
        next_lat = cur_lat + step_lat + random.uniform(-0.0001, 0.0001)
        next_lng = cur_lng + step_lng + random.uniform(-0.0001, 0.0001)
        p2_lat, p2_lng = next_lat, next_lng
        corridor_coords.append([p2_lng, p2_lat])

        # Polygon footprint for 500m segment (70m wide corridor)
        poly_coords = [
            [p1_lng - perp_lng, p1_lat - perp_lat],
            [p2_lng - perp_lng, p2_lat - perp_lat],
            [p2_lng + perp_lng, p2_lat + perp_lat],
            [p1_lng + perp_lng, p1_lat + perp_lat],
            [p1_lng - perp_lng, p1_lat - perp_lat]
        ]

        # Vary canopy density intentionally to simulate real highway conditions:
        # Some stretches are critical gaps (newly widened, < 8%), some are moderately shaded, some mature
        if seg_num in [4, 5, 8, 12, 13, 14, 21, 22]: # Severe gaps
            target_canopy = random.uniform(2.5, 7.8)
            num_trees = random.randint(4, 18)
        elif seg_num in [1, 2, 9, 10, 18, 19, 28]: # Good shade
            target_canopy = random.uniform(22.0, 36.5)
            num_trees = random.randint(45, 95)
        else: # Moderate
            target_canopy = random.uniform(10.5, 20.0)
            num_trees = random.randint(22, 44)

        num_shrubs = random.randint(30, 80)
        total_trees_corridor += num_trees
        total_shrubs_corridor += num_shrubs

        # Determine classification
        if target_canopy >= 25.0:
            shade_class = "High Shade (सुरक्षित छाया)"
            heat_risk = round(1.0 - (target_canopy / 35.0), 2)
            priority_rank = 3 # Low priority for new planting
        elif target_canopy >= 10.0:
            shade_class = "Moderate Shade (मध्यम छाया)"
            heat_risk = round(0.45 + (20.0 - target_canopy) * 0.02, 2)
            priority_rank = 2
        else:
            shade_class = "Critical Shade Gap (अत्यधिक धूप क्षेत्र)"
            heat_risk = round(0.75 + (8.0 - target_canopy) * 0.03, 2)
            priority_rank = 1 # Urgent planting priority

        # Generate rule-based recommendation
        slots_available = max(0, int((25.0 - target_canopy) * 5.2))
        if priority_rank == 1:
            rec_text = f"अत्यधिक धूप (Canopy {target_canopy:.1f}%). Plant {slots_available} native trees (Neem, Karanj, Jamun). Retain low median shrubs."
            rec_species = ["Azadirachta indica (Neem)", "Millettia pinnata (Karanj)", "Syzygium cumini (Jamun)"]
        elif priority_rank == 2:
            rec_text = f"मध्यम छाया (Canopy {target_canopy:.1f}%). Plant {slots_available} shade trees. Diversify with Peepal and Banyan at rest points."
            rec_species = ["Ficus religiosa (Peepal)", "Millettia pinnata (Karanj)"]
        else:
            rec_text = f"पर्याप्त हरित आवरण (Canopy {target_canopy:.1f}%). Green corridor established. Focus on canopy pruning and soil mulch."
            rec_species = ["Maintenance & Protection"]

        # Synthesize individual tree crowns in this segment
        segment_species_counts = {}
        for _ in range(num_trees):
            sp = random.choice(SPECIES_POOL)
            segment_species_counts[sp["name"]] = segment_species_counts.get(sp["name"], 0) + 1

            # Interpolate position along segment
            t = random.random()
            side = random.choice([-1, 1])
            offset_dist = random.uniform(0.35, 0.95)

            c_lat = (p1_lat + t * (p2_lat - p1_lat)) + side * perp_lat * offset_dist
            c_lng = (p1_lng + t * (p2_lng - p1_lng)) + side * perp_lng * offset_dist

            c_diam = round(random.uniform(4.5, 12.5), 1)
            c_area = round(math.pi * ((c_diam / 2) ** 2), 1)

            # Generate crown polygon (circle approximation)
            pts = 8
            crown_poly = []
            for a in range(pts):
                angle = (2 * math.pi / pts) * a
                r_deg = (c_diam / 2.0) / 111000.0
                crown_poly.append([
                    round(c_lng + r_deg * math.cos(angle) * 1.1, 6),
                    round(c_lat + r_deg * math.sin(angle), 6)
                ])
            crown_poly.append(crown_poly[0])

            crowns_features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [crown_poly]
                },
                "properties": {
                    "crown_id": f"CRW-{crown_id_counter:05d}",
                    "segment_id": seg_num,
                    "species": sp["name"],
                    "common_name": sp["common"],
                    "morphotype": sp["type"],
                    "diameter_m": c_diam,
                    "crown_area_sqm": c_area,
                    "confidence": round(random.uniform(0.84, 0.98), 2),
                    "is_native": sp["native"],
                    "centroid": [round(c_lng, 6), round(c_lat, 6)]
                }
            })
            crown_id_counter += 1

        # Check Santamour 10% species dominance
        dominant_species = None
        max_share = 0.0
        for sp_name, cnt in segment_species_counts.items():
            share = (cnt / num_trees) * 100
            if share > max_share:
                max_share = share
                dominant_species = sp_name
        diversity_alert = max_share > 30.0

        segments_features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [poly_coords]
            },
            "properties": {
                "segment_id": seg_num,
                "chainage": f"KM {start_km:.1f} - {end_km:.1f}",
                "start_km": start_km,
                "end_km": end_km,
                "canopy_percentage": round(target_canopy, 1),
                "tree_count": num_trees,
                "median_shrub_count": num_shrubs,
                "shade_classification": shade_class,
                "heat_risk_index": min(1.0, max(0.1, heat_risk)),
                "planting_priority": priority_rank,
                "slots_available": slots_available,
                "recommended_species": rec_species,
                "recommendation_text": rec_text,
                "dominant_species": dominant_species,
                "dominant_share_pct": round(max_share, 1),
                "diversity_alert": diversity_alert,
                "carbon_stock_tc": round(num_trees * 0.18, 1) # ~180 kg C per tree average
            }
        })

        # Add amenities (every 2-3 segments)
        if seg_num % 2 == 1:
            amenity_template = random.choice(AMENITY_TEMPLATES)
            amenity_side = random.choice([-0.4, 0.4])
            am_lat = (p1_lat + p2_lat) / 2 + amenity_side * perp_lat
            am_lng = (p1_lng + p2_lng) / 2 + amenity_side * perp_lng

            amenity_features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(am_lng, 6), round(am_lat, 6)]
                },
                "properties": {
                    "amenity_id": f"AMN-{amenity_id_counter:03d}",
                    "segment_id": seg_num,
                    "chainage": f"KM {start_km:.1f}",
                    "type": amenity_template["type"],
                    "icon": amenity_template["icon"],
                    "name_en": f"{amenity_template['name_en']} #{amenity_id_counter}",
                    "name_hi": f"{amenity_template['name_hi']} #{amenity_id_counter}",
                    "status": "Operational (सक्रिय 24x7)",
                    "water_available": True,
                    "shade_available": priority_rank != 1
                }
            })
            amenity_id_counter += 1

        cur_lat = next_lat
        cur_lng = next_lng

    # 3. Write out GeoJSON files
    centerline_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": corridor_coords
            },
            "properties": {
                "corridor_name": "Ujjain - Indore 6-Lane Highway (SH-27)",
                "total_segments": num_segments,
                "pilot_length_km": num_segments * 0.5,
                "target_event": "Simhastha Kumbh Mela 2028"
            }
        }]
    }

    segments_geojson = {
        "type": "FeatureCollection",
        "features": segments_features
    }

    crowns_geojson = {
        "type": "FeatureCollection",
        "features": crowns_features
    }

    amenities_geojson = {
        "type": "FeatureCollection",
        "features": amenity_features
    }

    with open("dataset/geojson/highway_centerline.geojson", "w", encoding="utf-8") as f:
        json.dump(centerline_geojson, f, indent=2)

    with open("dataset/geojson/highway_segments_500m.geojson", "w", encoding="utf-8") as f:
        json.dump(segments_geojson, f, indent=2)

    with open("dataset/geojson/detected_tree_crowns.geojson", "w", encoding="utf-8") as f:
        json.dump(crowns_geojson, f, indent=2)

    with open("dataset/geojson/simhastha_amenities.geojson", "w", encoding="utf-8") as f:
        json.dump(amenities_geojson, f, indent=2)

    summary_stats = {
        "corridor_name": "Ujjain–Indore Highway (SH-27)",
        "pilot_length_km": num_segments * 0.5,
        "total_segments": num_segments,
        "total_trees_detected": total_trees_corridor,
        "total_median_shrubs": total_shrubs_corridor,
        "critical_gaps_count": sum(1 for s in segments_features if s["properties"]["planting_priority"] == 1),
        "high_shade_count": sum(1 for s in segments_features if s["properties"]["planting_priority"] == 3),
        "avg_canopy_coverage_pct": round(sum(s["properties"]["canopy_percentage"] for s in segments_features) / num_segments, 1),
        "amenity_points_count": len(amenity_features),
        "target_simhastha_year": 2028
    }

    with open("dataset/geojson/corridor_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_stats, f, indent=2)

    print(f"Mock dataset generated successfully!")
    print(f"Total Segments: {num_segments} (Length: {num_segments * 0.5} km)")
    print(f"Total Trees Synthesized: {total_trees_corridor}")
    print(f"Total Median Shrubs: {total_shrubs_corridor}")
    print(f"Critical Gaps (<8% Canopy): {summary_stats['critical_gaps_count']}")
    print(f"Simhastha Amenities Mapped: {len(amenity_features)}")


if __name__ == "__main__":
    generate_mock_geospatial_corridor()
