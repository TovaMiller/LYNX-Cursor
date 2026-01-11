import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date

# ============================================
# CUSTOM CSS - PALANTIR GOTHAM / WAYVE STYLE
# ============================================
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1400px;
    }
    
    /* Header - Professional, minimal */
    h1 {
        color: #1A1D29;
        font-weight: 600;
        font-size: 2rem;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 0.75rem;
    }
    
    h2 {
        color: #2C3E50;
        font-weight: 600;
        font-size: 1.5rem;
        letter-spacing: -0.01em;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #34495E;
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Sidebar - Professional gray */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E5E7EB;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #2C3E50;
    }
    
    /* Metrics - Clean cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #1A1D29;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #6B7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Risk badges - Professional, minimal */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .risk-low {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    
    .risk-medium {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }
    
    .risk-high {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FECACA;
    }
    
    .risk-critical {
        background-color: #FEE2E2;
        color: #7F1D1D;
        border: 1px solid #FCA5A5;
        font-weight: 700;
    }
    
    /* Tables - Clean, professional */
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 6px;
    }
    
    /* Tabs - Professional styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #6B7280;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0066CC;
        border-bottom-color: #0066CC;
        font-weight: 600;
    }
    
    /* Buttons and inputs */
    .stButton>button {
        background-color: #0066CC;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
    }
    
    .stButton>button:hover {
        background-color: #0052A3;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #FAFBFC;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0066CC;
        background-color: #F0F7FF;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #F0F7FF;
        border-left: 3px solid #0066CC;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Section dividers */
    .section-divider {
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
        border: none;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-success { background-color: #10B981; }
    .status-warning { background-color: #F59E0B; }
    .status-error { background-color: #EF4444; }
    .status-info { background-color: #0066CC; }
    
    /* Professional card style */
    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Remove emoji styling from headers */
    h1::before, h2::before, h3::before {
        content: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Lynx Resource Planning",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# HEADER - Professional, minimal
# ============================================
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.25rem;">Lynx Resource Planning</h1>
    <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">Intelligent skill-based resource allocation and capacity planning</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================
def to_date(v):
    if pd.isna(v) or v is None:
        return None
    if isinstance(v, (datetime, date)):
        return v.date() if isinstance(v, datetime) else v
    try:
        return pd.to_datetime(v).date()
    except Exception:
        return None

def size_to_effort(s):
    """
    Map T-shirt size (XS-XL) to FTE (Full-Time Equivalent) days.
    
    T-shirt sizes represent relative effort:
    XS = 0.5 FTE days
    S = 1.0 FTE days
    M = 2.0 FTE days
    L = 4.0 FTE days
    XL = 8.0 FTE days
    
    Also supports numeric format (1-5) as fallback.
    """
    # Primary: Text T-shirt sizes (XS-XL) to FTE days
    text_mapping = {"XS": 0.5, "S": 1.0, "M": 2.0, "L": 4.0, "XL": 8.0}
    # Fallback: Numeric T-shirt sizes (1-5) to FTE days
    numeric_mapping = {1: 0.5, 2: 1.0, 3: 2.0, 4: 4.0, 5: 8.0}
    
    if pd.isna(s):
        return 2.0  # Default to Medium (M)
    
    # Try text format first (primary input format)
    s_str = str(s).strip().upper()
    if s_str in text_mapping:
        return text_mapping[s_str]
    
    # Fallback: Try numeric format
    try:
        num_val = int(float(s))
        if 1 <= num_val <= 5:
            return numeric_mapping[num_val]
    except (ValueError, TypeError):
        pass
    
    # Default to Medium (M = 2.0 FTE days)
    return 2.0

def parse_skills_importance_cell(v, max_items: int = 3):
    """Parse skills and importance from cell.
    
    Supports formats:
    - "Systems Engineering (5); Product Management (4); Effective Communication (4)"
    - "1. Requirements Engineering - 5\n2. ADAS System Knowledge - 4"
    - "Skill Name (5)" or "Skill Name - 5"
    """
    if v is None or (isinstance(v, float) and np.isnan(v)) or pd.isna(v):
        return []
    s = str(v).strip()
    if not s:
        return []
    
    # Split by semicolon (primary) or newline
    parts = re.split(r";\s*|[\n\r]+", s)
    out = []
    
    for p in parts:
        p = str(p).strip()
        if not p:
            continue
        
        # Priority 1: Format "Skill Name (5)" - parentheses with importance
        m1 = re.match(r"^\s*(.+?)\s*\(\s*(\d+(?:\.\d+)?)\s*\)\s*$", p)
        if m1:
            skill = m1.group(1).strip()
            imp = float(m1.group(2))
            if skill:
                out.append({"skill": skill, "skill_importance": imp})
                if len(out) >= max_items:
                    break
                continue
        
        # Priority 2: Format "1. Skill Name - 5" or "Skill Name - 5" (with dash/en dash/em dash/colon)
        m2 = re.match(r"^\s*(?:\d+\s*[\.|\)]\s*)?(.*?)\s*[-–—:]\s*(\d+(?:\.\d+)?)\s*$", p)
        if m2:
            skill = m2.group(1).strip()
            imp = float(m2.group(2))
            if skill:
                out.append({"skill": skill, "skill_importance": imp})
                if len(out) >= max_items:
                    break
            continue
        
        # Priority 3: Format "Skill Name 5" or "Skill Name(5)" (no space before paren)
        m3 = re.match(r"^\s*(.+?)\s*\(?\s*(\d+(?:\.\d+)?)\s*\)?\s*$", p)
        if m3:
            skill = m3.group(1).strip(" -–—:\t()")
            imp = float(m3.group(2))
            if skill and skill.lower() not in ["nan", "none"]:
                out.append({"skill": skill, "skill_importance": imp})
                if len(out) >= max_items:
                    break
    
    return out

def risk_band(score: float) -> str:
    if score <= 20:
        return "Low"
    if score <= 50:
        return "Medium"
    if score <= 70:
        return "High"
    return "Critical"

def get_risk_color(risk_band: str) -> str:
    """Get color for risk band - Wayve palette"""
    colors = {
        "Low": "#10B981",
        "Medium": "#F59E0B",
        "High": "#EF4444",
        "Critical": "#DC2626"
    }
    return colors.get(risk_band, "#6B7280")

def get_risk_badge_html(risk_band: str) -> str:
    """Generate HTML badge for risk"""
    color_class = risk_band.lower()
    return f'<span class="risk-badge risk-{color_class}">{risk_band}</span>'

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def compute_skill_risk(required_total: float, allocated_total: float) -> float:
    """Convert skill gap into 0-100 score."""
    if required_total <= 0:
        return 0.0
    if allocated_total >= required_total:
        return 0.0
    frac_missing = (required_total - allocated_total) / required_total
    return float(clamp01(frac_missing) * 100.0)

def coverage_missing_and_risk(emp_id: str, skills_req: list):
    """Return (missing_skills, coverage_risk_0_100)."""
    total_w = 0.0
    missing_w = 0.0
    missing = []

    for s in skills_req:
        sk = str(s["skill"]).strip()
        imp = float(s["skill_importance"])
        total_w += imp
        prow = people_raw[(people_raw["employee_id"] == emp_id) & (people_raw["skill"] == sk)]
        if prow.empty:
            missing.append(sk)
            missing_w += imp

    if total_w <= 0:
        return missing, 0.0
    return missing, float(clamp01(missing_w / total_w) * 100.0)

def compute_schedule_risk(utilization_peak: float, delay_days: int) -> float:
    """
    Compute schedule risk based on utilization and delays.
    
    Returns:
    - 0: No risk (utilization <= 100%, no delay)
    - 1-30: Low risk (slight overload or small delay)
    - 30-60: Medium risk (moderate overload or delay)
    - 60-100: High/Critical risk (severe overload or long delay)
    """
    base = 0.0
    
    # Zero risk case: utilization within capacity and no delay
    # Use <= 0 for delay_days to handle any edge cases, and small tolerance for utilization
    if utilization_peak <= 1.0 + 1e-6 and delay_days <= 0:
        return 0.0
    
    # Calculate risk from utilization overload
    # If utilization > 1.0, there's overload
    if utilization_peak > 1.0:
        # Map utilization to 0-60 risk points
        # utilization 1.0 = 0, utilization 2.0 = 60
        util_component = clamp01((utilization_peak - 1.0) / 1.0) * 60.0
    else:
        util_component = 0.0
    
    # Calculate risk from delays
    # Map delay days to 0-40 risk points
    # 0 days = 0, 20 days = 40
    delay_component = clamp01(delay_days / 20.0) * 40.0
    
    base = util_component + delay_component
    
    return float(clamp01(base / 100.0) * 100.0 if base > 100 else base)

def daterange(d0: date, d1: date):
    if d0 is None or d1 is None:
        return []
    if d1 < d0:
        return [d0]
    days = (d1 - d0).days
    return [d0 + timedelta(days=i) for i in range(days + 1)]

# ============================================
# SIDEBAR CONTROLS
# ============================================
st.sidebar.markdown("### Configuration")
st.sidebar.markdown("---")

with st.sidebar.expander("Assignment Rules", expanded=True):
    mandatory_threshold = st.slider(
        "Mandatory Skill Threshold",
        min_value=1,
        max_value=5,
        value=3,
        help="Skills with importance >= this threshold are mandatory. Employees must have ALL mandatory skills to be assigned."
    )
    team_first = st.checkbox(
        "Prefer Same Department",
        value=True,
        help="Prioritize assignees from the same department"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
if 'assign_df' in locals():
    if not assign_df.empty:
        total_tasks = len(assign_df)
        assigned = len(assign_df[assign_df["assignee"] != "UNASSIGNED"])
        st.sidebar.metric("Tasks", f"{assigned}/{total_tasks}", f"{assigned/total_tasks*100:.0f}% assigned")
        
        risk_counts = assign_df["risk_band"].value_counts()
        st.sidebar.markdown("**Risk Distribution:**")
        for risk in ["Low", "Medium", "High", "Critical"]:
            count = risk_counts.get(risk, 0)
            if count > 0:
                st.sidebar.markdown(f"- {risk}: {count}")

# ============================================
# MAIN TABS
# ============================================
tabs = st.tabs(["Data Input", "Allocation Results", "Gantt Chart", "Workload Analysis", "Task Details"])

# ============================================
# TAB 1: DATA INPUT
# ============================================
with tabs[0]:
    st.header("Data Input & Configuration")
    
    st.subheader("Upload Data Templates")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Tasks Template**")
        st.caption("Export from Jira with task information")
        task_file = st.file_uploader(
            "Upload Tasks Excel File",
            type=["xlsx"],
            key="tasks_upl",
            help="Required columns: task_id, task_name, department, start_date, end_date, work_size. Optional: priority, phase (for phase grouping)"
        )
        if task_file:
            st.success(f"{task_file.name} uploaded")
    
    with col2:
        st.markdown("**People Template**")
        st.caption("Export from HiBob + Lattice with employee skills")
        people_file = st.file_uploader(
            "Upload People Excel File",
            type=["xlsx"],
            key="people_upl",
            help="Required columns: employee_id, skill, proficiency, job_level, fte"
        )
        if people_file:
            st.success(f"{people_file.name} uploaded")
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    if not (task_file and people_file):
        st.info("Please upload both templates to continue with resource planning.")
        st.stop()
    
    # Load and validate data
    try:
        tasks_raw = pd.read_excel(task_file)
        people_raw = pd.read_excel(people_file)
    except Exception as e:
        st.error(f"Error reading files: {str(e)}")
        st.stop()
    
    # Normalize column names and handle duplicates
    def normalize_columns(df):
        """Normalize column names to lowercase and handle duplicates"""
        normalized = [c.lower().strip() for c in df.columns]
        # Handle duplicates by appending _1, _2, etc.
        seen = {}
        result = []
        for col in normalized:
            if col in seen:
                seen[col] += 1
                result.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                result.append(col)
        return result
    
    tasks_raw.columns = normalize_columns(tasks_raw)
    people_raw.columns = normalize_columns(people_raw)
    
    # Handle any remaining duplicate columns (safety check)
    if tasks_raw.columns.duplicated().any():
        # Remove duplicates by keeping first occurrence
        tasks_raw = tasks_raw.loc[:, ~tasks_raw.columns.duplicated()]
    
    # Required columns - PRIORITY IS NOW OPTIONAL
    task_required = ["task_id", "task_name", "department", "start_date", "end_date", "work_size"]
    people_required = ["employee_id", "skill", "proficiency", "job_level", "fte"]
    
    missing_tasks = [c for c in task_required if c not in tasks_raw.columns]
    missing_people = [c for c in people_required if c not in people_raw.columns]
    
    if missing_tasks:
        st.error(f"Tasks template missing required columns: {', '.join(missing_tasks)}")
        st.stop()
    if missing_people:
        st.error(f"People template missing required columns: {', '.join(missing_people)}")
        st.stop()
    
    # Handle optional priority field
    if "priority" not in tasks_raw.columns:
        tasks_raw["priority"] = "Medium"  # Default priority
    
    # Handle optional phase field - now that duplicates are merged, just ensure it exists and is clean
    if "phase" in tasks_raw.columns:
        # Ensure phase values are strings and handle NaN/None, but preserve actual phase names
        # Convert to string first, then handle nulls
        tasks_raw["phase"] = tasks_raw["phase"].astype(str)
        # Replace string representations of NaN/None with actual NaN, then fill
        tasks_raw["phase"] = tasks_raw["phase"].replace(["nan", "None", "NaN", "NaT", "<NA>"], pd.NA)
        tasks_raw["phase"] = tasks_raw["phase"].fillna("Uncategorized")
        # Replace empty strings with Uncategorized
        tasks_raw["phase"] = tasks_raw["phase"].replace("", "Uncategorized")
        # Strip whitespace
        tasks_raw["phase"] = tasks_raw["phase"].str.strip()
    else:
        # If phase column doesn't exist, set default
        tasks_raw["phase"] = "Uncategorized"  # Default phase
    
    # Final check: ensure no duplicate column names (safety net)
    if tasks_raw.columns.duplicated().any():
        # Remove duplicates by keeping first occurrence
        tasks_raw = tasks_raw.loc[:, ~tasks_raw.columns.duplicated()]
    
    # Parse dates
    tasks_raw["start_date"] = tasks_raw["start_date"].apply(to_date)
    tasks_raw["end_date"] = tasks_raw["end_date"].apply(to_date)
    
    # Available skills list
    people_raw["skill"] = people_raw["skill"].astype(str).str.strip()
    skills_list = sorted([s for s in people_raw["skill"].dropna().unique().tolist() if str(s).strip()])
    
    # Detect existing skills column - look for various possible column names
    skills_blob_col = None
    
    # First pass: Look for explicit patterns
    for c in tasks_raw.columns:
        lc = str(c).lower().strip()
        # Priority 1: columns with both "skills" and "importance" (most common)
        if "skills" in lc and "importance" in lc:
            skills_blob_col = c
            break
        # Priority 2: "skills" with "approved" or "db"
        elif "skills" in lc and ("approved" in lc or "db" in lc):
            skills_blob_col = c
            break
        # Priority 3: "skills needed"
        elif "skills needed" in lc:
            skills_blob_col = c
            break
    
    # Second pass: If not found, check content-based detection
    if skills_blob_col is None:
        for c in tasks_raw.columns:
            lc = str(c).lower().strip()
            # Check if column name suggests skills
            if "skill" in lc:
                # Check if this column actually contains skill data format
                non_null_values = tasks_raw[c].dropna()
                if len(non_null_values) > 0:
                    sample_val = str(non_null_values.iloc[0])
                    # Look for semicolon-separated format with parentheses (your format)
                    if ";" in sample_val and "(" in sample_val and ")" in sample_val:
                        # Verify it matches the pattern "Skill (number)"
                        test_parse = parse_skills_importance_cell(sample_val)
                        if len(test_parse) > 0:
                            skills_blob_col = c
                            break
    
    parsed_by_task = {}
    parsed_skill_values = set()
    if skills_blob_col is not None:
        for _, row in tasks_raw.iterrows():
            tid = str(row.get("task_id"))
            parsed = parse_skills_importance_cell(row.get(skills_blob_col))
            parsed_by_task[tid] = parsed
            for s in parsed:
                parsed_skill_values.add(str(s.get("skill", "")).strip())
    
    editor_skill_options = sorted({s for s in (set(skills_list) | parsed_skill_values) if str(s).strip()})
    if skills_blob_col is not None:
        # Show how many tasks have skills parsed
        tasks_with_skills = len([tid for tid, skills in parsed_by_task.items() if len(skills) > 0])
        st.success(f"✓ Detected skills column: **'{skills_blob_col}'**. Parsed skills from {tasks_with_skills} tasks. Pre-filled below for editing.")
    else:
        # Debug: show available columns that might be skills
        potential_cols = [c for c in tasks_raw.columns if 'skill' in str(c).lower()]
        if potential_cols:
            st.warning(f"Skills column not auto-detected. Found potential columns: {potential_cols}. Please check column names.")
    
    # Build skill editor
    st.subheader("Define Task Skills & Importance")
    st.markdown("Configure required skills for each task. Skills with higher importance are prioritized in assignment.")
    
    task_ids = tasks_raw["task_id"].astype(str).dropna().astype(str).unique().tolist()
    state_key = "task_skill_editor"
    
    def _init_editor():
        rows = []
        for tid in task_ids:
            parsed = parsed_by_task.get(str(tid), []) if isinstance(parsed_by_task, dict) else []
            def _get(i, key, default=None):
                if i < len(parsed) and key in parsed[i] and str(parsed[i][key]).strip() != "":
                    return parsed[i][key]
                return default
            skill1 = _get(0, "skill", None)
            skill2 = _get(1, "skill", None)
            skill3 = _get(2, "skill", None)
            # Ensure skills are strings or empty string (not lists, not None for selectbox compatibility)
            skill1 = str(skill1) if skill1 is not None else ""
            skill2 = str(skill2) if skill2 is not None else ""
            skill3 = str(skill3) if skill3 is not None else ""
            rows.append({
                "task_id": str(tid),
                "task_name": str(tasks_raw[tasks_raw["task_id"].astype(str) == tid]["task_name"].iloc[0] if len(tasks_raw[tasks_raw["task_id"].astype(str) == tid]) > 0 else tid),
                "skill_1": skill1,
                "importance_1": float(_get(0, "skill_importance", 3)),
                "skill_2": skill2,
                "importance_2": float(_get(1, "skill_importance", 2)),
                "skill_3": skill3,
                "importance_3": float(_get(2, "skill_importance", 1)),
            })
        df = pd.DataFrame(rows)
        # Explicitly set dtypes to ensure proper types
        df["task_id"] = df["task_id"].astype(str)
        df["task_name"] = df["task_name"].astype(str)
        df["skill_1"] = df["skill_1"].astype(object)
        df["skill_2"] = df["skill_2"].astype(object)
        df["skill_3"] = df["skill_3"].astype(object)
        return df
    
    if state_key not in st.session_state or st.session_state.get("task_ids_snapshot") != task_ids:
        st.session_state[state_key] = _init_editor()
        st.session_state["task_ids_snapshot"] = task_ids
    
    editor_df = st.session_state[state_key].copy()
    
    # Ensure skill columns are properly typed as object/string (not LIST)
    for col in ["skill_1", "skill_2", "skill_3"]:
        if col in editor_df.columns:
            # Convert to string type, handling None/NaN values
            editor_df[col] = editor_df[col].astype(object)
            # Replace None/NaN with empty string for selectbox compatibility
            editor_df[col] = editor_df[col].replace([None, np.nan], "")
            # Ensure all values are strings
            editor_df[col] = editor_df[col].apply(lambda x: str(x) if x != "" else "")
    
    # Prepare options with empty string for "no selection" instead of None
    skill_options_with_empty = [""] + editor_skill_options
    
    edited = st.data_editor(
        editor_df,
        use_container_width=True,
        num_rows="fixed",
        column_config={
            "task_id": st.column_config.TextColumn("Task ID", disabled=True),
            "task_name": st.column_config.TextColumn("Task Name", disabled=True),
            "skill_1": st.column_config.SelectboxColumn("Skill 1", options=skill_options_with_empty, width="medium"),
            "importance_1": st.column_config.NumberColumn("Importance 1", min_value=1, max_value=5, step=1, width="small"),
            "skill_2": st.column_config.SelectboxColumn("Skill 2", options=skill_options_with_empty, width="medium"),
            "importance_2": st.column_config.NumberColumn("Importance 2", min_value=1, max_value=5, step=1, width="small"),
            "skill_3": st.column_config.SelectboxColumn("Skill 3", options=skill_options_with_empty, width="medium"),
            "importance_3": st.column_config.NumberColumn("Importance 3", min_value=1, max_value=5, step=1, width="small"),
        },
        hide_index=True
    )
    
    st.session_state[state_key] = edited
    
    # Data previews
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Preview: Tasks Data", expanded=False):
            st.dataframe(tasks_raw.head(10), use_container_width=True)
            st.caption(f"Total: {len(tasks_raw)} tasks")
            # Show phase info if available
            if "phase" in tasks_raw.columns:
                unique_phases = tasks_raw["phase"].dropna().unique()
                if len(unique_phases) > 0:
                    st.caption(f"Phases detected: {', '.join([str(p) for p in unique_phases[:5]])}{'...' if len(unique_phases) > 5 else ''}")
    
    with col2:
        with st.expander("Preview: People Data", expanded=False):
            st.dataframe(people_raw.head(10), use_container_width=True)
            st.caption(f"Total: {len(people_raw)} skill records")

# ============================================
# BUILD TASK-SKILL DATA
# ============================================
skill_inputs = st.session_state.get("task_skill_editor")
if skill_inputs is None:
    st.stop()

# Create task-skill rows
skill_rows = []
for _, r in skill_inputs.iterrows():
    tid = str(r["task_id"])
    for i in [1,2,3]:
        sk = r.get(f"skill_{i}")
        imp = r.get(f"importance_{i}")
        if sk is None or (isinstance(sk, float) and np.isnan(sk)) or str(sk).strip().lower() in ["", "none", "nan"]:
            continue
        skill_rows.append({"task_id": tid, "skill": str(sk).strip(), "skill_importance": float(imp)})

task_skills_long = pd.DataFrame(skill_rows)
if task_skills_long.empty:
    st.warning("No task skills defined. Please add skills in the Data Input tab.")
    st.stop()

# Merge with tasks
tasks_base = tasks_raw.copy()
for col in ["skill", "skill_importance"]:
    if col in tasks_base.columns:
        tasks_base = tasks_base.drop(columns=[col])
tasks_base["task_id"] = tasks_base["task_id"].astype(str)
task_skills_long["task_id"] = task_skills_long["task_id"].astype(str)

tasks_long = tasks_base.merge(task_skills_long, on="task_id", how="left")
tasks_long = tasks_long.dropna(subset=["skill", "skill_importance"])

# Task-side calculation
tasks_long["work_size_num"] = tasks_long["work_size"].apply(size_to_effort)
tasks_long["required_skill_score"] = tasks_long["work_size_num"] * tasks_long["skill_importance"]

# People-side preparation
people_raw["employee_id"] = people_raw["employee_id"].astype(str)
people_raw["proficiency_output"] = people_raw["proficiency"].astype(float) * people_raw["job_level"].astype(float)
people_skill = people_raw.set_index(["employee_id","skill"])[["proficiency_output","fte"]].reset_index()

# Build task objects
task_objs = []
for tid, grp in tasks_long.groupby("task_id"):
    start_series = grp["start_date"].dropna()
    end_series = grp["end_date"].dropna()
    start = start_series.min() if not start_series.empty else None
    end = end_series.max() if not end_series.empty else None
    if end is None:
        continue
    if start is None:
        start = end
    if end < start:
        end = start
    duration_days = max(1, (end - start).days + 1)
    # Handle optional priority
    priority_val = grp["priority"].iloc[0] if "priority" in grp.columns and not grp["priority"].isna().iloc[0] else "Medium"
    # Handle optional phase - get from first row of the group
    if "phase" in grp.columns:
        phase_val = grp["phase"].iloc[0]
        # Handle NaN, None, or string "nan"
        if pd.isna(phase_val) or phase_val is None or str(phase_val).lower() in ["nan", "none", ""]:
            phase_val = "Uncategorized"
        else:
            phase_val = str(phase_val).strip()
    else:
        phase_val = "Uncategorized"
    task_objs.append({
        "task_id": tid,
        "task_name": grp["task_name"].iloc[0],
        "department": grp["department"].iloc[0],
        "priority": priority_val,
        "phase": phase_val,
        "work_size": grp["work_size"].iloc[0],
        "work_size_num": float(grp["work_size_num"].iloc[0]),
        "start_date": start,
        "end_date": end,
        "duration_days": duration_days,
        "skills": grp[["skill","skill_importance","required_skill_score"]].to_dict("records"),
        "required_total": float(grp["required_skill_score"].sum())
    })
tasks_df = pd.DataFrame(task_objs)
if tasks_df.empty:
    st.error("No valid tasks found (check start_date/end_date).")
    st.stop()

# ============================================
# ASSIGNMENT ENGINE
# ============================================
prio_map = {"critical":0, "high":1, "medium":2, "low":3}
tasks_df["_prio"] = tasks_df["priority"].astype(str).str.lower().map(prio_map).fillna(2)  # Default to medium
tasks_df = tasks_df.sort_values(["_prio","start_date"]).drop(columns=["_prio"])

employees = sorted(people_raw["employee_id"].unique().tolist())
emp_fte = people_raw.groupby("employee_id")["fte"].max().to_dict()

global_start = tasks_df["start_date"].min()
global_end = tasks_df["end_date"].max()
all_days = daterange(global_start, global_end)
daily_load = {e: {d: 0.0 for d in all_days} for e in employees}

def window_peak_util(emp_id: str, d0: date, d1: date):
    """Calculate peak utilization during a time window."""
    days = daterange(d0, d1)
    if not days:
        return 0.0
    cap = float(emp_fte.get(emp_id, 1.0))
    if cap <= 0:
        cap = 0.01
    return max((daily_load[emp_id].get(d,0.0)/cap) for d in days)

def has_capacity_for_task(emp_id: str, d0: date, d1: date, total_effort: float, max_utilization: float = 1.0):
    """
    Check if employee has capacity for a task BEFORE assignment.
    
    Simulates adding the task load (front-loaded) and checks if utilization
    stays within max_utilization (default 100%).
    
    Returns: (has_capacity: bool, estimated_peak_util: float)
    """
    days = daterange(d0, d1)
    if not days:
        return False, 0.0
    
    cap = float(emp_fte.get(emp_id, 1.0))
    if cap <= 0:
        cap = 0.01
    
    num_days = len(days)
    # Calculate front-loaded distribution (same as add_task_load)
    weights = []
    for i in range(num_days):
        weight = 2.0 - (1.5 * i / max(1, num_days - 1))
        weights.append(weight)
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w * num_days / total_weight for w in weights]
    
    # Simulate adding the task load
    peak_util = 0.0
    for i, d in enumerate(days):
        current_load = daily_load[emp_id].get(d, 0.0)
        additional_load = total_effort * weights[i] / num_days
        total_load = current_load + additional_load
        util = total_load / cap
        peak_util = max(peak_util, util)
    
    has_capacity = peak_util <= max_utilization
    return has_capacity, peak_util

def add_task_load(emp_id: str, d0: date, d1: date, total_effort: float):
    """
    Add task load to employee's daily schedule with FRONT-LOADED distribution.
    More work is allocated at the beginning of the task period.
    """
    days = daterange(d0, d1)
    if not days:
        return
    
    num_days = len(days)
    if num_days == 0:
        return
    
    # Front-loaded distribution: allocate more work at the beginning
    # Use a decreasing weight: first day gets most, last day gets least
    # Weights decrease linearly from 2.0 to 0.5
    weights = []
    for i in range(num_days):
        # Weight decreases from 2.0 (first day) to 0.5 (last day)
        weight = 2.0 - (1.5 * i / max(1, num_days - 1))
        weights.append(weight)
    
    # Normalize weights so they sum to num_days (maintains total effort)
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w * num_days / total_weight for w in weights]
    
    # Distribute effort according to weights
    for i, d in enumerate(days):
        if d in daily_load[emp_id]:
            daily_load[emp_id][d] += total_effort * weights[i] / num_days

def estimate_delay_days(emp_id: str, d0: date, d1: date, total_effort: float):
    cap = float(emp_fte.get(emp_id, 1.0))
    if cap <= 0:
        cap = 0.01
    days = daterange(d0, d1)
    if not days:
        return 0
    remaining_effort = total_effort
    for d in days:
        used = daily_load[emp_id].get(d, 0.0)
        avail = max(0.0, cap - used)
        take = min(avail, remaining_effort)
        remaining_effort -= take
        if remaining_effort <= 1e-9:
            return 0
    delay = 0
    cur = d1 + timedelta(days=1)
    for _ in range(365):
        used = daily_load[emp_id].get(cur, 0.0)
        avail = max(0.0, cap - used)
        take = min(avail, remaining_effort)
        remaining_effort -= take
        delay += 1
        if remaining_effort <= 1e-9:
            return delay
        cur = cur + timedelta(days=1)
    return delay

def person_allocated_skill_total(emp_id: str, skills_req: list):
    allocated = 0.0
    for s in skills_req:
        sk = s["skill"]
        imp = float(s["skill_importance"])
        prow = people_raw[(people_raw["employee_id"]==emp_id) & (people_raw["skill"]==sk)]
        if not prow.empty:
            allocated += float(prow.iloc[0]["proficiency_output"]) * imp
    return allocated

def has_mandatory_skills(emp_id: str, skills_req: list):
    """
    Check if employee has all mandatory skills.
    Mandatory skills are those with importance >= mandatory_threshold.
    Employee must have ALL mandatory skills to be eligible for assignment.
    """
    for s in skills_req:
        skill_importance = float(s["skill_importance"])
        # Skills with importance >= threshold are mandatory
        if skill_importance >= mandatory_threshold:
            sk = s["skill"]
            prow = people_raw[(people_raw["employee_id"]==emp_id) & (people_raw["skill"]==sk)]
            if prow.empty:
                return False  # Missing a mandatory skill
    return True  # Has all mandatory skills

assignments = []
for _, t in tasks_df.iterrows():
    tid = t["task_id"]
    skills_req = t["skills"]
    required_total = float(t["required_total"])
    effort = float(t["work_size_num"])
    d0 = t["start_date"]
    d1 = t["end_date"]
    
    candidates = employees.copy()
    
    if team_first and "department" in people_raw.columns:
        dept = str(t["department"])
        same_team = sorted(people_raw[people_raw["department"].astype(str)==dept]["employee_id"].unique().tolist())
        if same_team:
            candidates = same_team + [e for e in candidates if e not in same_team]
    
    best = None
    best_overall = None
    for emp in candidates:
        # STEP 1: Check skills first
        if not has_mandatory_skills(emp, skills_req):
            continue
        
        allocated_total = person_allocated_skill_total(emp, skills_req)
        
        # Additional check: if employee has 0% skill match (no skills at all), skip them
        # This handles the case where all skills are optional but employee has none
        if allocated_total <= 0 and required_total > 0:
            continue  # Skip employees with zero skill match
        
        # STEP 2: Check capacity BEFORE assigning
        # If employee doesn't have capacity, skip them and look for someone else
        has_capacity, estimated_peak_util = has_capacity_for_task(emp, d0, d1, effort, max_utilization=1.0)
        if not has_capacity:
            continue  # Skip - no capacity available
        
        # STEP 3: Calculate risks only for employees with skills AND capacity
        gap_skill_risk = compute_skill_risk(required_total, allocated_total)
        missing_skills, coverage_risk = coverage_missing_and_risk(emp, skills_req)
        skill_risk = max(gap_skill_risk, coverage_risk)
        
        # Use the estimated peak utilization from capacity check
        util_peak = estimated_peak_util
        delay_days = estimate_delay_days(emp, d0, d1, effort)
        # Ensure delay_days is an integer for the comparison
        delay_days_int = int(round(delay_days))
        sched_risk = compute_schedule_risk(util_peak, delay_days_int)
        
        overall = max(skill_risk, sched_risk)
        
        if best_overall is None or overall < best_overall or (overall == best_overall and delay_days < best.get("expected_delay_days", 10**9)):
            best = {
                "task_id": tid,
                "task_name": t["task_name"],
                "department": t["department"],
                "priority": t["priority"],
                "phase": str(t.get("phase", "Uncategorized")) if "phase" in t else "Uncategorized",
                "assignee": emp,
                "work_size": t["work_size"],
                "skill_required_total": required_total,
                "skill_allocated_total": allocated_total,
                "skill_delta": allocated_total - required_total,
                "missing_skills": ", ".join(missing_skills) if missing_skills else "",
                "coverage_risk": float(coverage_risk),
                "gap_skill_risk": float(gap_skill_risk),
                "skill_risk": skill_risk,
                "schedule_risk": sched_risk,
                "overall_risk": overall,
                "risk_band": risk_band(overall),
                "expected_delay_days": int(delay_days),
                "target_start": d0,
                "target_end": d1,
                "planned_start": d0,
                "planned_finish": d1 + timedelta(days=int(delay_days)),
            }
            best_overall = overall
    
    if best is None:
        # No one has skills AND capacity - flag as unassigned with delay
        # Estimate delay by finding when someone might have capacity
        estimated_delay = 0
        # Try to find when any eligible employee might have capacity
        for emp in candidates:
            if not has_mandatory_skills(emp, skills_req):
                continue
            allocated_total = person_allocated_skill_total(emp, skills_req)
            if allocated_total <= 0 and required_total > 0:
                continue
            # Check if they'll have capacity later (simple heuristic: check 30 days out)
            future_start = d0 + timedelta(days=30)
            future_end = d1 + timedelta(days=30)
            has_capacity_future, _ = has_capacity_for_task(emp, future_start, future_end, effort, max_utilization=1.0)
            if has_capacity_future:
                estimated_delay = 30  # Rough estimate
                break
        
        best = {
            "task_id": tid,
            "task_name": t["task_name"],
            "department": t["department"],
            "priority": t["priority"],
            "phase": str(t.get("phase", "Uncategorized")) if "phase" in t else "Uncategorized",
            "assignee": "UNASSIGNED",
            "work_size": t["work_size"],
            "skill_required_total": required_total,
            "skill_allocated_total": 0.0,
            "skill_delta": -required_total,
            "missing_skills": ", ".join([str(s.get("skill")).strip() for s in skills_req]) if skills_req else "",
            "coverage_risk": 100.0,
            "gap_skill_risk": 100.0,
            "skill_risk": 100.0,
            "schedule_risk": 100.0,
            "overall_risk": 100.0,
            "risk_band": "Critical",
            "expected_delay_days": estimated_delay,  # Flag delay when unassigned due to capacity
            "target_start": d0,
            "target_end": d1,
            "planned_start": d0,
            "planned_finish": d1 + timedelta(days=estimated_delay),
        }
    
    if best["assignee"] != "UNASSIGNED":
        add_task_load(best["assignee"], best["planned_start"], best["planned_finish"], effort)
    
    assignments.append(best)

assign_df = pd.DataFrame(assignments)

# ============================================
# TAB 2: ALLOCATION RESULTS
# ============================================
with tabs[1]:
    st.header("Allocation Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(assign_df)
    assigned = len(assign_df[assign_df["assignee"] != "UNASSIGNED"])
    unassigned = total_tasks - assigned
    
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Assigned", assigned, f"{assigned/total_tasks*100:.0f}%")
    with col3:
        st.metric("Unassigned", unassigned, f"-{unassigned/total_tasks*100:.0f}%")
    with col4:
        avg_risk = assign_df["overall_risk"].mean()
        st.metric("Avg Risk Score", f"{avg_risk:.1f}", risk_band(avg_risk))
    
    st.markdown("---")
    
    # Risk distribution chart - Wayve colors
    risk_counts = assign_df["risk_band"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_risk = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            color=risk_counts.index,
            color_discrete_map={
                "Low": "#10B981",
                "Medium": "#F59E0B",
                "High": "#EF4444",
                "Critical": "#DC2626"
            },
            labels={"x": "Risk Level", "y": "Number of Tasks"},
            title="Risk Distribution"
        )
        fig_risk.update_layout(
            showlegend=False, 
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=12)
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.markdown("### Risk Breakdown")
        for risk in ["Low", "Medium", "High", "Critical"]:
            count = risk_counts.get(risk, 0)
            pct = (count / total_tasks * 100) if total_tasks > 0 else 0
            st.markdown(f"**{risk}**: {count} ({pct:.1f}%)")
    
    st.markdown("---")
    
    # Filter and sort options
    has_phase_col = "phase" in assign_df.columns and assign_df["phase"].notna().any()
    
    if has_phase_col:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            filter_risk = st.multiselect(
                "Filter by Risk",
                options=["Low", "Medium", "High", "Critical"],
                default=["Low", "Medium", "High", "Critical"],
                key="alloc_filter_risk_phase"
            )
        with col2:
            filter_assignee = st.multiselect(
                "Filter by Assignee",
                options=sorted(assign_df["assignee"].unique().tolist()),
                default=sorted(assign_df["assignee"].unique().tolist()),
                key="alloc_filter_assignee_phase"
            )
        with col3:
            filter_phase = st.multiselect(
                "Filter by Phase",
                options=sorted(assign_df["phase"].dropna().unique().tolist()),
                default=sorted(assign_df["phase"].dropna().unique().tolist()),
                key="alloc_filter_phase"
            )
        with col4:
            sort_by = st.selectbox(
                "Sort by",
                options=["Risk Band", "Priority", "Phase", "Task ID", "Assignee"],
                index=0
            )
        
        # Filter dataframe
        filtered_df = assign_df[
            (assign_df["risk_band"].isin(filter_risk)) &
            (assign_df["assignee"].isin(filter_assignee)) &
            (assign_df["phase"].isin(filter_phase))
        ]
    else:
        col1, col2, col3 = st.columns(3)
    with col1:
        filter_risk = st.multiselect(
            "Filter by Risk",
            options=["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"],
            key="alloc_filter_risk_no_phase"
        )
    with col2:
        filter_assignee = st.multiselect(
            "Filter by Assignee",
            options=sorted(assign_df["assignee"].unique().tolist()),
            default=sorted(assign_df["assignee"].unique().tolist()),
            key="alloc_filter_assignee_no_phase"
        )
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Risk Band", "Priority", "Task ID", "Assignee"],
            index=0
        )
    
    # Filter dataframe
    filtered_df = assign_df[
        (assign_df["risk_band"].isin(filter_risk)) &
        (assign_df["assignee"].isin(filter_assignee))
    ]
    
    # Sort
    if sort_by == "Risk Band":
        risk_order = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
        filtered_df = filtered_df.copy()
        filtered_df["_risk_order"] = filtered_df["risk_band"].map(risk_order)
        filtered_df = filtered_df.sort_values(["_risk_order", "priority"]).drop(columns=["_risk_order"])
    elif sort_by == "Priority":
        prio_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        filtered_df = filtered_df.copy()
        filtered_df["_prio_order"] = filtered_df["priority"].astype(str).str.lower().map(prio_order).fillna(99)
        filtered_df = filtered_df.sort_values(["_prio_order", "risk_band"]).drop(columns=["_prio_order"])
    elif sort_by == "Phase" and has_phase_col:
        filtered_df = filtered_df.sort_values(["phase", "risk_band"])
    elif sort_by == "Task ID":
        filtered_df = filtered_df.sort_values("task_id")
    else:
        filtered_df = filtered_df.sort_values(["assignee", "risk_band"])
    
    # Display table with styling
    display_cols = [
        "task_id", "task_name", "department", "phase", "priority", "assignee", "work_size",
        "risk_band", "skill_risk", "schedule_risk", "expected_delay_days"
    ]
    # Remove phase if not available
    if "phase" not in filtered_df.columns:
        display_cols = [c for c in display_cols if c != "phase"]
    
    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "risk_band": st.column_config.TextColumn("Risk", width="small"),
            "skill_risk": st.column_config.NumberColumn("Skill Risk", format="%.0f", width="small"),
            "schedule_risk": st.column_config.NumberColumn("Schedule Risk", format="%.0f", width="small"),
            "expected_delay_days": st.column_config.NumberColumn("Delay (days)", format="%d", width="small"),
        }
    )

# ============================================
# TAB 3: GANTT CHART
# ============================================
with tabs[2]:
    st.header("📊 Gantt Chart - Hierarchical View")
    st.caption("✨ NEW: Phases → Tasks with improved layout and left-aligned text")
    
    # Check if phase column exists in assign_df
    has_phase_col = "phase" in assign_df.columns and assign_df["phase"].notna().any()
    
    gantt_df = assign_df.copy()
    gantt_df["Start"] = pd.to_datetime(gantt_df["planned_start"])
    gantt_df["Finish"] = pd.to_datetime(gantt_df["planned_finish"])
    gantt_df["Duration"] = (gantt_df["Finish"] - gantt_df["Start"]).dt.days
    
    # Color mapping - Wayve palette
    color_map = {
        "Low": "#10B981",
        "Medium": "#F59E0B",
        "High": "#EF4444",
        "Critical": "#DC2626"
    }
    
    # Phase filter (always show if phases exist)
    if has_phase_col:
        available_phases = sorted(gantt_df["phase"].dropna().unique().tolist())
        if len(available_phases) > 0:
            selected_phases = st.multiselect(
                "**Filter by Phase**",
                options=available_phases,
                default=available_phases,
                help="Select phases to display in the Gantt chart",
                key="gantt_phase_filter"
            )
            gantt_df = gantt_df[gantt_df["phase"].isin(selected_phases)]
    
    st.markdown("---")
    
    # Create unified Gantt chart with expandable/collapsible phases
    if has_phase_col:
        # Define custom phase order
        phase_order = ["Scoping", "Test architecture and SW dev", "Testing and approval", "Final approval", "Process"]
        
        # Get all phases from data
        all_phases = gantt_df["phase"].dropna().unique().tolist()
        
        # Sort phases: first by custom order, then any remaining phases alphabetically
        phases_sorted = []
        for phase in phase_order:
            # Case-insensitive matching
            matching_phases = [p for p in all_phases if str(p).strip().lower() == phase.lower()]
            if matching_phases:
                phases_sorted.extend(matching_phases)
        
        # Add any remaining phases not in the custom order
        remaining_phases = [p for p in all_phases if p not in phases_sorted]
        phases_sorted.extend(sorted(remaining_phases))
        
        # Initialize session state for expanded phases if not exists
        if "expanded_phases" not in st.session_state:
            st.session_state.expanded_phases = set()  # All collapsed by default
        
        # Phase expand/collapse controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.caption("Click the buttons below to expand/collapse each phase")
        with col2:
            if st.button("Expand All", key="expand_all"):
                st.session_state.expanded_phases = set(phases_sorted)
                st.rerun()
        with col3:
            if st.button("Collapse All", key="collapse_all"):
                st.session_state.expanded_phases = set()
                st.rerun()
        
        # Clickable phase toggle buttons (aligned with chart phases)
        st.markdown("**Click to toggle phases:**")
        phase_button_cols = st.columns(min(5, len(phases_sorted)))
        for idx, phase in enumerate(phases_sorted):
            col_idx = idx % 5
            with phase_button_cols[col_idx]:
                is_expanded = phase in st.session_state.expanded_phases
                button_text = f"➖ {phase}" if is_expanded else f"➕ {phase}"
                if st.button(button_text, key=f"phase_toggle_{phase}", use_container_width=True):
                    if is_expanded:
                        st.session_state.expanded_phases.discard(phase)
                    else:
                        st.session_state.expanded_phases.add(phase)
                    st.rerun()
        
        st.markdown("---")
        
        # Build hierarchical data for unified Gantt chart
        hierarchical_data = []
        
        for phase in phases_sorted:
            phase_tasks = gantt_df[gantt_df["phase"] == phase].copy()
            if len(phase_tasks) == 0:
                continue
            
            # Calculate phase summary
            phase_start = phase_tasks["Start"].min()
            phase_finish = phase_tasks["Finish"].max()
            avg_risk = phase_tasks["overall_risk"].mean()
            phase_risk_band = risk_band(avg_risk)
            task_count = len(phase_tasks)
            assigned_count = len(phase_tasks[phase_tasks["assignee"] != "UNASSIGNED"])
            
            # Determine expand/collapse icon
            is_expanded = phase in st.session_state.expanded_phases
            expand_icon = "➖" if is_expanded else "➕"
            
            # Add phase row (always visible) - big and bold
            # Using HTML-like formatting that will be rendered
            phase_name = f"{expand_icon} {phase} ({task_count} tasks)"
            hierarchical_data.append({
                "Name": phase_name,
                "Type": "Phase",
                "Phase": str(phase),
                "Start": phase_start,
                "Finish": phase_finish,
                "Duration": (phase_finish - phase_start).days,
                "Risk Band": phase_risk_band,
                "Task Count": task_count,
                "Assigned": assigned_count,
                "Avg Risk": avg_risk,
                "task_id": None,
                "task_name": None,
                "assignee": None,
                "skill_risk": None,
                "schedule_risk": None,
                "expected_delay_days": None,
                "IsExpanded": is_expanded
            })
            
            # Add task rows (only if phase is expanded)
            if is_expanded:
                # Sort tasks by start date within phase
                phase_tasks_sorted = phase_tasks.sort_values("Start")
                for _, task in phase_tasks_sorted.iterrows():
                    task_name = f"    └─ {task['task_name']} ({task['task_id']})"
                    hierarchical_data.append({
                        "Name": task_name,
                        "Type": "Task",
                        "Phase": str(phase),
                        "Start": task["Start"],
                        "Finish": task["Finish"],
                        "Duration": task["Duration"],
                        "Risk Band": task["risk_band"],
                        "Task Count": None,
                        "Assigned": None,
                        "Avg Risk": None,
                        "task_id": task["task_id"],
                        "task_name": task["task_name"],
                        "assignee": task["assignee"],
                        "skill_risk": task["skill_risk"],
                        "schedule_risk": task["schedule_risk"],
                        "expected_delay_days": task["expected_delay_days"],
                        "IsExpanded": None
                    })
        
        hierarchical_df = pd.DataFrame(hierarchical_data)
        
        # Create unified hierarchical Gantt chart
        fig = px.timeline(
            hierarchical_df,
            x_start="Start",
            x_end="Finish",
            y="Name",
            color="Risk Band",
            color_discrete_map=color_map,
            hover_data={
                "Type": True,
                "Phase": True,
                "Duration": True,
                "Task Count": True,
                "Assigned": True,
                "Avg Risk": ":.1f",
                "assignee": True,
                "skill_risk": ":.0f",
                "schedule_risk": ":.0f",
                "expected_delay_days": True,
                "Start": False,
                "Finish": False,
            },
            labels={"Risk Band": "Risk Level"},
        )
        
        # Enhanced styling for hierarchical view with left-aligned text
        # Create custom tick labels with different font sizes for phases vs tasks
        tick_labels = []
        for idx, row in hierarchical_df.iterrows():
            if row["Type"] == "Phase":
                # Bold and larger for phases
                tick_labels.append(row["Name"])
            else:
                # Regular for tasks
                tick_labels.append(row["Name"])
        
        fig.update_yaxes(
            autorange="reversed",
            title=None,  # Remove "undefined" label completely
            tickfont=dict(size=13, family="Inter, sans-serif"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            tickmode='array',
            tickvals=list(range(len(hierarchical_df))),
            ticktext=tick_labels,
            side='left',
            tickangle=0  # Horizontal text for better readability
        )
        
        # Update font for phase rows specifically using annotations or custom styling
        # Note: Plotly doesn't support per-tick font styling, so we'll make all phase text bold in the data
        
        fig.update_xaxes(
            title="Timeline",
            tickfont=dict(size=10, family="Inter, sans-serif"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        )
        
        # Calculate height based on number of visible items
        num_items = len(hierarchical_df)
        row_height = 40  # Increased height for better visibility
        min_height = 500
        max_height = 2000
        
        fig.update_layout(
            height=min(max(min_height, num_items * row_height), max_height),
            margin=dict(l=450, r=50, t=30, b=50),  # Increased left margin for better left alignment
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11)
            ),
            hovermode="closest",
            plot_bgcolor='#FAFAFA',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            title_font=dict(size=14, family="Inter, sans-serif"),
            showlegend=True
        )
        
        # Ensure y-axis labels are left-aligned
        fig.update_yaxes(
            tickangle=0,  # Horizontal text
            side='left',
            anchor='free',
            position=0.0
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            phase_count = len(phases_sorted)
            st.metric("Total Phases", phase_count)
        with col2:
            task_count = len(gantt_df)
            st.metric("Total Tasks", task_count)
        with col3:
            total_duration = (gantt_df["Finish"].max() - gantt_df["Start"].min()).days
            st.metric("Total Duration", f"{total_duration} days")
        with col4:
            unassigned = len(gantt_df[gantt_df["assignee"] == "UNASSIGNED"])
            st.metric("Unassigned Tasks", unassigned, delta=f"-{unassigned}" if unassigned > 0 else None)
    
    else:
        # Task-level view (no phases available)
        gantt_df["Task"] = gantt_df["task_name"].astype(str) + " (" + gantt_df["task_id"].astype(str) + ")"
        gantt_df["Assignee"] = gantt_df["assignee"].astype(str)
        
        fig = px.timeline(
            gantt_df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="risk_band",
            color_discrete_map=color_map,
            hover_data={
                "Assignee": True,
                "skill_risk": ":.0f",
                "schedule_risk": ":.0f",
                "expected_delay_days": True,
                "Duration": True,
                "Start": False,
                "Finish": False,
            },
            labels={"risk_band": "Risk Level"}
        )
        
        fig.update_yaxes(
            autorange="reversed",
            title="",
            tickfont=dict(size=11, family="Inter, sans-serif"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        )
        fig.update_xaxes(
            title="Timeline",
            tickfont=dict(size=10, family="Inter, sans-serif"),
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        )
        
        fig.update_layout(
            height=max(600, 40*len(gantt_df)),
            margin=dict(l=450, r=50, t=30, b=50),  # Increased left margin for left alignment
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11)
            ),
            hovermode="closest",
            plot_bgcolor='#FAFAFA',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            title_font=dict(size=14, family="Inter, sans-serif")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gantt summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Duration", f"{(gantt_df['Finish'].max() - gantt_df['Start'].min()).days} days")
        with col2:
            avg_duration = gantt_df["Duration"].mean()
            st.metric("Avg Task Duration", f"{avg_duration:.1f} days")
        with col3:
            max_delay = gantt_df["expected_delay_days"].max() if gantt_df["expected_delay_days"].notna().any() else 0
            st.metric("Max Delay", f"{max_delay} days")

# ============================================
# TAB 4: WORKLOAD ANALYSIS
# ============================================
with tabs[3]:
    st.header("Workload Analysis")
    st.caption("Resource utilization and capacity planning")
    
    w_start = min(assign_df["planned_start"])
    w_end = max(assign_df["planned_finish"])
    days = daterange(w_start, w_end)
    
    rows = []
    for emp in employees:
        cap = float(emp_fte.get(emp, 1.0))
        for d in days:
            load = daily_load[emp].get(d, 0.0)
            util = load / cap if cap > 0 else 0.0
            rows.append({"assignee": emp, "date": d, "load": load, "capacity": cap, "utilization": util})
    
    workload_df = pd.DataFrame(rows)
    
    # Summary statistics
    summary = workload_df.groupby("assignee").agg(
        avg_util=("utilization", "mean"),
        max_util=("utilization", "max"),
        total_effort=("load", "sum"),
        fte=("capacity", "max")
    ).reset_index()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", len(employees))
    with col2:
        avg_util_all = summary["avg_util"].mean()
        st.metric("Avg Utilization", f"{avg_util_all*100:.1f}%")
    with col3:
        overloaded = len(summary[summary["max_util"] > 1.0])
        st.metric("Overloaded", overloaded, f"{overloaded/len(employees)*100:.0f}%")
    with col4:
        underutilized = len(summary[summary["avg_util"] < 0.5])
        st.metric("Underutilized", underutilized, f"{underutilized/len(employees)*100:.0f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        summary_sorted = summary.sort_values("avg_util", ascending=False)
        fig_bar = px.bar(
            summary_sorted,
            x="assignee",
            y="avg_util",
            color="avg_util",
            color_continuous_scale=["#10B981", "#F59E0B", "#EF4444", "#DC2626"],
            labels={"avg_util": "Average Utilization", "assignee": "Employee"},
            title="Average Utilization by Employee",
            hover_data=["max_util", "fte", "total_effort"]
        )
        fig_bar.add_hline(y=1.0, line_dash="dash", line_color="#DC2626", annotation_text="100% Capacity")
        fig_bar.update_layout(
            height=400, 
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11)
        )
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Heatmap of utilization over time
        pivot_data = workload_df.pivot_table(
            index="assignee",
            columns="date",
            values="utilization",
            aggfunc="mean"
        )
        
        fig_heatmap = px.imshow(
            pivot_data.values,
            labels=dict(x="Date", y="Employee", color="Utilization"),
            x=[str(d) for d in pivot_data.columns],
            y=pivot_data.index,
            color_continuous_scale=["#10B981", "#F59E0B", "#EF4444", "#DC2626"],
            aspect="auto",
            title="Utilization Heatmap Over Time"
        )
        fig_heatmap.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("---")
    
    # Time series chart
    st.subheader("Utilization Trends")
    selected_employees = st.multiselect(
        "Select employees to view",
        options=sorted(employees),
        default=sorted(employees)[:min(5, len(employees))],
        key="workload_employee_select"
    )
    
    if selected_employees:
        filtered_workload = workload_df[workload_df["assignee"].isin(selected_employees)]
        fig_line = px.line(
            filtered_workload,
            x="date",
            y="utilization",
            color="assignee",
            labels={"utilization": "Utilization", "date": "Date"},
            title="Daily Utilization Over Time"
        )
        fig_line.add_hline(y=1.0, line_dash="dash", line_color="#DC2626", annotation_text="100% Capacity")
        fig_line.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Summary table
    st.subheader("Employee Summary")
    summary_display = summary.sort_values("avg_util", ascending=False)
    summary_display["avg_util_pct"] = (summary_display["avg_util"] * 100).round(1)
    summary_display["max_util_pct"] = (summary_display["max_util"] * 100).round(1)
    
    st.dataframe(
        summary_display[["assignee", "fte", "avg_util_pct", "max_util_pct", "total_effort"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "assignee": "Employee",
            "fte": "FTE",
            "avg_util_pct": st.column_config.NumberColumn("Avg Utilization %", format="%.1f%%"),
            "max_util_pct": st.column_config.NumberColumn("Max Utilization %", format="%.1f%%"),
            "total_effort": st.column_config.NumberColumn("Total Effort", format="%.1f"),
        }
    )

# ============================================
# TAB 5: TASK DETAILS
# ============================================
with tabs[4]:
    st.header("Task Details & Analysis")
    
    selected = st.selectbox(
        "Select Task",
        options=tasks_df["task_id"].tolist(),
        format_func=lambda x: f"{tasks_df[tasks_df['task_id']==x]['task_name'].iloc[0]} ({x})"
    )
    
    tinfo = tasks_df[tasks_df["task_id"]==selected].iloc[0]
    arow = assign_df[assign_df["task_id"]==selected].iloc[0]
    
    # Task overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {tinfo['task_name']}")
        st.markdown(f"**Task ID:** {selected}")
        st.markdown(f"**Department:** {tinfo['department']}")
        if "phase" in tinfo and pd.notna(tinfo.get("phase")):
            st.markdown(f"**Phase:** {tinfo['phase']}")
        st.markdown(f"**Priority:** {tinfo['priority']}")
        st.markdown(f"**Work Size:** {tinfo['work_size']}")
        st.markdown(f"**Duration:** {tinfo['start_date']} → {tinfo['end_date']} ({tinfo['duration_days']} days)")
    
    with col2:
        risk_color = get_risk_color(arow['risk_band'])
        st.markdown(f"### Risk Assessment")
        st.markdown(f"**Overall Risk:** {get_risk_badge_html(arow['risk_band'])}", unsafe_allow_html=True)
        st.markdown(f"**Risk Score:** {arow['overall_risk']:.1f}/100")
        st.markdown(f"**Skill Risk:** {arow['skill_risk']:.1f}/100")
        st.markdown(f"**Schedule Risk:** {arow['schedule_risk']:.1f}/100")
        if pd.notna(arow["expected_delay_days"]):
            st.markdown(f"**Expected Delay:** {arow['expected_delay_days']} days")
        else:
            st.markdown("**Expected Delay:** N/A")
    
    st.markdown("---")
    
    # Required skills
    st.subheader("Required Skills")
    req_rows = []
    for s in tinfo["skills"]:
        req_rows.append({
            "Skill": s["skill"],
            "Importance": s["skill_importance"],
            "Required Score": f"{s['required_skill_score']:.2f}"
        })
    req_df = pd.DataFrame(req_rows)
    st.dataframe(req_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Assignment details
    st.subheader("Assignment Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Assignee:** {arow['assignee']}")
        st.markdown(f"**Skill Required Total:** {arow['skill_required_total']:.2f}")
        st.markdown(f"**Skill Allocated Total:** {arow['skill_allocated_total']:.2f}")
        st.markdown(f"**Skill Delta:** {arow['skill_delta']:.2f}")
        if str(arow.get('missing_skills','')).strip():
            st.warning(f"Missing skills: {arow['missing_skills']}")
    
    with col2:
        st.markdown(f"**Target Start:** {arow['target_start']}")
        st.markdown(f"**Target End:** {arow['target_end']}")
        st.markdown(f"**Planned Start:** {arow['planned_start']}")
        st.markdown(f"**Planned Finish:** {arow['planned_finish']}")
        if pd.notna(arow["expected_delay_days"]) and arow["expected_delay_days"] > 0:
            st.error(f"Projected delay of {arow['expected_delay_days']} days")
    
    st.markdown("---")
    
    # Candidate comparison
    with st.expander("Candidate Skill Comparison", expanded=False):
        cand = []
        for emp in employees:
            allocated_total = person_allocated_skill_total(emp, tinfo["skills"])
            cand.append({
                "Employee": emp,
                "Allocated Skill Score": f"{allocated_total:.2f}",
                "Match %": f"{(allocated_total / arow['skill_required_total'] * 100):.1f}%" if arow['skill_required_total'] > 0 else "0%"
            })
        cand_df = pd.DataFrame(cand)
        cand_df = cand_df.sort_values("Allocated Skill Score", ascending=False, key=lambda x: x.str.replace('%', '').astype(float) if x.name == "Match %" else pd.to_numeric(x.str.replace('Allocated Skill Score', ''), errors='coerce'))
        st.dataframe(cand_df, use_container_width=True, hide_index=True)
