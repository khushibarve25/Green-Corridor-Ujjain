"""
FastAPI Backend Server for GreenCorridor Ujjain
Serves geospatial GeoJSON endpoints, corridor analytics, and mounts the interactive web client.
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.preprocessing import DroneTelemetryParser, SlidingWindowTiler
from src.recommendation import EcologicalRecommendationEngine

app = FastAPI(
    title="GreenCorridor Ujjain API",
    description="AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for Simhastha 2028 (SH-27)",
    version="1.0.0"
)

# Enable CORS for local cross-origin development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEOJSON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset", "geojson")
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")


def load_geojson_file(filename: str):
    file_path = os.path.join(GEOJSON_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Dataset file {filename} not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
async def root():
    """Serves the main dual-perspective web interface."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "GreenCorridor Ujjain API running"}


@app.get("/api/v1/corridor/segments")
async def get_segments():
    """Returns 500m discretized corridor segments with canopy and shade statistics."""
    return JSONResponse(content=load_geojson_file("highway_segments_500m.geojson"))


@app.get("/api/v1/crowns")
async def get_crowns(limit: int = 1500):
    """Returns individual detected tree crowns with polygons, species, and confidence."""
    data = load_geojson_file("detected_tree_crowns.geojson")
    if limit and len(data.get("features", [])) > limit:
        data["features"] = data["features"][:limit]
    return JSONResponse(content=data)


@app.get("/api/v1/pilgrim/amenities")
async def get_amenities():
    """Returns Simhastha 2028 civic amenity points (water, first aid, rest zones)."""
    return JSONResponse(content=load_geojson_file("simhastha_amenities.geojson"))


@app.get("/api/v1/corridor/centerline")
async def get_centerline():
    """Returns the Ujjain–Indore highway centerline polyline."""
    return JSONResponse(content=load_geojson_file("highway_centerline.geojson"))


@app.get("/api/v1/stats")
async def get_stats():
    """Returns corridor-level aggregate health metrics."""
    return JSONResponse(content=load_geojson_file("corridor_summary.json"))


@app.get("/api/v1/survey/telemetry")
async def get_sample_telemetry():
    """Parses sample drone image flight telemetry."""
    sample_img = os.path.join("dataset", "raw_frames", "DJI_UJJ_001_KM01.jpg")
    if not os.path.exists(sample_img):
        return {"error": "Sample image not generated yet"}
    telemetry = DroneTelemetryParser.extract_telemetry(sample_img)
    gsd = DroneTelemetryParser.calculate_gsd(
        altitude_m=telemetry["estimated_altitude_m"],
        sensor_width_mm=telemetry["sensor_width_mm"],
        focal_length_mm=telemetry["focal_length_mm"],
        image_width_px=telemetry["width"]
    )
    telemetry["ground_sampling_distance_cm_px"] = gsd
    return telemetry


# Mount static web directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server:app", host="127.0.0.1", port=8000, reload=True)
