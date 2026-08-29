import streamlit as st
from pathlib import Path
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HeatScope — Site Intelligence",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# PATHS (Fixed as requested)
# =========================================================

ROOT = Path(__file__).resolve().parent
TARGET_DIR = ROOT / "outputs" / "parcel_diridon_san_jose_2024-07-15"
MAPS_DIR = TARGET_DIR / "maps"

FINDINGS_FILE = TARGET_DIR / "findings.csv"
DUE_DILIGENCE_PDF = TARGET_DIR / "parcel_due_diligence_report.pdf"
HEAT_INTELLIGENCE_PDF = TARGET_DIR / "heat_intelligence_parcel_diridon_san_jose_2024-07-15.pdf"

HEAT_MAP = MAPS_DIR / "parcel_heat_layer.html"
CONTEXT_MAP = MAPS_DIR / "parcel_context.html"


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

st.markdown("""
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

/* تنسيق أزرار الـ Streamlit Download عشان الكلام يبان بوضوح وما يبقاش أسود غامق */
div.stDownloadButton > button {
    background-color: #304d3a !important; /* لون أخضر متناسق مع التصميم */
    color: #ffffff !important; /* الكلام أبيض وواضح جداً */
    border: none !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}

div.stDownloadButton > button:hover {
    background-color: #26362c !important; /* لون أغمق شوية عند الوقوف بالماوس */
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
}

.evidence-copy {
    color: #747e78;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 5px;
    min-height: 58px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================

def section(kicker, title, copy=None):
    st.markdown(
        f'<div class="section-kicker">{kicker}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )
    if copy:
        st.markdown(
            f'<div class="section-copy">{copy}</div>',
            unsafe_allow_html=True
        )


def show_map(path, height=620):
    if path and path.exists():
        try:
            html_content = path.read_text(encoding="utf-8")
            st.markdown('<div class="map-shell">', unsafe_allow_html=True)
            st.components.v1.html(html_content, height=height, scrolling=False)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as error:
            st.error(f"Could not load map: {error}")
    else:
        st.warning(f"Map file not found: {path}")


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="topbar">
    <div class="wordmark">
        HeatScope
        <span>/ site intelligence</span>
    </div>
    <div class="date-pill">
        <span class="date-dot"></span>
        15 JUL 2024 · SAN JOSE
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown('<div class="eyebrow">Urban heat · parcel assessment</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    Know the heat<br>
    before you <span class="hero-accent">build.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-copy">
    A parcel-level assessment of thermal exposure, shade,
    vegetation and surface conditions — translated into
    practical design decisions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pills">
    <div class="site-pill">
        ● &nbsp; Diridon · San Jose, California
    </div>
    <div class="study-pill">
        Study window · 168 hours
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 01 SITE STATUS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "01 · Site status",
    "What should we pay attention to?",
    "The strongest signal is persistent exposure combined with limited shade."
)

st.markdown("""
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
                1.6% canopy · 26.9% impervious surface ·
                35.6 h above 27°C
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
""", unsafe_allow_html=True)


# =========================================================
# 02 AT A GLANCE
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "02 · At a glance",
    "Four numbers tell the story.",
    "A compact view of the site's main thermal and shade indicators."
)

cols = st.columns(4)

metrics = [
    ("HEAT EXPOSURE", "35.6 h", "above 27°C · 168 h window"),
    ("TREE CANOPY", "1.6%", "reference target · 15%"),
    ("IMPERVIOUS SURFACE", "26.9%", "parcel footprint ratio"),
    ("PEAK HEAT INDEX", "27.3°C", "NOAA caution band"),
]

for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)


st.markdown("""
<div class="takeaway">
    <div class="takeaway-label">
        Assessment takeaway
    </div>
    <div class="takeaway-title">
        Duration and shade matter more than the peak.
    </div>
    <div class="takeaway-copy">
        The study day does not show an extreme peak-temperature signal.
        The stronger signals are repeated heat exposure, very low tree
        canopy and limited shade at the frontage.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 03 EVIDENCE
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "03 · Evidence",
    "What is driving the priority?",
    "The decision above is based on measurable signals and findings from the site assessment file."
)

measured_evidence = [
    ("ELEVATED", "tag-warn", "Hours above 27°C", "35.6 h / 21% of the total 168-hour study window indicates sustained thermal accumulation."),
    ("ELEVATED", "tag-warn", "Longest consecutive run", "6.5 hours of continuous exposure above the threshold requires tactical shading interventions."),
    ("ELEVATED", "tag-warn", "Impervious surface", "26.9% surface coverage amplifies local heat retention and re-radiation within the parcel."),
    ("BELOW TARGET", "tag-warn", "Tree canopy", "1.6% current canopy falls significantly short of the 15% reference target, limiting natural cooling.")
]

extra_findings = []
if not findings.empty:
    cols_list = list(findings.columns)
    for _, row in findings.iterrows():
        status = str(row.iloc[0]) if len(cols_list) > 0 else "ELEVATED"
        title = str(row.iloc[1]) if len(cols_list) > 1 else str(row.iloc[0])
        desc = str(row.iloc[2]) if len(cols_list) > 2 else ""
        tag_class = "tag-good" if "GOOD" in status.upper() or "RECOVER" in status.upper() else "tag-warn"
        extra_findings.append((status, tag_class, title, desc))

all_evidence_items = measured_evidence + extra_findings

left, right = st.columns(2)
half_len = (len(all_evidence_items) + 1) // 2

with left:
    for status, tag_class, title, desc in all_evidence_items[:half_len]:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

with right:
    for status, tag_class, title, desc in all_evidence_items[half_len:]:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)


# =========================================================
# 04 SPATIAL ANALYSIS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "04 · Spatial analysis",
    "Where does the heat sit?",
    "Move from a site-level number to the spatial pattern around the parcel."
)

show_map(HEAT_MAP, 620)

st.markdown(
    '<div class="map-caption">'
    'HEAT LAYER · INTERACTIVE · PARCEL + SURROUNDING CONTEXT'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 05 DECISION
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "05 · Decision",
    "What should change?",
    "Each recommendation is tied directly to one of the observed signals."
)

actions = [
    ("01", "Increase canopy", "Add a planting strategy and quantify the expected canopy benefit before entitlement decisions.", "↳ Evidence · 1.6% canopy vs 15% reference"),
    ("02", "Improve pedestrian shade", "Consider street trees or a shade structure where ground-floor active uses are planned.", "↳ Evidence · 6.5% frontage vegetation"),
    ("03", "Design for sustained heat", "Model annual exposure and prioritize envelope performance for sustained thermal load.", "↳ Evidence · 35.6 h above 27°C"),
    ("04", "Re-check a summer design day", "Re-run the comfort assessment against a summer design day before final design decisions.", "↳ Evidence · current study-day snapshot"),
]

for start in (0, 2):
    c1, c2 = st.columns(2)
    for col, action in zip((c1, c2), actions[start:start + 2]):
        with col:
            num, title, copy, evidence = action
            st.markdown(f"""
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
            """, unsafe_allow_html=True)


# =========================================================
# 06 SITE CONTEXT
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "06 · Site context",
    "The parcel in context.",
    "Understand the surrounding urban fabric before deciding where intervention matters most."
)

show_map(CONTEXT_MAP, 620)

st.markdown(
    '<div class="map-caption">'
    'SITE CONTEXT · INTERACTIVE · PARCEL + URBAN FABRIC'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 07 EVIDENCE / DOWNLOADS
# =========================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

section(
    "07 · Evidence",
    "Take the analysis with you.",
    "The dashboard is the quick read. The reports and structured findings provide the supporting evidence."
)

e1, e2, e3 = st.columns(3)

with e1:
    st.markdown("""
    <div class="evidence">
        <div class="evidence-title">
            Site due-diligence report
        </div>
        <div class="evidence-copy">
            Branded assessment with findings,
            methodology, maps and limitations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if DUE_DILIGENCE_PDF.exists():
        st.download_button(
            "Download report ↓",
            data=DUE_DILIGENCE_PDF.read_bytes(),
            file_name=DUE_DILIGENCE_PDF.name,
            mime="application/pdf",
            use_container_width=True,
            key="dl1"
        )
    else:
        st.info("Report not available.")

with e2:
    st.markdown("""
    <div class="evidence">
        <div class="evidence-title">
            Heat intelligence report
        </div>
        <div class="evidence-copy">
            Supporting FortyGuard heat-intelligence
            output for the site.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if HEAT_INTELLIGENCE_PDF.exists():
        st.download_button(
            "Download report ↓",
            data=HEAT_INTELLIGENCE_PDF.read_bytes(),
            file_name=HEAT_INTELLIGENCE_PDF.name,
            mime="application/pdf",
            use_container_width=True,
            key="dl2"
        )
    else:
        st.info("Report not available.")

with e3:
    st.markdown("""
    <div class="evidence">
        <div class="evidence-title">
            Structured findings
        </div>
        <div class="evidence-copy">
            Raw findings used to support the dashboard interpretation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if FINDINGS_FILE.exists():
        st.download_button(
            "Download findings ↓",
            data=FINDINGS_FILE.read_bytes(),
            file_name="findings.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl3"
        )
        if not findings.empty:
            with st.expander("View findings.csv"):
                st.dataframe(findings, use_container_width=True, hide_index=True)
    else:
        st.info("Findings file not available.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer"
     style="
        border-top: 1px solid #e2e6e1;
        margin-top: 65px;
        padding-top: 18px;
        color: #9aa29c;
        font-size: 10px;
        display: flex;
        justify-content: space-between;
       ">
    <span>
        HeatScope · Diridon, San Jose
    </span>
    <span>
        FortyGuard tOS Enterprise data · 15 Jul 2024
    </span>
</div>
""", unsafe_allow_html=True)