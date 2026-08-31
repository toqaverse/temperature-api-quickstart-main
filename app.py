from pathlib import Path
import pandas as pd
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HeatScope",
    page_icon="🌡️🌞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent

TARGET_DIR = ROOT / "outputs" / "parcel_diridon_san_jose_2024-07-15"
MAPS_DIR = TARGET_DIR / "maps"

PARCEL_FILE = TARGET_DIR / "parcel_evaluation.csv"
FINDINGS_FILE = TARGET_DIR / "findings.csv"

DUE_DILIGENCE_PDF = TARGET_DIR / "parcel_due_diligence_report.pdf"
HEAT_INTELLIGENCE_PDF = (
    TARGET_DIR / "heat_intelligence_parcel_diridon_san_jose_2024-07-15.pdf"
)

HEAT_MAP = MAPS_DIR / "parcel_heat_layer.html"
CONTEXT_MAP = MAPS_DIR / "parcel_context.html"

# =========================================================
# LOAD PARCEL DATA
# =========================================================

if PARCEL_FILE.exists():
    try:
        parcel = pd.read_csv(PARCEL_FILE)

        if parcel.empty:
            st.error("parcel_evaluation.csv is empty.")
            st.stop()

        row = parcel.iloc[0]

    except Exception as error:
        st.error(f"Could not read parcel_evaluation.csv: {error}")
        st.stop()

else:
    st.error(
        "parcel_evaluation.csv was not found.\n\n"
        f"Expected location: {PARCEL_FILE}"
    )
    st.stop()

# =========================================================
# SAFE DATA HELPERS
# =========================================================


def get_number(column, default=0.0):
    try:
        value = row[column]
        return float(value)
    except Exception:
        return default


def get_text(column, default=""):
    try:
        return str(row[column])
    except Exception:
        return default


# =========================================================
# PARCEL VALUES
# =========================================================

parcel_name = get_text("name", "Diridon Gateway Site")
city = get_text("city", "San Jose")
state = get_text("state", "CA")
study_date = get_text("study_date", "2024-07-15")

window_hours = get_number("window_hours", 168)
exceedance_hours = get_number("exceedance_hours", 0)
exceedance_share = get_number("exceedance_share_pct", 0)
persistence_hours = get_number("persistence_hours", 0)

impervious_pct = get_number("impervious_pct", 0)
canopy_pct = get_number("canopy_pct", 0)
vegetation_pct = get_number("vegetation_pct", 0)
streetview_vegetation_pct = get_number("streetview_vegetation_pct", 0)

parcel_peak = get_number("parcel_peak_c", 0)
parcel_mean = get_number("parcel_mean_c", 0)
parcel_min = get_number("parcel_min_c", 0)

heat_index = get_number("heat_index_at_hot_hour_c", 0)
peak_apparent = get_number("peak_apparent_temp_c", 0)
peak_wet_bulb = get_number("peak_wet_bulb_c", 0)

hot_hour = get_number("hot_hour", 13)

# =========================================================
# LOAD FINDINGS
# =========================================================

if FINDINGS_FILE.exists():
    try:
        findings = pd.read_csv(FINDINGS_FILE)
    except Exception:
        findings = pd.DataFrame()
else:
    findings = pd.DataFrame()

# =========================================================
# DESIGN — CSS
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #17201b;
    --muted: #69736d;
    --soft: #929b95;
    --line: #e2e6e1;
    --paper: #fafbf8;
    --card: #ffffff;
    --green: #304d3a;
    --green-dark: #26362c;
    --sage: #e9efe8;
    --olive: #65765e;
    --amber: #b66b2c;
    --amber-bg: #fff1e3;
}

.stApp {
    background: var(--paper);
    color: var(--ink);
}

.block-container {
    max-width: 1180px;
    padding: 30px 42px 80px 42px;
}

#MainMenu, footer, header {
    visibility: hidden;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

h1, h2, h3 {
    font-family: "Manrope", sans-serif !important;
}

div.stDownloadButton > button {
    background-color: #304d3a !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}

div.stDownloadButton > button:hover {
    background-color: #26362c !important;
    color: #ffffff !important;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0 48px 0;
}

.wordmark {
    font-family: "Manrope", sans-serif;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--ink);
}

.wordmark span {
    color: #929a94;
    font-weight: 500;
    margin-left: 5px;
}

.date-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--line);
    background: white;
    border-radius: 999px;
    padding: 8px 14px;
    color: #68716b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .04em;
}

.date-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #607d63;
}

.eyebrow {
    color: var(--amber);
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .16em;
    margin-bottom: 13px;
}

.hero {
    font-family: "Manrope", sans-serif;
    font-size: 58px;
    line-height: 1.01;
    font-weight: 800;
    letter-spacing: -.06em;
    max-width: 820px;
    margin: 0;
    color: var(--ink);
}

.hero-accent {
    color: #65765e;
}

.hero-copy {
    max-width: 700px;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.75;
    margin-top: 19px;
}

.pills {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
    margin-top: 25px;
}

.site-pill {
    display: inline-flex;
    padding: 9px 15px;
    border-radius: 999px;
    background: var(--green);
    color: white;
    font-size: 12px;
    font-weight: 700;
}

.study-pill {
    display: inline-flex;
    padding: 9px 15px;
    border-radius: 999px;
    background: #edf1ec;
    color: #59665d;
    font-size: 12px;
    font-weight: 700;
}

.rule {
    height: 1px;
    background: var(--line);
    margin: 60px 0 34px 0;
}

.section-kicker {
    color: #8a938d;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .17em;
    margin-bottom: 8px;
}

.section-title {
    font-family: "Manrope", sans-serif;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.045em;
    margin-bottom: 5px;
    color: var(--ink);
}

.section-copy {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.65;
}

.priority-card {
    margin-top: 25px;
    background: var(--green-dark);
    border-radius: 22px;
    padding: 30px 32px;
    color: white;
    position: relative;
    overflow: hidden;
}

.priority-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.priority-label {
    color: #b9c7bd;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .15em;
}

.priority-badge {
    background: #fff1e3;
    color: #9a5d26;
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
}

.priority-title {
    font-family: "Manrope", sans-serif;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.04em;
    margin-top: 18px;
}

.priority-copy {
    color: #d4ddd7;
    max-width: 720px;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 7px;
}

.priority-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 24px;
}

.priority-box {
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.035);
    border-radius: 14px;
    padding: 15px;
}

.priority-box-label {
    color: #9eafa3;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 7px;
}

.priority-box-value {
    color: #eef2ef;
    font-size: 12px;
    line-height: 1.55;
}

.metric {
    position: relative;
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
    box-shadow: 0 5px 20px rgba(31,43,36,.025);
}

.metric:before {
    content: "";
    position: absolute;
    left: 0;
    top: 20px;
    width: 3px;
    height: 31px;
    border-radius: 0 4px 4px 0;
    background: var(--olive);
}

.metric-label {
    color: #7c857f;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .11em;
    margin-bottom: 19px;
    padding-left: 8px;
}

.metric-value {
    font-family: "Manrope", sans-serif;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -.045em;
    color: var(--ink);
}

.metric-note {
    color: #919a94;
    font-size: 11px;
    margin-top: 4px;
}

.takeaway {
    margin-top: 22px;
    background: #26362c;
    border-radius: 20px;
    padding: 27px 30px;
    color: white;
}

.takeaway-label {
    color: #bdcabe;
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: 10px;
    font-weight: 800;
}

.takeaway-title {
    font-family: "Manrope", sans-serif;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -.035em;
    margin: 9px 0 7px;
}

.takeaway-copy {
    color: #d5ddd7;
    max-width: 790px;
    font-size: 13px;
    line-height: 1.65;
}

.finding {
    background: white;
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 20px 21px;
    min-height: 150px;
    margin-bottom: 13px;
}

.tag {
    display: inline-block;
    border-radius: 999px;
    padding: 5px 8px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .08em;
    margin-bottom: 11px;
}

.tag-warn {
    color: #986022;
    background: var(--amber-bg);
}

.tag-good {
    color: #49634e;
    background: #e8f0e8;
}

.finding-title {
    font-family: "Manrope", sans-serif;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: -.025em;
    margin-bottom: 6px;
    color: var(--ink);
}

.finding-copy {
    color: #707a74;
    font-size: 12.5px;
    line-height: 1.6;
}

.map-shell {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 7px;
    margin-top: 20px;
    overflow: hidden;
    box-shadow: 0 7px 24px rgba(31,43,36,.035);
}

.map-caption {
    margin-top: 11px;
    color: #8b948e;
    font-size: 10px;
    letter-spacing: .08em;
    font-weight: 700;
}

.action {
    background: #f1f3ef;
    border: 1px solid #e0e5de;
    border-radius: 17px;
    padding: 21px;
    min-height: 175px;
    margin-bottom: 14px;
}

.action-no {
    color: var(--amber);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .12em;
}

.action-title {
    font-family: "Manrope", sans-serif;
    font-size: 17px;
    font-weight: 800;
    margin: 10px 0 6px;
    color: var(--ink);
}

.action-copy {
    color: #68736c;
    font-size: 12.5px;
    line-height: 1.6;
}

.action-evidence {
    margin-top: 13px;
    color: #637066;
    font-size: 10px;
    font-weight: 700;
}

.evidence {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 21px;
    min-height: 175px;
}

.evidence-title {
    font-family: "Manrope", sans-serif;
    font-weight: 800;
    font-size: 15px;
    color: var(--ink);
}

.evidence-copy {
    color: #747e78;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 5px;
    min-height: 58px;
}

.footer {
    border-top: 1px solid #e2e6e1;
    margin-top: 65px;
    padding-top: 18px;
    color: #9aa29c;
    font-size: 10px;
    display: flex;
    justify-content: space-between;
}

/* Professional Data Table Styling */
div[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #d4dccd;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 10px 30px rgba(48, 77, 58, 0.06);
}

div[data-testid="stDataFrame"] iframe {
    background-color: #ffffff !important;
}

.dataframe {
    font-family: "DM Sans", sans-serif !important;
    border-collapse: collapse !important;
    width: 100% !important;
}

.dataframe th {
    background-color: #26362c !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 12px 16px !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    border-top: none !important;
}

.dataframe td {
    color: #17201b !important;
    background-color: #ffffff !important;
    padding: 10px 16px !important;
    border-bottom: 1px solid #e9efe8 !important;
    font-size: 13px !important;
}

.dataframe tr:hover td {
    background-color: #f4f7f3 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================


def section(kicker, title, copy=None):
    html_content = (
        f'<div class="section-kicker">{kicker}</div>'
        f'<div class="section-title">{title}</div>'
    )
    if copy:
        html_content += f'<div class="section-copy">{copy}</div>'
    st.markdown(html_content, unsafe_allow_html=True)


def show_map(path, height=620):
    if path.exists():
        try:
            html_content = path.read_text(encoding="utf-8")
            st.markdown('<div class="map-shell">', unsafe_allow_html=True)
            st.components.v1.html(html_content, height=height, scrolling=False)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as error:
            st.error(f"Could not load map: {error}")
    else:
        st.warning(f"Map file not found: {path}")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
<div class="topbar">
    <div class="wordmark">
        HeatScope🌞<span>
    </div>
    <div class="date-pill">
        <span class="date-dot"></span>
        {study_date} · {city.upper()}
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="eyebrow">Urban heat · parcel assessment</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
    Know the heat<br>
    before you <span class="hero-accent">build.</span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-copy">
    A parcel-level assessment of thermal exposure, shade,
    vegetation and surface conditions — translated into
    practical design decisions.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="pills">
    <div class="site-pill">
        ● &nbsp; {parcel_name} · {city}, {state}
    </div>
    <div class="study-pill">
        Study window · {int(window_hours)} hours
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 01 SITE STATUS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "01 · Site status",
    "What should we pay attention to?",
    "The strongest signal is persistent exposure combined with limited shade.",
)

st.markdown(
    f"""
<div class="priority-card">
    <div class="priority-top">
        <div class="priority-label">
            Site priority
        </div>
        <div class="priority-badge">
            HIGH PRIORITY
        </div>
    </div>
    <div class="priority-title">
        Shade + canopy
    </div>
    <div class="priority-copy">
        The site's clearest intervention opportunity is increasing
        shade where people move and gather, while expanding tree canopy.
    </div>
    <div class="priority-grid">
        <div class="priority-box">
            <div class="priority-box-label">
                Why
            </div>
            <div class="priority-box-value">
                {canopy_pct:.1f}% canopy ·
                {impervious_pct:.1f}% impervious surface ·
                {exceedance_hours:.1f} h above 27°C
            </div>
        </div>
        <div class="priority-box">
            <div class="priority-box-label">
                Recommended
            </div>
            <div class="priority-box-value">
                Street trees, increased canopy and/or
                pedestrian shade structures.
            </div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 02 AT A GLANCE
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "02 · At a glance",
    "Four numbers tell the story.",
    "A compact view of the site's main thermal and shade indicators.",
)

cols = st.columns(4)

metrics = [
    (
        "HEAT EXPOSURE",
        f"{exceedance_hours:.1f} h",
        f"above 27°C · {int(window_hours)} h window",
    ),
    ("TREE CANOPY", f"{canopy_pct:.1f}%", "reference target · 15%"),
    ("IMPERVIOUS SURFACE", f"{impervious_pct:.1f}%", "site vicinity"),
    ("PEAK HEAT INDEX", f"{heat_index:.1f}°C", "NOAA caution band"),
]

for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""
<div class="metric">
    <div class="metric-label">
        {label}
    </div>
    <div class="metric-value">
        {value}
    </div>
    <div class="metric-note">
        {note}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown(
    """
<div class="takeaway">
    <div class="takeaway-label">
        Assessment takeaway
    </div>
    <div class="takeaway-title">
        Duration and shade matter more than the peak.
    </div>
    <div class="takeaway-copy">
        The study period does not show an extreme peak-temperature signal.
        The stronger signals are repeated heat exposure, very low tree
        canopy and limited shade at the frontage.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 03 EVIDENCE
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "03 · Evidence",
    "What is driving the priority?",
    "The decision above is based on measurable signals from the site assessment.",
)

measured_evidence = [
    (
        "ELEVATED",
        "tag-warn",
        "Hours above 27°C",
        f"{exceedance_hours:.1f} h / {exceedance_share:.1f}% of the "
        f"{int(window_hours)}-hour study window indicates sustained thermal"
        " exposure.",
    ),
    (
        "ELEVATED",
        "tag-warn",
        "Longest consecutive run",
        f"{persistence_hours:.1f} hours of continuous exposure above "
        "the threshold suggests a need for tactical shading.",
    ),
    (
        "ELEVATED",
        "tag-warn",
        "Impervious surface",
        f"{impervious_pct:.1f}% surface coverage in the site vicinity.",
    ),
    (
        "BELOW TARGET",
        "tag-warn",
        "Tree canopy",
        f"{canopy_pct:.1f}% current canopy compared with a 15% reference"
        " target.",
    ),
    (
        "BELOW",
        "tag-warn",
        "Ground-level vegetation",
        f"{streetview_vegetation_pct:.1f}% frontage vegetation in the field of"
        " view.",
    ),
    (
        "CAUTION BAND",
        "tag-warn",
        "Heat index at hot hour",
        f"{heat_index:.1f}°C at approximately {int(hot_hour):02d}:00.",
    ),
    (
        "BELOW",
        "tag-good",
        "Peak wet-bulb temperature",
        f"{peak_wet_bulb:.1f}°C, below the 26°C evaporative-cooling reference.",
    ),
]

left, right = st.columns(2)
half_len = (len(measured_evidence) + 1) // 2

with left:
    for status, tag_class, title, desc in measured_evidence[:half_len]:
        st.markdown(
            f"""
<div class="finding">
    <div class="tag {tag_class}">
        {status}
    </div>
    <div class="finding-title">
        {title}
    </div>
    <div class="finding-copy">
        {desc}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

with right:
    for status, tag_class, title, desc in measured_evidence[half_len:]:
        st.markdown(
            f"""
<div class="finding">
    <div class="tag {tag_class}">
        {status}
    </div>
    <div class="finding-title">
        {title}
    </div>
    <div class="finding-copy">
        {desc}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

# =========================================================
# 04 SPATIAL ANALYSIS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "04 · Spatial analysis",
    "Where does the heat sit?",
    "Move from a site-level number to the spatial pattern around the parcel.",
)

show_map(HEAT_MAP, 620)

st.markdown(
    '<div class="map-caption">'
    "HEAT LAYER · INTERACTIVE · PARCEL + SURROUNDING CONTEXT"
    "</div>",
    unsafe_allow_html=True,
)

# =========================================================
# 05 DECISION
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "05 · Decision",
    "What should change?",
    "Each recommendation is tied directly to one of the observed signals.",
)

actions = [
    (
        "01",
        "Increase canopy",
        "Add a planting strategy and quantify the expected canopy benefit "
        "before entitlement decisions.",
        f"↳ Evidence · {canopy_pct:.1f}% canopy vs 15% reference",
    ),
    (
        "02",
        "Improve pedestrian shade",
        "Consider street trees or a shade structure where ground-floor "
        "active uses are planned.",
        f"↳ Evidence · {streetview_vegetation_pct:.1f}% frontage vegetation",
    ),
    (
        "03",
        "Design for sustained heat",
        "Model annual exposure and prioritize envelope performance for "
        "sustained thermal load.",
        f"↳ Evidence · {exceedance_hours:.1f} h above 27°C",
    ),
    (
        "04",
        "Re-check a summer design day",
        "Re-run the comfort assessment against a summer design day "
        "before final design decisions.",
        "↳ Evidence · current study-period snapshot",
    ),
]

for start in (0, 2):
    c1, c2 = st.columns(2)
    for col, action in zip((c1, c2), actions[start : start + 2]):
        with col:
            num, title, copy, evidence = action
            st.markdown(
                f"""
<div class="action">
    <div class="action-no">
        {num}
    </div>
    <div class="action-title">
        {title}
    </div>
    <div class="action-copy">
        {copy}
    </div>
    <div class="action-evidence">
        {evidence}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

# =========================================================
# 06 SITE CONTEXT
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "06 · Site context",
    "The parcel in context.",
    (
        "Understand the surrounding urban fabric before deciding where"
        " intervention matters most."
    ),
)

show_map(CONTEXT_MAP, 620)

st.markdown(
    '<div class="map-caption">'
    "SITE CONTEXT · INTERACTIVE · PARCEL + URBAN FABRIC"
    "</div>",
    unsafe_allow_html=True,
)

# =========================================================
# 07 EVIDENCE / DOWNLOADS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "07 · Evidence",
    "Take the analysis with you.",
    (
        "The dashboard is the quick read. The reports and structured findings"
        " provide the supporting evidence."
    ),
)

e1, e2, e3 = st.columns(3)

with e1:
    st.markdown(
        """
<div class="evidence">
    <div class="evidence-title">
        Site due-diligence report
    </div>
    <div class="evidence-copy">
        Branded assessment with findings,
        methodology, maps and limitations.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    if DUE_DILIGENCE_PDF.exists():
        st.download_button(
            "Download report ↓",
            data=DUE_DILIGENCE_PDF.read_bytes(),
            file_name=DUE_DILIGENCE_PDF.name,
            mime="application/pdf",
            use_container_width=True,
            key="dl1",
        )
    else:
        st.info("Report not available.")

with e2:
    st.markdown(
        """
<div class="evidence">
    <div class="evidence-title">
        Heat intelligence report
    </div>
    <div class="evidence-copy">
        Supporting FortyGuard heat-intelligence
        output for the site.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    if HEAT_INTELLIGENCE_PDF.exists():
        st.download_button(
            "Download report ↓",
            data=HEAT_INTELLIGENCE_PDF.read_bytes(),
            file_name=HEAT_INTELLIGENCE_PDF.name,
            mime="application/pdf",
            use_container_width=True,
            key="dl2",
        )
    else:
        st.info("Report not available.")

with e3:
    st.markdown(
        """
<div class="evidence">
    <div class="evidence-title">
        Structured findings
    </div>
    <div class="evidence-copy">
        Raw findings used to support the dashboard interpretation.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    if FINDINGS_FILE.exists():
        st.download_button(
            "Download findings ↓",
            data=FINDINGS_FILE.read_bytes(),
            file_name="findings.csv",
            mime="application/csv",
            use_container_width=True,
            key="dl3",
        )
    else:
        st.info("Findings file not available.")

# =========================================================
# 08 · DATA TABLE
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "08 · Data Table",
    "Site assessment data",
    "A structured view of the main metrics used in the HeatScope assessment."
)

if PARCEL_FILE.exists():

    try:
        df_full = pd.read_csv(PARCEL_FILE, encoding="utf-8")

        if not df_full.empty:

            row = df_full.iloc[0]

            # -------------------------------------------------
            # SITE INFORMATION
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Site information</div>',
                unsafe_allow_html=True
            )

            site_data = {
                "Site": row.get("name", "—"),
                "Address": row.get("address", "—"),
                "City": row.get("city", "—"),
                "State": row.get("state", "—"),
                "Zoning": row.get("zoning", "—"),
                "Proposed use": row.get("proposed_use", "—"),
                "Study date": row.get("study_date", "—"),
                "Study window": f'{row.get("window_hours", "—")} hours',
            }

            st.dataframe(
                pd.DataFrame(
                    list(site_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # THERMAL CONDITIONS
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Thermal conditions</div>',
                unsafe_allow_html=True
            )

            thermal_data = {
                "Parcel peak temperature": f'{row.get("parcel_peak_c", "—")} °C',
                "Parcel mean temperature": f'{row.get("parcel_mean_c", "—")} °C',
                "Parcel minimum temperature": f'{row.get("parcel_min_c", "—")} °C',
                "Diurnal temperature swing": f'{row.get("diurnal_swing_c", "—")} °C',
                "City temperature difference": f'{row.get("city_delta_c", "—")} °C',
            }

            st.dataframe(
                pd.DataFrame(
                    list(thermal_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # HEAT EXPOSURE
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Heat exposure</div>',
                unsafe_allow_html=True
            )

            exposure_data = {
                "Threshold": f'{row.get("exceedance_threshold_c", "—")} °C',
                "Hours above threshold": f'{row.get("exceedance_hours", "—")} h',
                "Share of study window": f'{row.get("exceedance_share_pct", "—")}%',
                "Longest exposure run": f'{row.get("persistence_hours", "—")} h',
                "Study window": f'{row.get("window_hours", "—")} h',
            }

            st.dataframe(
                pd.DataFrame(
                    list(exposure_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # SURFACE & VEGETATION
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Surface & vegetation</div>',
                unsafe_allow_html=True
            )

            surface_data = {
                "Impervious surface": f'{row.get("impervious_pct", "—")}%',
                "Tree canopy": f'{row.get("canopy_pct", "—")}%',
                "Vegetation": f'{row.get("vegetation_pct", "—")}%',
                "Frontage vegetation": f'{row.get("streetview_vegetation_pct", "—")}%',
                "Street-view sky": f'{row.get("streetview_sky_pct", "—")}%',
            }

            st.dataframe(
                pd.DataFrame(
                    list(surface_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # HEAT INDEX
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Heat index & moisture</div>',
                unsafe_allow_html=True
            )

            heat_index_data = {
                "Hot hour": f'{row.get("hot_hour", "—")}:00',
                "Heat index at hot hour": f'{row.get("heat_index_at_hot_hour_c", "—")} °C',
                "Peak apparent temperature": f'{row.get("peak_apparent_temp_c", "—")} °C',
                "Peak wet-bulb temperature": f'{row.get("peak_wet_bulb_c", "—")} °C',
                "Maximum heat index": f'{row.get("heat_index_series_max_c", "—")} °C',
                "Maximum heat index hour": f'{row.get("heat_index_series_max_hour", "—")}:00',
            }

            st.dataframe(
                pd.DataFrame(
                    list(heat_index_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # SPATIAL DATA
            # -------------------------------------------------

            st.markdown(
                '<div class="table-section-title">Spatial data</div>',
                unsafe_allow_html=True
            )

            spatial_data = {
                "Latitude": row.get("centroid_lat", "—"),
                "Longitude": row.get("centroid_lon", "—"),
                "Lot area": f'{row.get("lot_area_m2", "—")} m²',
                "Lot area acres": f'{row.get("lot_area_acres", "—")} acres',
                "Analysis buffer": f'{row.get("aoi_buffer_m", "—")} m',
                "AOI area": f'{row.get("aoi_km2", "—")} km²',
                "Spatial granularity": f'{row.get("granularity_m", "—")} m',
            }

            st.dataframe(
                pd.DataFrame(
                    list(spatial_data.items()),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning("The data file is empty.")

    except Exception as e:
        st.error(f"Error reading the data file: {e}")

else:
    st.warning("Data file not found.")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    f"""
<div class="footer">
    <span>
        HeatScope · {city}, {state}
    </span>
    <span>
        FortyGuard temperature data · {study_date}
    </span>
</div>
""",
    unsafe_allow_html=True,
)
