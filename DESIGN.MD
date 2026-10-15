# UI/UX & System Design Document

## Project: GreenCorridor Ujjain
**AI-Based Tree Census, Green Cover Gap Analysis, and Shade Planning for the Ujjain–Indore Highway (Simhastha 2028)**  
**Document Version:** 1.0.0  

---

## 1. Design Philosophy & Aesthetic Identity

GreenCorridor Ujjain serves two drastically different user archetypes:
1. **Civic Planners & Forestry Engineers (Officials' Dashboard):** Require high-density information architecture, precise geospatial controls, audit trail verification, and multi-layered GIS choropleths.
2. **Simhastha Devotees & Highway Pedestrians (Pilgrim Web App):** Require an ultra-clean, mobile-first, high-contrast, bilingual interface designed for outdoor readability under intense direct sunlight, poor cellular connectivity, and zero technological learning curve.

### 1.1 Visual Tone & Theme
- **Theme:** Clean, modern, nature-tech aesthetic combining deep emerald greens, technical charcoal slates, warm Malwa sandstone accents, and vibrant warning hues for heat vulnerability.
- **Glassmorphism & Micro-Interactions:** Subtle backdrop blurs (`backdrop-filter: blur(12px)`), gentle elevation shadows, and animated transitions on hover and active segment selection.
- **Sunlight Readability:** High contrast ratios (WCAG AAA standard $\ge 7:1$) on mobile interfaces to ensure pilgrims can view the shade map easily under bright mid-day sunlight.

---

## 2. Color Palette & Typography Tokens

### 2.1 Color Tokens

| Token Name | Hex Code | HSL / RGB | Purpose / Usage |
| :--- | :--- | :--- | :--- |
| `--forest-900` | `#08281E` | `hsl(163, 67%, 9%)` | Dark mode primary surface & headers |
| `--forest-700` | `#0E4F39` | `hsl(161, 70%, 18%)` | Primary brand accent & active states |
| `--forest-500` | `#10B981` | `hsl(160, 84%, 39%)` | Dense canopy indicators ($\ge 25\%$ canopy) |
| `--amber-500` | `#F59E0B` | `hsl(38, 92%, 50%)` | Moderate shade / caution ($10\%\text{--}25\%$ canopy) |
| `--coral-500` | `#EF4444` | `hsl(0, 84%, 60%)` | Critical shade gap ($< 8\%$ canopy) / high heat alert |
| `--sandstone-100`| `#F9F6F0` | `hsl(40, 43%, 96%)` | Pilgrim app background (reduces glare vs harsh white) |
| `--slate-800` | `#1E293B` | `hsl(217, 33%, 17%)` | Officials sidebar & card backgrounds |
| `--slate-100` | `#F1F5F9` | `hsl(210, 40%, 96%)` | Light mode surface & card borders |

### 2.2 Typography Hierarchy
- **Latin Font Family:** `'Inter'`, `'Plus Jakarta Sans'`, sans-serif.
- **Devanagari Font Family (Hindi):** `'Noto Sans Devanagari'`, `'Rozha One'`, sans-serif.
- **Font Scale:**
  - `Display / H1`: $32\,\text{px} / 2.0\,\text{rem}$, Bold ($700$) — Highway Title & Simhastha Tracker
  - `Heading / H2`: $24\,\text{px} / 1.5\,\text{rem}$, SemiBold ($600$) — Segment Analytics Headers
  - `Subhead / H3`: $18\,\text{px} / 1.125\,\text{rem}$, Medium ($500$) — Card Titles & Metrics
  - `Body Regular`: $14\,\text{px} / 0.875\,\text{rem}$, Regular ($400$) — Data descriptions & explanations
  - `Data / Monospace`: `'JetBrains Mono'`, monospace — Chainage KM, GPS Lat/Lng, Crown IDs

---

## 3. Officials' Analytics & Audit Dashboard Design

### 3.1 Layout Architecture (Desktop-First)
The dashboard uses an asymmetric split layout maximizing map workspace while providing instant drilldown on segment statistics.

```
+-----------------------------------------------------------------------------------------------+
| [LOGO] GreenCorridor Ujjain | Simhastha 2028 Planning | Total Trees: 14,820 | Corridor: 16.4% |
+-------------------------------------------------------------+---------------------------------+
|                                                             | [SEGMENT INSPECTION PANEL]      |
|  [GIS MAP CANVAS - MapLibre / Leaflet]                      | Chainage: KM 18.0 - 18.5        |
|                                                             | Canopy Cover: 4.1% [CRITICAL]   |
|  - High-res satellite / drone orthomosaic base layer        | Trees: 38 | Shrubs: 112         |
|  - Vector Crown Bounding Polygons (interactive hover)       | ------------------------------- |
|  - Segment Choropleth (Green: >25%, Orange: 10-25%, Red: <8%)| Diversity Breakdown (10-20-30): |
|  - Centerline Chainage Markers (every 500m)                 | - Neem: 68% [ALERT: OVER 10%]   |
|                                                             | - Peepal: 18%                   |
|  [MAP CONTROLS]                                             | - Karanj: 14%                   |
|  [x] Show Crowns  [x] Show Gaps  [x] Show Median Shrubs     | ------------------------------- |
|                                                             | Explainable Recommendation:     |
|                                                             | "Plant 85 native trees. Favor   |
|                                                             | Karanj & Jamun to rebalance     |
|                                                             | diversity. Median holds shrubs."|
|                                                             | ------------------------------- |
|                                                             | [Export CSV] [Export PDF Audit] |
+-------------------------------------------------------------+---------------------------------+
```

### 3.2 Key Dashboard Components
1. **Corridor Health Ribbon:** Top metric bar highlighting:
   - Total Highway Trees Enumerated
   - Median Shrubs Enumerated
   - Overall Corridor Canopy Coverage Percentage
   - Number of Critical Shade Gaps Flagged
   - Estimated Biomass / Carbon Stock
2. **Multi-Layer GIS Map:**
   - **Base Layers:** Drone Orthomosaic Raster, ESRI Satellite, OpenStreetMap.
   - **Vector Layers:** Individual Tree Crown Polygons (colored by morphotype), Median Shrub Polygons, $500\,\text{m}$ Corridor Segments (choropleth by canopy cover %).
   - **Interactive Popups:** Hovering over a crown displays ID, estimated crown diameter ($m$), area ($\text{m}^2$), and morphotype confidence score.
3. **Audit & Survival Compare Tool:**
   - Swipe slider tool comparing baseline drone survey (e.g., Post-Construction 2026) vs. periodic monitoring flights (e.g., 2027 Pre-Simhastha).
   - Highlights saplings planted that survived vs. saplings lost or failed.

---

## 4. Pilgrim Shade & Help Mobile Web App (PWA) Design

### 4.1 Mobile-First Viewport & Navigation
Designed for handheld smartphones with single-thumb navigation, high outdoor contrast, and instant language toggle.

```
+---------------------------------------+
| GreenCorridor | उज्जैन - इंदौर मार्ग  [EN|हिं] |
| Simhastha 2028 Chhaya & Seva Mitra    |
+---------------------------------------+
| [ LIVE HIGHWAY HEAT-RISK TRACKER ]   |
|                                       |
| Ujjain (0 KM) =======|====== इंदौर    |
| [==================!=================]|
| Green: Chhaya (Cool) | Red: Dhoop     |
|                                       |
| Current Location: Near KM 14.2        |
| Status: ☀️ अत्यधिक धूप (Extreme Sun)  |
| Nearest Chhaya: 180m ahead (Peepal)   |
+---------------------------------------+
| QUICK FILTERS:                        |
| [🌳 छाया] [💧 जल/प्याऊ] [🩺 चिकित्सा]  |
+---------------------------------------+
| [ INTERACTIVE PILGRIM MAP ]           |
|                                       |
| (Shows walking path, shade trees,     |
|  water stations, and first aid camps) |
|                                       |
+---------------------------------------+
| NEAREST HELP STATIONS:                |
| 1. Shri Mahakal Chhaya Kendra - 220m  |
|    - Water: Available (शीतल जल)       |
|    - Medical Camp: 24x7 Doctor On Duty|
| 2. Pyaau Booth No. 18 - 450m          |
+---------------------------------------+
| [ 📞 आपातकालीन हेल्पलाइन: 108 / 112 ]  |
+---------------------------------------+
```

### 4.2 Heat-Risk Index Formula (Pilgrim Rating)
The app calculates a 3-tier heat risk score for each 500-meter segment:
$$\text{Heat Risk Index (HRI)} = 1.0 - \min\left(1.0, \frac{\text{Canopy Cover (\%)}}{30.0}\right)$$
- $\text{HRI} \le 0.35$: **सुरक्षित छायादार मार्ग (Safe Shaded Stretch)** — Green badge.
- $0.35 < \text{HRI} \le 0.70$: **मध्यम धूप क्षेत्र (Moderate Sun Exposure)** — Amber badge.
- $\text{HRI} > 0.70$: **अत्यधिक धूप क्षेत्र (Extreme Sun Void)** — Red blinking badge + advice: *"कृपया पानी साथ रखें, अगला विश्राम केंद्र 300 मीटर पर है।"*

---

## 5. Micro-Animations & State Transitions
- **Segment Select Transition:** Smooth zoom-to-extent (`flyTo({ zoom: 16 })`) with $400\,\text{ms}$ ease-in-out curve.
- **Filter Chip Toggle:** Tactile scale transform (`scale(0.96)`) on tap, activating solid pill background.
- **PWA Service Worker Update Alert:** Non-intrusive floating toast at bottom: *"नया नक्शा अपडेट उपलब्ध है (New map update cached)"*.
