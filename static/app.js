/**
 * GreenCorridor Ujjain - Client Application Logic
 * Dual-View GIS Dashboard & Simhastha Pilgrim Shade Map
 */

// Global State
const state = {
  currentView: 'officials', // 'officials' | 'pilgrim'
  currentLang: 'en', // 'en' | 'hi'
  activeSegmentId: 4, // Default to a critical gap for instant inspection
  segmentsData: null,
  crownsData: null,
  amenitiesData: null,
  corridorSummary: null,
  officialsMap: null,
  pilgrimMap: null,
  layers: {
    officialsSegments: null,
    officialsCrowns: null,
    officialsAmenities: null,
    pilgrimSegments: null,
    pilgrimAmenities: null
  },
  amenityFilter: 'all'
};

// Bilingual Localization Dictionary
const i18n = {
  en: {
    headerSubtitle: "AI-Based Tree Census & Green Cover Planning | Simhastha 2028 (SH-27)",
    tabOfficials: "Officials' Analytics",
    tabPilgrim: "Pilgrim Shade Map (छाया मित्र)",
    simhasthaBadge: "Simhastha 2028 Ready",
    lblSurvey: "Surveyed Corridor",
    lblSegments: "30 segments (500m)",
    lblTrees: "Mature Trees Detected",
    lblAccuracy: "DeepForest AI | 92% Conf.",
    lblShrubs: "Median Shrubs",
    lblShrubDesc: "Bougainvillea / Nerium",
    lblCanopy: "Avg Canopy Cover",
    lblTargetCanopy: "Target: 25.0%",
    lblGaps: "Critical Shade Gaps",
    lblGapAlert: "< 8% cover (High Heat Risk)",
    lblCarbon: "Est. Biomass Carbon",
    lblCarbonNote: "Allometric approximation",
    lblLegendTitle: "Canopy Cover (% per 500m)",
    legHigh: "≥ 25% (High Shade)",
    legMod: "10% – 25% (Moderate)",
    legGap: "< 10% (Critical Shade Gap)",
    legCrown: "Detected Crown",
    chkCrownsLabel: "Tree Crown Points",
    chkAmenityLabel: "Civic Amenities",
    lblSegCanopy: "Canopy Cover",
    lblSegTrees: "Trees",
    lblSegShrubs: "Median Shrubs",
    lblSegSlots: "Planting Slots",
    lblDiversityRule: "Urban Forestry Rule (Santamour 10-20-30)",
    lblRecTitle: "Explainable Planting Prescription",
    lblPrescribedSpecies: "Prescribed Native Species:",
    lblProhibitedNote: "Prohibited: Eucalyptus (water drain) & Conocarpus (pavement root damage)",
    btnExportCsvLabel: "Export Segment CSV",
    btnExportAuditLabel: "Print Audit Summary",
    lblRouteTrackerTitle: "Ujjain – Indore Highway Shade & Heat Corridor",
    heatBarMidpoint: "KM 7.5 (Sanwer Road)",
    fltAllLabel: "All",
    fltShadeLabel: "Shade",
    fltWaterLabel: "Water",
    fltMedicalLabel: "Medical",
    fltRestLabel: "Shelter",
    lblNearestAmenities: "Nearby Simhastha Help Points",
    lblLiveStatus: "24x7 Operational",
    lblEmergencyCall: "Simhastha Emergency Helpline (Toll-Free SOS)"
  },
  hi: {
    headerSubtitle: "एआई आधारित वृक्ष गणना एवं हरित आवरण योजना | सिंहस्थ 2028 (उज्जैन-इंदौर मार्ग)",
    tabOfficials: "अधिकारी विश्लेषिकी",
    tabPilgrim: "यात्री छाया नक्शा (छाया मित्र)",
    simhasthaBadge: "सिंहस्थ 2028 तैयार",
    lblSurvey: "सर्वेक्षित राजमार्ग",
    lblSegments: "30 खंड (500 मीटर प्रत्येक)",
    lblTrees: "कुल छायादार वृक्ष",
    lblAccuracy: "डीपफॉरेस्ट एआई | 92% शुद्धता",
    lblShrubs: "डिवाइडर झाड़ियाँ",
    lblShrubDesc: "बोगनवेलिया / कनेर",
    lblCanopy: "औसत हरित आवरण",
    lblTargetCanopy: "लक्ष्य: 25.0%",
    lblGaps: "अत्यधिक धूप क्षेत्र",
    lblGapAlert: "< 8% आवरण (लू का खतरा)",
    lblCarbon: "अनुमानित बायोमास कार्बन",
    lblCarbonNote: "एलोमेट्रिक अनुमान",
    lblLegendTitle: "छाया आवरण (% प्रति 500 मी.)",
    legHigh: "≥ 25% (शीतल छाया)",
    legMod: "10% – 25% (मध्यम छाया)",
    legGap: "< 10% (अत्यधिक धूप)",
    legCrown: "चिन्हित वृक्ष",
    chkCrownsLabel: "वृक्ष बिंदु दिखाएं",
    chkAmenityLabel: "नागरिक सुविधाएं दिखाएं",
    lblSegCanopy: "हरित आवरण",
    lblSegTrees: "पेड़",
    lblSegShrubs: "झाड़ियाँ",
    lblSegSlots: "रोपण स्थान",
    lblDiversityRule: "शहरी वानिकी नियम (संतमौर 10-20-30)",
    lblRecTitle: "तर्कसंगत वृक्षारोपण निर्देश",
    lblPrescribedSpecies: "सुझाए गए स्थानीय देशी वृक्ष:",
    lblProhibitedNote: "प्रतिबंधित: यूकेलिप्टस (जल संकट) एवं कोनोकार्पस (सड़क नुकसान)",
    btnExportCsvLabel: "खंड डेटा डाउनलोड (CSV)",
    btnExportAuditLabel: "ऑडिट रिपोर्ट प्रिंट करें",
    lblRouteTrackerTitle: "उज्जैन – इंदौर मार्ग छाया एवं तापमान कॉरिडोर",
    heatBarMidpoint: "किमी 7.5 (सांवेर मार्ग)",
    fltAllLabel: "सभी",
    fltShadeLabel: "छाया",
    fltWaterLabel: "शीतल जल",
    fltMedicalLabel: "चिकित्सा",
    fltRestLabel: "विश्राम",
    lblNearestAmenities: "नजदीकी सिंहस्थ सेवा केंद्र",
    lblLiveStatus: "24x7 सक्रिय",
    lblEmergencyCall: "सिंहस्थ आपातकालीन हेल्पलाइन (टोल-फ्री SOS)"
  }
};

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  setupEventListeners();
  initOfficialsMap();
  initPilgrimMap();

  await loadData();
  renderHeatBar();
  selectSegment(state.activeSegmentId);
});

// Setup DOM Event Listeners
function setupEventListeners() {
  // View Switcher Tabs
  const tabOfficials = document.getElementById("tabOfficials");
  const tabPilgrim = document.getElementById("tabPilgrim");

  tabOfficials.addEventListener("click", () => switchView("officials"));
  tabPilgrim.addEventListener("click", () => switchView("pilgrim"));

  // Language Toggle
  document.getElementById("langToggle").addEventListener("click", toggleLanguage);

  // Map Controls
  document.getElementById("btnZoomFit").addEventListener("click", () => {
    if (state.layers.officialsSegments && state.officialsMap) {
      state.officialsMap.fitBounds(state.layers.officialsSegments.getBounds(), { padding: [30, 30] });
    }
  });

  document.getElementById("chkShowCrowns").addEventListener("change", (e) => {
    if (state.layers.officialsCrowns && state.officialsMap) {
      if (e.target.checked) state.officialsMap.addLayer(state.layers.officialsCrowns);
      else state.officialsMap.removeLayer(state.layers.officialsCrowns);
    }
  });

  document.getElementById("chkShowAmenities").addEventListener("change", (e) => {
    if (state.layers.officialsAmenities && state.officialsMap) {
      if (e.target.checked) state.officialsMap.addLayer(state.layers.officialsAmenities);
      else state.officialsMap.removeLayer(state.layers.officialsAmenities);
    }
  });

  // Pilgrim Quick Filters
  document.querySelectorAll(".filter-chip").forEach(chip => {
    chip.addEventListener("click", (e) => {
      document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
      const btn = e.currentTarget;
      btn.classList.add("active");
      state.amenityFilter = btn.dataset.filter;
      filterPilgrimAmenities();
    });
  });

  // CSV Export Button
  document.getElementById("btnExportCsv").addEventListener("click", exportCsv);
  document.getElementById("btnExportAudit").addEventListener("click", () => window.print());
}

// Switch between Officials Dashboard & Pilgrim App
function switchView(viewName) {
  state.currentView = viewName;

  const tabOfficials = document.getElementById("tabOfficials");
  const tabPilgrim = document.getElementById("tabPilgrim");
  const viewOfficials = document.getElementById("viewOfficials");
  const viewPilgrim = document.getElementById("viewPilgrim");

  if (viewName === "officials") {
    tabOfficials.classList.add("active");
    tabPilgrim.classList.remove("active");
    viewOfficials.classList.add("active");
    viewPilgrim.classList.remove("active");
    setTimeout(() => state.officialsMap.invalidateSize(), 150);
  } else {
    tabPilgrim.classList.add("active");
    tabOfficials.classList.remove("active");
    viewPilgrim.classList.add("active");
    viewOfficials.classList.remove("active");
    setTimeout(() => state.pilgrimMap.invalidateSize(), 150);
  }
}

// Language Switcher
function toggleLanguage() {
  state.currentLang = state.currentLang === "en" ? "hi" : "en";
  document.getElementById("langLabel").textContent = state.currentLang === "en" ? "हिंदी" : "English";

  const dict = i18n[state.currentLang];
  for (const [key, text] of Object.entries(dict)) {
    const el = document.getElementById(key);
    if (el) el.textContent = text;
  }

  // Update dynamic content
  selectSegment(state.activeSegmentId);
  renderAmenitiesFeed();
}

// Map 1: Officials GIS Map
function initOfficialsMap() {
  state.officialsMap = L.map("officialsMap", {
    center: [23.15, 75.80],
    zoom: 12,
    zoomControl: false
  });

  L.control.zoom({ position: "bottomright" }).addTo(state.officialsMap);

  // CartoDB Dark Matter Basemap
  L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(state.officialsMap);
}

// Map 2: Pilgrim Heat & Shade Map
function initPilgrimMap() {
  state.pilgrimMap = L.map("pilgrimMap", {
    center: [23.15, 75.80],
    zoom: 13,
    zoomControl: false
  });

  L.control.zoom({ position: "bottomright" }).addTo(state.pilgrimMap);

  L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(state.pilgrimMap);
}

// Fetch GeoJSON Datasets from API
async function loadData() {
  try {
    const [segRes, crwRes, amnRes, sumRes] = await Promise.all([
      fetch("/api/v1/corridor/segments"),
      fetch("/api/v1/crowns"),
      fetch("/api/v1/pilgrim/amenities"),
      fetch("/api/v1/stats")
    ]);

    state.segmentsData = await segRes.json();
    state.crownsData = await crwRes.json();
    state.amenitiesData = await amnRes.json();
    state.corridorSummary = await sumRes.json();

    updateSummaryRibbon();
    renderOfficialsMapLayers();
    renderPilgrimMapLayers();
    renderAmenitiesFeed();
  } catch (err) {
    console.error("Failed to load geospatial data:", err);
  }
}

// Update Top Corridor Key Metrics
function updateSummaryRibbon() {
  if (!state.corridorSummary) return;
  const s = state.corridorSummary;
  document.getElementById("valCorridorKm").innerHTML = `${s.pilot_length_km} <span class="unit">km</span>`;
  document.getElementById("valTotalTrees").textContent = s.total_trees_detected.toLocaleString();
  document.getElementById("valTotalShrubs").textContent = s.total_median_shrubs.toLocaleString();
  document.getElementById("valAvgCanopy").textContent = `${s.avg_canopy_coverage_pct}%`;
  document.getElementById("valCriticalGaps").innerHTML = `${s.critical_gaps_count} <span class="unit">zones</span>`;
  document.getElementById("valCarbonStock").innerHTML = `${(s.total_trees_detected * 0.18).toFixed(1)} <span class="unit">tC</span>`;
}

// Render Officials Map Layers
function renderOfficialsMapLayers() {
  if (!state.segmentsData) return;

  // 1. Segments Polygon Layer
  state.layers.officialsSegments = L.geoJSON(state.segmentsData, {
    style: (feature) => {
      const cov = feature.properties.canopy_percentage;
      let color = "#ef4444"; // Coral gap
      if (cov >= 25.0) color = "#10b981"; // Emerald
      else if (cov >= 10.0) color = "#f59e0b"; // Amber

      return {
        color: color,
        weight: feature.properties.segment_id === state.activeSegmentId ? 3.5 : 1.5,
        fillColor: color,
        fillOpacity: feature.properties.segment_id === state.activeSegmentId ? 0.65 : 0.35
      };
    },
    onEachFeature: (feature, layer) => {
      layer.on({
        click: () => {
          selectSegment(feature.properties.segment_id);
        },
        mouseover: (e) => {
          e.target.setStyle({ fillOpacity: 0.8 });
        },
        mouseout: (e) => {
          if (feature.properties.segment_id !== state.activeSegmentId) {
            e.target.setStyle({ fillOpacity: 0.35 });
          }
        }
      });

      layer.bindTooltip(`
        <strong>${feature.properties.chainage}</strong><br>
        Canopy: <strong>${feature.properties.canopy_percentage}%</strong><br>
        Trees: ${feature.properties.tree_count} | Priority: #${feature.properties.planting_priority}
      `, { sticky: true });
    }
  }).addTo(state.officialsMap);

  // 2. Individual Tree Crowns Layer
  if (state.crownsData) {
    state.layers.officialsCrowns = L.geoJSON(state.crownsData, {
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: Math.min(8, Math.max(3, feature.properties.diameter_m * 0.6)),
          fillColor: "#34d399",
          color: "#064e3b",
          weight: 1,
          opacity: 0.9,
          fillOpacity: 0.75
        });
      },
      onEachFeature: (feature, layer) => {
        const p = feature.properties;
        layer.bindPopup(`
          <div style="font-size: 12px; color: #1e293b; line-height: 1.4;">
            <strong style="color: #065f46;">${p.common_name}</strong><br>
            <em>${p.species}</em><br>
            Spread Diameter: <strong>${p.diameter_m} m</strong><br>
            Crown Area: <strong>${p.crown_area_sqm} m²</strong><br>
            AI Confidence: <strong>${(p.confidence * 100).toFixed(0)}%</strong>
          </div>
        `);
      }
    }).addTo(state.officialsMap);
  }

  // 3. Civic Amenities Layer
  renderOfficialsAmenities();

  state.officialsMap.fitBounds(state.layers.officialsSegments.getBounds(), { padding: [25, 25] });
}

function renderOfficialsAmenities() {
  if (!state.amenitiesData) return;
  state.layers.officialsAmenities = L.geoJSON(state.amenitiesData, {
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, {
        radius: 6,
        fillColor: "#38bdf8",
        color: "#0284c7",
        weight: 1.5,
        fillOpacity: 0.9
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.name_en}</strong><br>${p.name_hi}<br>${p.chainage}`);
    }
  }).addTo(state.officialsMap);
}

// Render Pilgrim Map Layers
function renderPilgrimMapLayers() {
  if (!state.segmentsData) return;

  state.layers.pilgrimSegments = L.geoJSON(state.segmentsData, {
    style: (feature) => {
      const cov = feature.properties.canopy_percentage;
      let color = "#ef4444";
      if (cov >= 25.0) color = "#10b981";
      else if (cov >= 10.0) color = "#f59e0b";

      return {
        color: color,
        weight: feature.properties.segment_id === state.activeSegmentId ? 4 : 2,
        fillColor: color,
        fillOpacity: 0.45
      };
    },
    onEachFeature: (feature, layer) => {
      layer.on({
        click: () => selectSegment(feature.properties.segment_id)
      });
    }
  }).addTo(state.pilgrimMap);

  renderPilgrimAmenitiesMarkers();
  state.pilgrimMap.fitBounds(state.layers.pilgrimSegments.getBounds(), { padding: [25, 25] });
}

function renderPilgrimAmenitiesMarkers() {
  if (!state.amenitiesData) return;
  if (state.layers.pilgrimAmenities) {
    state.pilgrimMap.removeLayer(state.layers.pilgrimAmenities);
  }

  state.layers.pilgrimAmenities = L.geoJSON(state.amenitiesData, {
    filter: (feature) => {
      if (state.amenityFilter === 'all') return true;
      if (state.amenityFilter === 'shade') return feature.properties.shade_available;
      return feature.properties.type === state.amenityFilter;
    },
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      let color = "#38bdf8";
      if (p.type === 'medical') color = "#f87171";
      if (p.type === 'shade_hub') color = "#10b981";

      return L.circleMarker(latlng, {
        radius: 8,
        fillColor: color,
        color: "#fff",
        weight: 2,
        fillOpacity: 0.95
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      const isHi = state.currentLang === 'hi';
      layer.bindPopup(`
        <div style="font-size: 13px; color: #1e293b;">
          <strong>${isHi ? p.name_hi : p.name_en}</strong><br>
          ${p.chainage} | <em>${p.status}</em>
        </div>
      `);
    }
  }).addTo(state.pilgrimMap);
}

function filterPilgrimAmenities() {
  renderPilgrimAmenitiesMarkers();
  renderAmenitiesFeed();
}

// Render the 30-Segment Heat Bar Tracker
function renderHeatBar() {
  const container = document.getElementById("heatBarTrack");
  if (!container || !state.segmentsData) return;
  container.innerHTML = "";

  state.segmentsData.features.forEach(feat => {
    const p = feat.properties;
    const bar = document.createElement("div");
    bar.className = "heat-seg-bar";

    let shadeClass = "shade-gap";
    if (p.canopy_percentage >= 25.0) shadeClass = "shade-high";
    else if (p.canopy_percentage >= 10.0) shadeClass = "shade-mod";

    bar.classList.add(shadeClass);
    if (p.segment_id === state.activeSegmentId) bar.classList.add("active");

    bar.title = `${p.chainage}: ${p.canopy_percentage}% Canopy`;
    bar.addEventListener("click", () => selectSegment(p.segment_id));
    container.appendChild(bar);
  });
}

// Select a segment and update all inspector UI cards
function selectSegment(segmentId) {
  state.activeSegmentId = segmentId;
  if (!state.segmentsData) return;

  const segmentFeature = state.segmentsData.features.find(f => f.properties.segment_id === segmentId);
  if (!segmentFeature) return;

  const p = segmentFeature.properties;
  const isHi = state.currentLang === 'hi';

  // Update Officials Inspector
  document.getElementById("inspectorChainage").textContent = p.chainage;
  document.getElementById("inspectorTitle").textContent = isHi ? `खंड #${p.segment_id} निरीक्षण` : `Segment #${p.segment_id} Inspection`;

  const shadeBadge = document.getElementById("inspectorShadeBadge");
  shadeBadge.textContent = p.canopy_percentage >= 25.0 ? (isHi ? "शीतल छाया" : "High Shade") : (p.canopy_percentage >= 10.0 ? (isHi ? "मध्यम छाया" : "Moderate Shade") : (isHi ? "अत्यधिक धूप" : "Critical Gap"));
  shadeBadge.className = `shade-badge ${p.canopy_percentage >= 25.0 ? 'high' : (p.canopy_percentage >= 10.0 ? 'moderate' : 'gap')}`;

  document.getElementById("inspectorCanopy").textContent = `${p.canopy_percentage}%`;
  document.getElementById("inspectorTrees").textContent = p.tree_count;
  document.getElementById("inspectorShrubs").textContent = p.median_shrub_count;
  document.getElementById("inspectorSlots").textContent = `${p.slots_available} ${isHi ? 'स्थान' : 'slots'}`;

  // Species Diversity & Santamour Rule
  const diversityBadge = document.getElementById("diversityStatusBadge");
  const alertBox = document.getElementById("diversityAlertBox");
  if (p.diversity_alert) {
    diversityBadge.className = "diversity-status alert";
    diversityBadge.textContent = isHi ? "चेतावनी (10% अधिक)" : "Alert (>10% Dominance)";
    alertBox.classList.remove("hidden");
    document.getElementById("diversityAlertText").textContent = isHi
      ? `${p.dominant_species} का अनुपात ${p.dominant_share_pct}% है जो 10% सीमा से अधिक है।`
      : `${p.dominant_species} constitutes ${p.dominant_share_pct}%, exceeding Santamour diversity rule.`;
  } else {
    diversityBadge.className = "diversity-status pass";
    diversityBadge.textContent = isHi ? "मानक अनुरूप" : "Compliant";
    alertBox.classList.add("hidden");
  }

  // Species diversity mini-bar
  renderSpeciesBar(p);

  // Recommendation Card
  document.getElementById("inspectorRecText").textContent = p.recommendation_text;
  const pillsContainer = document.getElementById("inspectorSpeciesPills");
  pillsContainer.innerHTML = "";
  p.recommended_species.forEach(sp => {
    const pill = document.createElement("span");
    pill.className = "pill-tag";
    pill.textContent = sp;
    pillsContainer.appendChild(pill);
  });

  // Update Pilgrim Guidance Banner
  const alertHead = document.getElementById("pilgrimAlertHead");
  const alertDesc = document.getElementById("pilgrimAlertDesc");
  const banner = document.getElementById("pilgrimAlertBanner");

  if (p.canopy_percentage >= 25.0) {
    banner.className = "heat-alert-banner cool";
    alertHead.textContent = isHi ? `${p.chainage}: सुरक्षित छायादार क्षेत्र` : `${p.chainage}: Well Shaded Stretch`;
    alertDesc.textContent = isHi ? `पर्याप्त छाया (${p.canopy_percentage}% आवरण)। पैदल यात्रियों के लिए सुरक्षित।` : `Abundant natural shade (${p.canopy_percentage}% canopy). Safe for walking devotees.`;
  } else {
    banner.className = "heat-alert-banner";
    alertHead.textContent = isHi ? `${p.chainage}: अत्यधिक धूप क्षेत्र` : `${p.chainage}: Scorching Sun Exposed Gap`;
    alertDesc.textContent = isHi ? `छाया केवल ${p.canopy_percentage}% है। पानी की बोतल साथ रखें। अगला सहायता केंद्र नजदीक है।` : `Canopy is only ${p.canopy_percentage}%. Carry drinking water. Nearest help point is ahead.`;
  }

  // Update Heat Bar active selection
  renderHeatBar();

  // Highlight segment on maps
  if (state.layers.officialsSegments) state.layers.officialsSegments.setStyle((f) => ({
    weight: f.properties.segment_id === segmentId ? 3.5 : 1.5,
    fillOpacity: f.properties.segment_id === segmentId ? 0.65 : 0.35
  }));

  if (state.layers.pilgrimSegments) state.layers.pilgrimSegments.setStyle((f) => ({
    weight: f.properties.segment_id === segmentId ? 4 : 2,
    fillOpacity: f.properties.segment_id === segmentId ? 0.65 : 0.45
  }));

  // Pan to segment center smoothly
  const bounds = L.geoJSON(segmentFeature).getBounds();
  state.officialsMap.panTo(bounds.getCenter());
  state.pilgrimMap.panTo(bounds.getCenter());

  renderAmenitiesFeed();
}

function renderSpeciesBar(segmentProps) {
  const bar = document.getElementById("speciesBar");
  const legend = document.getElementById("speciesLegend");
  bar.innerHTML = "";
  legend.innerHTML = "";

  const dominantShare = segmentProps.dominant_share_pct || 40;
  const otherShare = 100 - dominantShare;

  const seg1 = document.createElement("div");
  seg1.style.width = `${dominantShare}%`;
  seg1.style.background = "#34d399";
  seg1.title = `${segmentProps.dominant_species}: ${dominantShare}%`;
  bar.appendChild(seg1);

  const seg2 = document.createElement("div");
  seg2.style.width = `${otherShare}%`;
  seg2.style.background = "#059669";
  seg2.title = `Other Native Species: ${otherShare}%`;
  bar.appendChild(seg2);

  const item1 = document.createElement("div");
  item1.className = "species-legend-item";
  item1.innerHTML = `<span>● ${segmentProps.dominant_species || 'Neem'}</span> <span>${dominantShare}%</span>`;
  legend.appendChild(item1);

  const item2 = document.createElement("div");
  item2.className = "species-legend-item";
  item2.innerHTML = `<span>● Peepal / Karanj / Jamun</span> <span>${otherShare.toFixed(1)}%</span>`;
  legend.appendChild(item2);
}

// Render Pilgrim Help Points List
function renderAmenitiesFeed() {
  const feed = document.getElementById("amenitiesFeed");
  if (!feed || !state.amenitiesData) return;
  feed.innerHTML = "";

  const isHi = state.currentLang === 'hi';
  const filtered = state.amenitiesData.features.filter(f => {
    if (state.amenityFilter === 'all') return true;
    if (state.amenityFilter === 'shade') return f.properties.shade_available;
    return f.properties.type === state.amenityFilter;
  });

  filtered.slice(0, 5).forEach((feat, idx) => {
    const p = feat.properties;
    const card = document.createElement("div");
    card.className = "amenity-card";

    let iconHtml = '<i data-lucide="droplet"></i>';
    if (p.type === 'medical') iconHtml = '<i data-lucide="activity"></i>';
    if (p.type === 'shade_hub') iconHtml = '<i data-lucide="home"></i>';
    if (p.type === 'toilet') iconHtml = '<i data-lucide="bath"></i>';
    if (p.type === 'police') iconHtml = '<i data-lucide="shield"></i>';

    card.innerHTML = `
      <div class="amenity-card-icon ${p.type}">
        ${iconHtml}
      </div>
      <div class="amenity-info">
        <div class="amenity-name">${isHi ? p.name_hi : p.name_en}</div>
        <div class="amenity-meta">${p.chainage} • ${p.status}</div>
      </div>
      <div class="amenity-dist">${(idx + 1) * 120}m</div>
    `;

    card.addEventListener("click", () => {
      selectSegment(p.segment_id);
    });

    feed.appendChild(card);
  });

  if (window.lucide) window.lucide.createIcons();
}

// 1-Click CSV Export
function exportCsv() {
  if (!state.segmentsData) return;

  const rows = [
    ["Segment ID", "Chainage", "Canopy Cover (%)", "Tree Count", "Median Shrubs", "Shade Classification", "Planting Priority", "Planting Slots Needed", "Dominant Species", "Dominant Share (%)", "Recommendation"]
  ];

  state.segmentsData.features.forEach(f => {
    const p = f.properties;
    rows.push([
      p.segment_id,
      p.chainage,
      p.canopy_percentage,
      p.tree_count,
      p.median_shrub_count,
      `"${p.shade_classification}"`,
      p.planting_priority,
      p.slots_available,
      `"${p.dominant_species || 'N/A'}"`,
      p.dominant_share_pct || 0,
      `"${p.recommendation_text.replace(/"/g, '""')}"`
    ]);
  });

  const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `greencorridor_ujjain_segments_audit_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
