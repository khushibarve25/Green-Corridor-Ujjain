# Engineering, Geospatial & Ecological Rules

## Project: GreenCorridor Ujjain
**AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)**  
**Document Version:** 1.0.0  

---

## 1. Geospatial & Coordinate System Rules

### RULE-GEO-001: Strict Coordinate Reference System (CRS) Separation
- **Display & Interchange CRS:** Always use **WGS 84 (`EPSG:4326`)** for GeoJSON payloads, API requests/responses, and frontend Leaflet/MapLibre tile renders. In GeoJSON, coordinates MUST strictly follow RFC 7946 format: `[longitude, latitude]`.
- **Metric Computation CRS:** NEVER compute distances (meters), buffer radii, or polygon areas ($\text{m}^2$) in angular degrees (`EPSG:4326`). Always reproject vector geometries to **WGS 84 / UTM Zone 43N (`EPSG:32643`)** prior to running `Shapely` or `GeoPandas` geometric calculations.

### RULE-GEO-002: Sliding Tile Affine Transform Integrity
- When cutting high-resolution aerial orthomosaics into $640\times640$ sliding window tiles, the spatial affine transform matrix (`affine.Affine`) must be recomputed and persisted for every individual tile.
- Tile naming convention must preserve global row and column indexes:  
  `tile_{survey_id}_r{row:04d}_c{col:04d}_{zoom}_{timestamp}.tif`

### RULE-GEO-003: Overlap & Stride Ratios
- To prevent truncation of tree crowns situated on tile seams, sliding window slicing must maintain an overlap stride of **$20\%$** (tile size: $640\times640$, step: $512$ px).
- Re-assembly across tile seams must execute spatial Non-Maximum Suppression (NMS) with an Intersection-over-Union threshold of $\text{IoU} = 0.45$.

---

## 2. Artificial Intelligence & Computer Vision Rules

### RULE-AI-001: Honest Validation & Metrics Integrity
- Never report model performance solely on training or validation sets. All evaluation metrics presented in papers or reports must be evaluated on unseen, hand-annotated test tiles.
- Evaluation metrics must always report three distinct numbers:
  1. **Bounding Box Precision** ($\ge 85\%$)
  2. **Bounding Box Recall** ($\ge 80\%$)
  3. **Absolute Tree Count Error Percentage** ($\le 10\%$):
     $$\text{Count Error} = \frac{|\text{Predicted Count} - \text{Ground Truth Count}|}{\text{Ground Truth Count}} \times 100$$

### RULE-AI-002: Vegetation Stratification Boundaries
Detections must not be lumped into a single generic "vegetation" category. The system must enforce physical stratification:
1. **Mature Shade Trees:** Crown Area $\ge 12\,\text{m}^2$, located in roadside outer verges or adjacent lands.
2. **Median Ornamental Shrubs:** Small flowering shrubs (e.g., Bougainvillea, Nerium) planted along the central highway divider ($\text{Area} < 8\,\text{m}^2$). These must **NOT** be counted toward pedestrian shade metrics.
3. **Bare Embankments / Stone Pitching:** Soil or rocky shoulders devoid of active vegetation cover.

### RULE-AI-003: Species Identification Modesty
- Acknowledge overhead drone optical limitations: nadir (top-down) RGB imagery captures crown canopy structure, not leaf venation, bark texture, or flowers.
- High-level classification must be termed **"Crown Morphotypes"** (e.g., Dense Broadleaf, Spreading Canopy, Columnar/Palm, Sparse Deciduous) unless verified by field botanist GPS ground-truth labels.

---

## 3. Urban Forestry & Ecological Rules

### RULE-ECO-001: Santamour 10-20-30 Diversity Rule
To prevent highway plantations from turning into fragile ecological monocultures susceptible to epidemics or pest outbreaks, the recommendation engine must enforce:
- No single species shall comprise $> 10\%$ of the corridor population.
- No single genus shall comprise $> 20\%$ of the corridor population.
- No single family shall comprise $> 30\%$ of the corridor population.

### RULE-ECO-002: Malwa Native Shade Species Prioritization
Recommendations for filling shade voids must prioritize proven indigenous trees adapted to the semi-arid, black-cotton soil conditions of the Ujjain–Malwa plateau:
- **Priority Tier 1 (Dense Native Shade):**
  - *Azadirachta indica* (Neem / नीम) — High canopy density, natural pest resistance, summer cooling.
  - *Ficus religiosa* (Peepal / पीपल) — Expansive crown footprint, cultural significance, round-the-clock oxygenation.
  - *Ficus benghalensis* (Banyan / बरगद) — Massive shade canopy, recommended for designated rest zones and bus bays.
  - *Millettia pinnata* (Karanj / करंज) — Drought-hardy, road-dust tolerant, rich oilseeds.
  - *Syzygium cumini* (Jamun / जामुन) — Thick evergreen canopy, hardy roadside performer.
- **Priority Tier 2 (Flowering & Soil Binding):**
  - *Cassia fistula* (Amaltas / अमलतास) — Medium height, yellow flowering, suitable for outer verges.
  - *Butea monosperma* (Palash / पलाश) — Extreme drought resilience.

### RULE-ECO-003: Prohibited & Discouraged Species
Under no circumstances shall the recommendation engine prescribe:
- *Eucalyptus globulus* / *Eucalyptus hybrid*: Excessive groundwater depletion, fragile branch structure prone to falling on passing highway traffic during summer squalls.
- *Conocarpus erectus*: Highly invasive root structures causing road pavement buckling; aero-allergenic pollen concerns.
- *Prosopis juliflora* (Vilayati Babool): Invasive thorny weed suppressing native undergrowth.

### RULE-ECO-004: Road Safety & Highway Geometry Constraints
- **Median Restriction:** Large shade trees (canopy radius $> 3\,\text{m}$, height $> 2\,\text{m}$) must **NEVER** be recommended for the central median divider. Median plantings must be restricted to low-height shrubs ($\le 1.2\,\text{m}$) to preserve vehicular sight distances and prevent root intrusions into structural pavement layers.
- **Clear Zone Setback:** High-girth trees must maintain a minimum lateral clearance of $5.0\,\text{m}$ from the active six-lane carriageway edge unless shielded by W-beam crash barriers (IRC:SP:84 guidelines).

---

## 4. Software Architecture & Code Standards

### RULE-DEV-001: Python Code Standards
- Adhere strictly to **PEP 8** style guidelines.
- Mandatory type annotations for all function and method signatures.
- No bare `except:` clauses; catch specific exceptions (`ValueError`, `FileNotFoundError`, `RasterioIOError`).
- Use structured logging (`logger = logging.getLogger(__name__)`) instead of raw `print()` statements in production services.

### RULE-DEV-002: Fast and Lightweight Frontend Assets
- The Pilgrim Shade & Help Web App must maintain a total initial production bundle size of $\le 1.8\,\text{MB}$ uncompressed.
- All map vector layers must be served in chunked GeoJSON or vector tile (`pbf`) format to ensure fluid interaction on 3G cellular connections in crowded Simhastha environments.

### RULE-DEV-003: Language & Accessibility (i18n)
- The Pilgrim interface must support complete, native bilingual localization:
  - English (`en`)
  - Hindi (`hi`)
- Terminology must use familiar pilgrim terms:
  - Drinking water: *"पीने का पानी (प्याऊ / छबील)"*
  - First aid: *"चिकित्सा केंद्र"*
  - Shaded rest point: *"छायादार विश्राम स्थल"*
  - High heat alert: *"अत्यधिक धूप क्षेत्र"*

### RULE-DEV-004: Version Control & Git Commit Convention
- Commit messages must follow Conventional Commits format:
  - `feat(detection): integrate deepforest tile inference with spatial nms`
  - `fix(segmentation): correct utm zone 43n area calculation in geopandas`
  - `docs(prd): expand simhastha 2028 operational requirements`
