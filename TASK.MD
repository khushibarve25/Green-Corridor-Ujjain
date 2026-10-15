# Task Breakdown & Implementation Roadmap

## Project: GreenCorridor Ujjain
**AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)**  
**Document Version:** 1.0.0  
**Status Legend:** `[x]` Completed | `[~]` In Progress | `[ ]` Pending  

---

## Phase 0: Project Setup, Environment & Dataset Ingestion

- [x] **TASK-001 [P0] Project Requirements & Documentation**
  - Synthesize mentor concept note and academic research into comprehensive project artifacts (`PRD.md`, `ARCHITECTURE.MD`, `TASK.MD`, `RULE.MD`, `DESIGN.MD`, `TECHSTACK.MD`, `BRAIN.md`, `Agent.md`, `Decisions.md`).
- [x] **TASK-002 [P0] Repository Setup & Environment Configuration**
  - Set up Python virtual environment (`venv` / `conda`).
  - Configure `requirements.txt` with DeepForest, PyTorch, GeoPandas, Rasterio, OpenCV, FastAPI, and Uvicorn.
  - Setup Node.js frontend workspace (React + Vite + Leaflet / MapLibre).
- [x] **TASK-003 [P0] Drone Imagery Catalog & Inspection**
  - Inventory available Ujjain–Indore drone photos (check file formats, resolutions, overlap factor, capture dates, flight altitudes).
  - Extract EXIF GPS metadata and compile flight coverage boundary in GeoJSON format.
  - Built synthetic mock dataset pipeline (`scripts/generate_mock_dataset.py`) generating top-view drone frames and 30-segment corridor spatial database.

---

## Phase 1: Imagery Preprocessing & Spatial Tiling

- [x] **TASK-101 [P0] EXIF/XMP Telemetry Extractor**
  - Implemented `src/preprocessing.py` with `DroneTelemetryParser` to calculate GSD, altitude, and sensor telemetry.
- [x] **TASK-102 [P0] Sliding Window Tiler Pipeline**
  - Implemented `SlidingWindowTiler` with configurable tile dimensions ($640\times640$ px) and step stride ($512$ px, $20\%$ overlap).
- [ ] **TASK-103 [P1] Stitching Pipeline (Conditional)**
  - If raw overlapping frames need orthomosaic creation, run OpenDroneMap (ODM) or WebODM CLI to generate orthophoto GeoTIFF.

---

## Phase 2: Tree Crown Detection & Model Fine-Tuning

- [ ] **TASK-201 [P0] Pretrained DeepForest Baseline Inference**
  - Install and initialize `deepforest.main.deepforest()`.
  - Run initial zero-shot inference on sample highway tiles.
  - Evaluate default recall and false positive rate on roadside infrastructure (guard rails, lane markings, median curbs).
- [ ] **TASK-202 [P0] Annotation & Ground-Truth Dataset Creation**
  - Select representative highway tiles (urban approach, rural fields, bridges, median sections).
  - Label 300–500 tree crowns using Label Studio or CVAT format (PASCAL VOC / COCO format).
  - Split dataset into Train ($70\%$), Validation ($15\%$), and Test ($15\%$) sets.
- [ ] **TASK-203 [P0] Model Fine-Tuning & Evaluation**
  - Fine-tune DeepForest on local Ujjain highway crown annotations using PyTorch Lightning.
  - Benchmark performance: calculate Precision, Recall, F1-score, and count error percentage against manual counts on held-out test tiles.
  - Acceptance threshold: Precision $\ge 85\%$, Recall $\ge 80\%$, Count Error $\le 10\%$.
- [x] **TASK-204 [P0] Border Re-Assembly & Spatial NMS**
  - Implemented `SpatialNMS` in `src/detection.py` with IoU threshold deduplication across tile borders.
  - Output georeferenced crown GeoJSON features with area, diameter, and confidence.

---

## Phase 3: Coarse Morphological Classification

- [x] **TASK-301 [P0] Class Separation: Tree vs. Median Shrub vs. Bare Ground**
  - Built `VegetationClassifier` in `src/detection.py`:
    1. *Mature Trees* (Crown Area $> 12\,\text{m}^2$)
    2. *Median Ornamental Shrubs* (Bougainvillea / Nerium clusters in median)
    3. *Barren Shoulder / Embankment Soil*
- [~] **TASK-302 [P1] Crown Morphotype Classifier**
  - Classification into 4 visual architectural types: Dense Round Broadleaf, Spreading Open Canopy, Palm/Columnar, Sparse Deciduous.
- [ ] **TASK-303 [P2] Botanical Ground-Truth Cross-Referencing**
  - Connect field survey GPS points (Neem, Peepal, Banyan, Karanj) to map identified crown clusters to confirmed botanical names where available.

---

## Phase 4: Highway Corridor Segmentation & Gap Analytics

- [x] **TASK-401 [P0] Centerline Digitization & Buffer Creation**
  - Generated Ujjain–Indore highway alignment geometry and $70\,\text{m}$ corridor buffer ($35\,\text{m}$ left/right).
- [x] **TASK-402 [P0] Linear 500m Discretization**
  - Sliced corridor into 30 regular $500\,\text{m}$ linear segments (KM 0.0 to KM 15.0).
- [x] **TASK-403 [P0] Canopy Metric Aggregator**
  - Implemented `HighwaySegmentationEngine` in `src/segmentation.py`:
    - Canopy coverage percentage ($C_{\text{cov}}$)
    - Tree count & shrub count per segment
- [x] **TASK-404 [P0] Critical Gap Identification**
  - Flagged segments with $C_{\text{cov}} < 8\%$ as Critical Shade Gaps with priority ranking.
- [x] **TASK-405 [P1] Exploratory Carbon Stock Estimation**
  - Implemented allometric carbon stock calculator ($tC$) per segment.

---

## Phase 5: Explainable Recommendation Engine

- [x] **TASK-501 [P0] Santamour 10-20-30 Rule Evaluator**
  - Implemented `EcologicalRecommendationEngine` in `src/recommendation.py` with 10% species dominance alerting.
- [x] **TASK-502 [P0] Native Malwa Planting Prescription Generator**
  - Rule-based prescriptions prioritizing Neem, Peepal, Banyan, Karanj, Jamun, while forbidding Eucalyptus and Conocarpus.
- [x] **TASK-503 [P0] Human-Readable Explanation Synthesizer**
  - Automatic synthesis of natural language rationales for engineers and forest officers.

---

## Phase 6: Dual UI Development (Officials Dashboard + Pilgrim PWA)

- [x] **TASK-601 [P0] Backend API Development (FastAPI)**
  - Implemented `src/server.py` serving `/api/v1/corridor/segments`, `/api/v1/crowns`, `/api/v1/pilgrim/amenities`, and `/api/v1/stats`.
- [x] **TASK-602 [P0] Officials' Web Dashboard**
  - Interactive Leaflet GIS map with canopy choropleth, tree crown circles, segment inspection drawer, and CSV export.
- [x] **TASK-603 [P0] Pilgrim Shade & Help Mobile Web App**
  - Bilingual (Hindi/English) PWA view with live Route Heat-Risk Bar, amenity filters, and emergency SOS callouts.
- [~] **TASK-604 [P1] Before-and-After Plantation Monitor Interface**
  - Initial baseline metrics integrated; comparison flight slider ready for multi-temporal flight datasets.

---

## Phase 7: Validation, Testing & Minor Project Report

- [ ] **TASK-701 [P0] Model Validation & Statistical Verification**
  - Run blind validation on 10 held-out test drone tiles; record precision, recall, and count error percentage in formal tables.
- [x] **TASK-702 [P0] System Integration & End-to-End Testing**
  - Verified end-to-end pipeline: synthetic drone images $\rightarrow$ sliding tiler $\rightarrow$ NMS $\rightarrow$ segmentation $\rightarrow$ recommendation $\rightarrow$ interactive web prototype.
- [ ] **TASK-703 [P0] Minor Project Report & Presentation Preparation**
  - Compile final documentation, methodology diagrams, research paper citations, and demonstration slides for university evaluation.
