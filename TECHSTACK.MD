# Technology Stack & Toolchain Specification

## Project: GreenCorridor Ujjain
**AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)**  
**Document Version:** 1.0.0  

---

## 1. Architectural Stack Overview

| Tier | Primary Technologies | Key Purpose / Rationale | Open Source? |
| :--- | :--- | :--- | :--- |
| **Data Capture** | DJI Drone RGB Aerial Imagery, EXIF / XMP | High-resolution top-down aerial photography with RTK/GPS metadata | Yes (Standard RGB/EXIF) |
| **Preprocessing & Tiling** | Python 3.10+, Rasterio, GDAL, OpenCV, ExifTool | GeoTIFF manipulation, affine transform reprojection, $640\times640$ sliding window tiling | Yes (BSD/MIT) |
| **Crown Detection** | **DeepForest**, PyTorch, PyTorch Lightning | Pretrained deep learning package benchmarked on 30M+ tree crowns | Yes (MIT) |
| **Morphotype Classification** | PyTorch, Torchvision (ResNet-18 / MobileNetV3) | Classify crown patches into mature broadleaf, palm/columnar, shrub, or bare ground | Yes (Apache 2.0) |
| **Spatial Analysis** | **GeoPandas**, Shapely, PyProj, Rtree | Linear highway corridor slicing ($500\,\text{m}$), buffer creation ($70\,\text{m}$), canopy cover % | Yes (BSD) |
| **Spatial Database** | **GeoPackage (`.gpkg`)** / PostgreSQL + PostGIS | File-based OGC standard vector storage for minor project; PostGIS for production scalability | Yes (OGC / GPL) |
| **Backend API** | **FastAPI**, Pydantic v2, Uvicorn | Async Python REST framework serving GeoJSON features and analytics metrics | Yes (MIT) |
| **Officials' Dashboard** | React + Vite, MapLibre GL JS / Leaflet, Chart.js | Interactive GIS map canvas, segment inspection, CSV/PDF audit export | Yes (MIT) |
| **Pilgrim Shade PWA** | React / Lightweight HTML5, Leaflet, Workbox PWA | Mobile-optimized, bilingual (Hindi/English) offline-first shade & help map | Yes (MIT) |
| **Compute & Training** | Google Colab (Tesla T4) / Kaggle Free GPUs | Model fine-tuning and batch inference without expensive local hardware | Free Cloud Tier |

---

## 2. Detailed Component Breakdown & Selection Rationale

### 2.1 Computer Vision & Tree Crown Detection

#### **DeepForest (Weinstein et al.)**
- **Repository:** `https://github.com/weecology/DeepForest`
- **Why chosen:**
  - Standard deep learning models (generic YOLO or Faster R-CNN) trained on COCO detect people, cars, and dogs; they fail on nadir aerial canopy boundaries.
  - DeepForest comes pretrained on over **30 million crowns** from 22 diverse forest and urban canopy datasets.
  - Native support for sliding-window tile inference on large high-resolution aerial imagery with built-in border prediction merging.
  - Easily fine-tuned with 200–500 labeled highway tiles using PyTorch Lightning.
- **Alternative / Complement:** YOLOv8-OBB (Oriented Bounding Boxes) or Detectree2 (Mask R-CNN instance segmentation).

### 2.2 Geospatial Analysis & Data Ingestion

#### **Rasterio & GDAL**
- **Why chosen:** Rasterio provides idiomatic Python interfaces to GDAL for geospatial raster formats (`.tif`, `.geotiff`). It preserves spatial references (Affine transforms, EPSG projections) when cutting large drone orthophotos into sub-tiles.

#### **GeoPandas & Shapely**
- **Why chosen:**
  - Provides intuitive tabular geospatial analysis (similar to pandas DataFrames with a `geometry` column).
  - Spatial joins (`gpd.sjoin`) allow joining thousands of detected tree crown points into linear $500\,\text{m}$ highway segment polygons in under 1 second.
  - Effortless coordinate reprojection between `EPSG:4326` (WGS84 lat/long) and `EPSG:32643` (UTM Zone 43N metric grid).

### 2.3 Spatial Data Persistence

#### **GeoPackage (`.gpkg`) & GeoJSON**
- **Why chosen for Minor Project:**
  - Self-contained, single-file SQLite container conforming to Open Geospatial Consortium (OGC) standards.
  - Zero database installation or server maintenance required for student demonstration.
  - Directly readable by QGIS, GeoPandas, and ArcGIS.
- **Enterprise Upgrade Path:** PostgreSQL 15 + PostGIS 3.3 for high-concurrency municipal production environments.

### 2.4 Application Backend: FastAPI

- **Why chosen:**
  - Native asynchronous architecture (`async`/`await`) capable of streaming high-volume GeoJSON FeatureCollections with minimal latency.
  - Direct integration with Python data science libraries (GeoPandas, NumPy, PyTorch).
  - Automatic OpenAPI / Swagger interactive documentation (`/docs`).

### 2.5 Dual Client Presentation Tier

#### **Officials' GIS Dashboard (Desktop-First)**
- **Libraries:** React 18, Vite, MapLibre GL JS / Leaflet, Tailwind / Vanilla CSS design tokens.
- **Features:** Satellite imagery tile layers, segment canopy choropleth layers, tree point clustering, interactive sidebar charts, CSV/PDF export.
- **Prototyping Alternative:** Streamlit with `streamlit-folium` for rapid mentor milestone reviews.

#### **Pilgrim Shade & Help Map (Mobile PWA)**
- **Libraries:** React / Vanilla JS, Leaflet 1.9+, Workbox PWA Plugin.
- **Why chosen:**
  - Extremely lightweight: initial bundle payload under $1.5\,\text{MB}$.
  - Offline Service Worker: caches the entire 45 km route amenity data locally on the pilgrim's device so map remains functional even during severe network throttling at Simhastha ghats.
  - Full native i18n support for Hindi and English.

---

## 3. Hardware & Compute Environment Requirements

| Environment | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Local Development** | 8 GB RAM, 4-core Intel i5 / AMD Ryzen 5, 20 GB free SSD | 16 GB RAM, 8-core CPU, NVIDIA RTX 3060 (6 GB VRAM) |
| **Model Fine-Tuning** | Google Colab Free Tier (12 GB RAM, NVIDIA Tesla T4 16 GB) | Colab Pro / Kaggle GPU (T4 / P100) |
| **Inference Runtime** | CPU batch inference supported (~15 sec per $640\times640$ tile) | GPU accelerated batch inference (~0.3 sec per tile) |
| **Production Server** | 2 vCPU, 4 GB RAM (Ubuntu Linux 22.04 LTS / Docker) | 4 vCPU, 8 GB RAM, Nginx reverse proxy |

---

## 4. Software Dependencies & Package Manifest

### Python Ecosystem (`requirements.txt`)
```text
# Deep Learning & Computer Vision
deepforest==1.3.3
torch>=2.0.0
torchvision>=0.15.0
pytorch-lightning>=2.0.0
opencv-python-headless>=4.8.0
albumentations>=1.3.1
pillow>=10.0.0

# Geospatial & Remote Sensing
rasterio>=1.3.8
geopandas>=0.14.0
shapely>=2.0.0
pyproj>=3.6.0
rtree>=1.0.1
exifread>=3.0.0

# Backend & API
fastapi>=0.104.0
uvicorn[standard]>=0.23.2
pydantic>=2.4.2
python-multipart>=0.0.6

# Utilities & Scientific
numpy>=1.24.0
pandas>=2.1.0
matplotlib>=3.8.0
tqdm>=4.66.0
```

### Frontend Ecosystem (`package.json`)
```json
{
  "name": "greencorridor-frontend",
  "private": true,
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "leaflet": "^1.9.4",
    "lucide-react": "^0.300.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "vite-plugin-pwa": "^0.17.0"
  }
}
```
