# Product Requirements Document (PRD)

## Project: GreenCorridor Ujjain
**Subtitle:** AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)  
**Document Version:** 1.0.0  
**Target Event:** Simhastha Kumbh Mela (March 27 – May 27, 2028)  
**Corridor:** Ujjain–Indore 6-Lane Highway (SH-27 / NH upgrade, ~45–55 km corridor)  

---

## 1. Executive Summary & Vision
The Ujjain–Indore highway corridor is undergoing major widening into a six-lane highway to accommodate an estimated **40 crore devotees** during **Simhastha 2028**, with peak single-day influxes nearing 4 crore pilgrims. The widening project necessitated cutting or transplanting an estimated **3,000 mature shade trees**. The Government of Madhya Pradesh has announced a massive afforestation drive of **15 lakh trees** in the Ujjain region, particularly along pilgrimage and approach routes.

However, road authorities and civic agencies currently lack a scalable, objective, and auditable mechanism to:
1. Establish a scientific baseline of surviving green cover.
2. Accurately detect, count, and classify roadside tree crowns vs. median shrubs.
3. Quantify canopy gaps and heat exposure along the 500-meter highway segments.
4. Generate explainable, rule-based planting recommendations (prioritizing native Malwa shade species while preventing monocultures).
5. Provide pilgrims navigating scorching April–May temperatures (surface asphalt $>45^\circ\text{C}$) an accessible, lightweight **Shade and Help Map**.

**GreenCorridor Ujjain** bridges this divide by turning aerial drone imagery (top-view DJI drone RGB frames and orthomosaics) into verifiable tree censuses, spatial canopy analytics, and dual-purpose public interfaces.

---

## 2. Problem Statement

### 2.1 The Planning & Verification Deficit
Traditional highway tree surveys rely on manual foot patrols. These are slow, expensive, subjective, and prone to "ghost saplings" (where saplings are recorded on planting day but dry out within months without audit).

### 2.2 The Extreme Summer Heat & Simhastha 2028
Simhastha takes place in peak summer (late March to late May). Road asphalt temperatures routinely reach $50^\circ\text{C}$. Urban forestry studies confirm:
- Tree shade reduces road surface temperature by $12^\circ\text{C}\text{--}19^\circ\text{C}$.
- Tree shade cuts globe/mean radiant temperature (perceived heat) by $4^\circ\text{C}\text{--}7^\circ\text{C}$.
Pilgrims, pedestrians, and stranded motorists face severe heatstroke risk along unshaded sections.

### 2.3 The Monoculture & Invasive Species Risk
Highway median plantations often default to non-native, water-guzzling, or shallow-rooted varieties that provide no shade. Ecological balance demands adhering to the **Santamour 10-20-30 diversity rule** ($\le 10\%$ single species, $\le 20\%$ genus, $\le 30\%$ family).

### 2.4 The Unprocessed Aerial Imagery Problem
Officials and mentors collect gigabytes of high-resolution drone frames. Raw aerial imagery without AI-driven spatial extraction cannot inform municipal budgets or planting tenders.

---

## 3. Goals and Non-Goals

### 3.1 Primary Goals
- **Automated Crown Enumeration:** Accurately detect individual tree crowns from drone RGB images ($640\times640$ pixel tiles) with Precision $\ge 85\%$, Recall $\ge 80\%$, and Count Error $\le 10\%$ against manual validation sample tiles.
- **Vegetation Stratification:** Distinguish between mature shade trees, median ornamental shrubs (e.g., Bougainvillea, Nerium), and bare embankments/shoulders.
- **Highway Linear Discretization:** Divide the 45–55 km corridor into $500\,\text{m}$ segments; calculate canopy cover percentage ($C_{\text{cov}}$), tree density, and crown diameter per segment.
- **Gap & Heat-Risk Analysis:** Identify segments with $C_{\text{cov}} < 8\%$ as critical shade gaps and assign heat-vulnerability scores.
- **Explainable Native Recommendations:** Provide automated, transparent planting recommendations adhering to forestry guidelines, prioritizing indigenous drought-tolerant shade species (Neem, Peepal, Banyan, Karanj, Mahua).
- **Dual Delivery Systems:**
  - **Officials' Dashboard:** Map layers, canopy metrics, gap prioritization, CSV/GeoJSON audit export.
  - **Pilgrim Shade & Help Map:** Mobile-first, bilingual (Hindi/English) PWA displaying shade spots, drinking water (*Pyaau*), medical kiosks, toilets, and rest areas.

### 3.2 Non-Goals (Out of Scope for Minor Project)
- Hyperspectral disease diagnosis or biochemical chlorophyll stress detection.
- Real-time video streaming analysis from active in-flight drones.
- Live crowd surveillance or turn-by-turn vehicle GPS navigation.
- Broad geographic processing outside the defined Ujjain–Indore highway corridor buffer ($70\,\text{m}$ width).

---

## 4. User Personas & User Journeys

| Persona | Role | Key Objectives | Critical Pain Point |
| :--- | :--- | :--- | :--- |
| **Er. R. K. Sharma** | Executive Engineer, MPRDC / NHAI | Monitor green cover percentage per km; audit contractor survival compliance; present progress to ministry. | Has thousands of unindexed drone images; unable to verify survival rate on ground. |
| **Dr. Anjali Verma** | Forest Department Officer / Botanist | Enforce native biodiversity; prevent invasive or water-heavy species; plan sapling logistics. | Sapling survival data is recorded manually on paper without GPS coordinates. |
| **Ramesh & Geeta Patel** | Simhastha Pilgrims (Walking / Public Transit) | Find shaded rest stops, nearest drinking water kiosks, toilet blocks, and medical help during peak sun ($12\text{--}4\,\text{PM}$). | Extreme heat stress on open, widened six-lane asphalt without shade. |

---

## 5. Functional Requirements (FR)

### Module 1: Drone Imagery Ingestion & Preprocessing
- **FR-1.1 EXIF/GPS Metadata Extraction:** System must parse EXIF/XMP tags (Latitude, Longitude, Altitude, Gimbal Yaw, Resolution, Date/Time).
- **FR-1.2 Orthomosaic & Frame Tiling:** Support both pre-stitched GeoTIFF orthomosaics and georeferenced raw drone frames, slicing them into $640\times640$ overlapping tiles with a $20\%$ overlap stride.
- **FR-1.3 Spatial Deduplication:** Implement coordinate-based spatial deduplication to prevent counting the same crown twice in overlapping frames.

### Module 2: AI Crown Detection & Morphotype Classification
- **FR-2.1 Pretrained Crown Detector:** Integrate the DeepForest model (RetinaNet backbone pretrained on 30M+ algorithmic crowns and 10k+ hand-annotated aerial crowns).
- **FR-2.2 Local Fine-Tuning:** Provide fine-tuning utilities using local highway drone annotation samples.
- **FR-2.3 Edge NMS Re-assembly:** Stitch tile-level bounding boxes across borders using non-maximum suppression (NMS IoU threshold $= 0.45$).
- **FR-2.4 Vegetation Class Distinction:**
  - Class 1: *Mature Tree* (Crown area $> 12\,\text{m}^2$)
  - Class 2: *Median Shrub / Ornamental Bush* (Clusters within central median)
  - Class 3: *Bare Soil / Embankment Gap*
- **FR-2.5 Visual Morphological Sub-types:** Classify detected crowns into 4 visual structural categories (Dense Broadleaf, Spreading Canopy, Palm/Columnar, Sparse/Deciduous).

### Module 3: Spatial Corridor Analytics & Gap Detection
- **FR-3.1 Highway Buffer & Segmentation:** Generate a $70\,\text{m}$ corridor buffer ($35\,\text{m}$ on either side of centerline) and segment into contiguous $500\,\text{m}$ segments.
- **FR-3.2 Metric Aggregation:** Compute:
  $$\text{Canopy Cover (\%)} = \frac{\sum \text{Crown Area within Segment}}{\text{Total Segment Corridor Area}} \times 100$$
  $$\text{Tree Density} = \frac{\text{Tree Count}}{\text{Segment Length (km)}}$$
- **FR-3.3 Critical Gap Flagging:** Flag segments with $\text{Canopy Cover} < 8\%$ as "High Planting Priority".
- **FR-3.4 Carbon Stock Estimation:** Provide an approximate exploratory carbon sequestration estimate based on allometric crown area formulas:
  $$\text{Approx. Aboveground Biomass (AGB)} = a \cdot (\text{Crown Area})^b$$
  *(Clearly labeled in UI as an indicative planning estimate).*

### Module 4: Explainable Recommendation Engine
- **FR-4.1 Santamour Diversity Rule Enforcement:** Trigger an over-representation alert if any single morphotype/species exceeds $10\%$ of segment or corridor total.
- **FR-4.2 Native Species Prescriptions:** Recommend Malwa-indigenous, low-maintenance shade trees:
  - *Azadirachta indica* (Neem)
  - *Ficus religiosa* (Peepal)
  - *Ficus benghalensis* (Banyan)
  - *Millettia pinnata* (Karanj)
  - *Syzygium cumini* (Jamun)
- **FR-4.3 Discouraged Species Filter:** Flag and discourage water-draining or brittle roadside trees (*Eucalyptus*, *Conocarpus*, *Leucaena*).
- **FR-4.4 Explainability Output:** Each segment recommendation must provide human-readable logic:
  `"Segment 14 (KM 18.0 - 18.5): 4.1% canopy cover, 92 planting slots available. Low broadleaf diversity. Recommend: 40 Neem, 30 Karanj, 22 Jamun. Median shrubs present: do not plant tall trees in median."`

### Module 5: Officials' Analytics Dashboard
- **FR-5.1 Interactive Web Map:** MapLibre / Leaflet interactive GIS canvas showing:
  - Crown bounding boxes / centroid pins
  - Segment canopy choropleth (Green $\ge 25\%$, Amber $10\text{--}25\%$, Red $< 10\%$)
  - Gap ranking table sorted by intervention priority
- **FR-5.2 Audit & Comparison View:** Compare baseline flight (e.g., Oct 2026) vs. follow-up monitoring flight (e.g., 2027) to calculate sapling survival percentage.
- **FR-5.3 Export Capabilities:** 1-click export of segment reports as GeoJSON, CSV, and summary PDF.

### Module 6: Pilgrim Shade & Help Mobile Web App
- **FR-6.1 Bilingual Accessibility:** Full toggle between Hindi (हिंदी) and English.
- **FR-6.2 Heat-Risk Segment Overlay:** Visual green-to-red shade indicator along the highway.
- **FR-6.3 Simhastha Amenities Locator:** Geo-tagged markers for:
  - Drinking water kiosks (*Pyaau / Chhabeel*)
  - Emergency medical outposts (*Chikitsa Kendra*)
  - Public toilets (*Sulabh Shauchalaya*)
  - Police help booths & resting sheds (*Chhaya Kendra*)
- **FR-6.4 Offline / Low-Bandwidth Mode:** Lightweight static PWA assets capable of cached offline rendering.

---

## 6. Non-Functional Requirements (NFR)

| Metric | Target | Verification Method |
| :--- | :--- | :--- |
| **Detection Precision** | $\ge 85\%$ | Evaluation against 500 manually labeled test crowns |
| **Detection Recall** | $\ge 80\%$ | Evaluation against 500 manually labeled test crowns |
| **Count Error** | $\le 10\%$ | $|(\text{Predicted} - \text{GroundTruth})/\text{GroundTruth}|$ on held-out tiles |
| **Inference Throughput** | $\ge 2\text{ hectares/min}$ | Benchmarked on NVIDIA T4 / RTX 3060 / Colab GPU |
| **Pilgrim PWA Bundle Size** | $\le 1.8\text{ MB}$ initial load | Chrome Lighthouse & Webpack bundle analyzer |
| **PWA Mobile Load Time** | $\le 2.0\text{ seconds}$ on 3G network | Network throttling test |
| **Geospatial Integrity** | EPSG:4326 (WGS84) & EPSG:32643 (UTM 43N) | Coordinate reprojection unit tests |

---

## 7. Deliverables & Acceptance Criteria

1. **Preprocessing & Tile Pipeline:** Script converting raw drone photos / orthomosaics into $640\times640$ georeferenced tiles with EXIF index.
2. **Crown Detection & Classification Pipeline:** Trained DeepForest / PyTorch model with edge NMS, producing GeoJSON crown vector points and areas.
3. **Corridor Analytics & Recommendation Engine:** GeoPandas module dividing corridor into $500\,\text{m}$ slices, scoring canopy %, and outputting native planting prescriptive rules.
4. **Officials' Web Dashboard:** Functional web UI with interactive map, segment drilldown, gap ranking, and export options.
5. **Pilgrim Shade & Help Map:** Mobile-responsive bilingual web app with shade rating and civic amenities.
6. **Project Report & Documentation:** Minor project documentation adhering to college guidelines with full methodology and validation results.
