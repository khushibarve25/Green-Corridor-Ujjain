# Architecture Decision Records (ADRs)

## Project: GreenCorridor Ujjain
**AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)**  
**Document Version:** 1.0.0  

---

## Index of Decisions

- **ADR-001:** Selection of DeepForest for Crown Detection over Training from Scratch
- **ADR-002:** Deterministic Rule-Based Recommendation Engine vs. Black-Box AI
- **ADR-003:** Discretization into 500-Meter Highway Linear Segments
- **ADR-004:** Dual Interface Architecture: Officials Dashboard vs. Pilgrim Mobile PWA
- **ADR-005:** GeoPackage & GeoJSON Storage for Minor Project Scope
- **ADR-006:** Coordinate System Separation: EPSG:4326 (Display) vs. EPSG:32643 (Metric)
- **ADR-007:** Strict Stratification: Mature Shade Trees vs. Median Ornamental Shrubs
- **ADR-008:** 640×640 px Tile Resolution with 20% Overlap Stride

---

### ADR-001: Selection of DeepForest for Crown Detection
* **Status:** Accepted  
* **Context:** The team needs to detect and count thousands of tree crowns from aerial drone photography. Standard object detectors (YOLOv8, Faster R-CNN) trained on MS-COCO fail on overhead nadir forest canopies due to lack of distinct bounding borders, variable illumination, and continuous textures.  
* **Decision:** Adopt **DeepForest** (Weinstein et al., 2020), an open-source deep learning package with a RetinaNet backbone pre-trained on 30 million algorithmically generated crowns and fine-tuned on 10,000 hand-annotated airborne RGB crowns.  
* **Alternatives Considered:**
  1. *Training YOLOv8 from scratch:* Rejected due to the massive annotation overhead (thousands of boxes needed to generalize) and high risk of overfitting to specific sun angles.
  2. *SAM (Segment Anything Model) zero-shot:* Rejected due to high GPU memory footprint ($>16\,\text{GB}$) and propensity to over-segment individual tree crown foliage clusters into dozens of micro-polygons.  
* **Consequences:** Provides an immediate out-of-the-box baseline with high crown recall, requiring only light fine-tuning (200–500 local highway annotations) to adapt to Ujjain roadside conditions.

---

### ADR-002: Deterministic Rule-Based Recommendation Engine vs. Black-Box AI
* **Status:** Accepted  
* **Context:** Civic engineers at MPRDC/NHAI and forestry officers from the MP Forest Department require planting recommendations to fill canopy gaps. Government decision-makers are legally accountable for public afforestation funds and reject unexplainable "black-box" outputs.  
* **Decision:** Implement a **deterministic, rule-based recommendation engine** enforcing established urban forestry guidelines:
  1. Santamour 10-20-30 diversity rule ($\le 10\%$ single species, $\le 20\%$ genus, $\le 30\%$ family).
  2. Indigenous Malwa species selection matrix (Neem, Peepal, Banyan, Karanj, Jamun).
  3. Physical highway safety constraints (no large trees in medians, 5m carriageway setback).  
* **Alternatives Considered:**
  1. *Reinforcement Learning / Black-box neural recommender:* Rejected because outputs cannot be legally defended or explained to administrative auditors.
  2. *Generative AI / LLM prompt-based recommender:* Rejected due to hallucination risks and lack of strict adherence to local ecological constraints.  
* **Consequences:** Transparent, defensible, and instantly interpretable recommendations: *"Segment 14 has 4.1% canopy and over-representation of Neem (68%); plant 50 Karanj and 35 Jamun to restore diversity."*

---

### ADR-003: Discretization into 500-Meter Highway Linear Segments
* **Status:** Accepted  
* **Context:** A 45–55 km highway corridor is too long to treat as a single uniform entity, while a 5-meter grid creates an unmanageable computational burden for tabular municipal reporting.  
* **Decision:** Discretize the highway corridor into **500-meter contiguous linear segments** ($S_1, S_2, \dots, S_N$).  
* **Rationale:**
  1. *Alignment with Highway Engineering:* Standard NHAI / MPRDC maintenance contracts, chainage markers, and toll milestone reporting operate on 500m or 1km intervals.
  2. *Pedestrian Reality:* A 500m stretch represents approximately a 6-to-8 minute walk in scorching heat—the exact threshold where an unshaded void causes significant heatstroke risk for pilgrims.  
* **Consequences:** Clean, actionable aggregation unit for both municipal tenders and pilgrim heat-risk badges.

---

### ADR-004: Dual Interface Architecture: Officials Dashboard vs. Pilgrim PWA
* **Status:** Accepted  
* **Context:** The project has two distinct audiences: government planners needing technical geospatial analysis, and millions of devotees navigating the road during Simhastha in 45°C heat.  
* **Decision:** Architect two separate frontends powered by a unified spatial API:
  1. **Officials' Analytics Dashboard:** Desktop-first, multi-layered GIS map (MapLibre / Leaflet), segment inspection, audit comparison, and PDF/CSV export.
  2. **Pilgrim Shade & Help PWA:** Mobile-first, single-thumb navigation, high-contrast Devanagari typography, bilingual (Hindi/English), and offline service worker caching.  
* **Consequences:** Prevents overloading pilgrims with complex GIS metrics while giving officials the high-density data required for project audits.

---

### ADR-005: GeoPackage & GeoJSON Storage for Minor Project Scope
* **Status:** Accepted  
* **Context:** The project requires storing vector features (thousands of tree crown polygons, highway centerline, 500m segment boundaries, amenity points).  
* **Decision:** Use **GeoPackage (`.gpkg`)** and **GeoJSON** as the primary persistence layer for the minor project demonstration, with an optional Dockerized PostGIS configuration.  
* **Rationale:**
  - GeoPackage is an open OGC standard built on SQLite. It requires zero database server daemon, runs seamlessly in local student environments, is cross-platform, and opens natively in QGIS and GeoPandas.  
* **Consequences:** Eliminates database setup friction for academic evaluation while maintaining standard SQL spatial query capabilities (`ST_Intersects`, `ST_Area`).

---

### ADR-006: Coordinate System Separation: EPSG:4326 vs. EPSG:32643
* **Status:** Accepted  
* **Context:** Computing polygon areas in angular degrees (`EPSG:4326`) causes catastrophic distortion errors, while web map libraries require WGS84 latitude/longitude.  
* **Decision:**
  - **Interchange & Display:** Use **WGS 84 (`EPSG:4326`)** for all GeoJSON payloads, Leaflet/MapLibre layers, and API responses.
  - **Metric Calculation:** Reproject all geometries to **WGS 84 / UTM Zone 43N (`EPSG:32643`)** inside GeoPandas before calculating crown areas ($\text{m}^2$), segment canopy cover percentages, or buffer distances.  
* **Consequences:** Ensures mathematical accuracy in canopy area measurements without breaking compatibility with standard web mapping tools.

---

### ADR-007: Strict Stratification: Mature Shade Trees vs. Median Shrubs
* **Status:** Accepted  
* **Context:** Aerial drone imagery shows highway medians planted with young ornamental shrubs (*Bougainvillea*, *Nerium*). If counted as "trees", they give a falsely inflated canopy cover reading while providing zero shade to pedestrians.  
* **Decision:** Implement geometric and spatial masking to split detections into distinct classes:
  1. *Mature Trees:* Area $\ge 12\,\text{m}^2$, located in outer verges.
  2. *Median Ornamental Shrubs:* Detections within the highway median buffer with area $< 8\,\text{m}^2$.
  3. *Bare Embankments / Shoulders.*  
* **Consequences:** Preserves the integrity of pedestrian shade calculations and prevents deceptive green cover inflation.

---

### ADR-008: 640×640 px Tile Resolution with 20% Overlap Stride
* **Status:** Accepted  
* **Context:** Orthomosaics and high-resolution drone photos can exceed $10,000 \times 10,000$ pixels, which causes out-of-memory errors on GPU inference. Slicing without overlap truncates crowns sitting across tile boundaries.  
* **Decision:** Adopt a standard tile size of **$640 \times 640$ pixels** with a **$20\%$ overlap stride** ($512$ pixels step), followed by global spatial Non-Maximum Suppression (NMS, $\text{IoU} = 0.45$).  
* **Consequences:** Matches standard neural network input dimensions, maximizes GPU batch efficiency, and completely eliminates split-crown double counting along seams.
