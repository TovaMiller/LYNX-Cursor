"""
LYNX Resource Planning System - Allocation Engine

Core allocation algorithm, risk scoring, and capacity planning logic.
No Streamlit dependency - can be tested independently.
"""

import pandas as pd
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple


# ============================================
# RISK SCORING
# ============================================

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def risk_band(score: float) -> str:
    """Map a 0-100 risk score to a categorical band."""
    if score <= 20:
        return "Low"
    if score <= 50:
        return "Medium"
    if score <= 70:
        return "High"
    return "Critical"


def get_risk_color(band: str) -> str:
    """Get hex color for a risk band."""
    colors = {
        "Low": "#10B981",
        "Medium": "#F59E0B",
        "High": "#EF4444",
        "Critical": "#DC2626",
    }
    return colors.get(band, "#6B7280")


def get_risk_badge_html(band: str) -> str:
    """Generate an HTML badge for a risk band."""
    color_class = band.lower()
    return f'<span class="risk-badge risk-{color_class}">{band}</span>'


def compute_skill_risk(required_total: float, allocated_total: float) -> float:
    """Convert skill gap into a 0-100 score."""
    if required_total <= 0:
        return 0.0
    if allocated_total >= required_total:
        return 0.0
    frac_missing = (required_total - allocated_total) / required_total
    return float(clamp01(frac_missing) * 100.0)


def compute_schedule_risk(utilization_peak: float, delay_days: int) -> float:
    """
    Compute schedule risk based on utilization and delays (0-100).

    - utilization_peak: ratio of load to capacity (1.0 = 100%)
    - delay_days: projected delay beyond the original end date
    """
    if utilization_peak <= 1.0 + 1e-6 and delay_days <= 0:
        return 0.0

    util_component = clamp01((utilization_peak - 1.0) / 1.0) * 60.0 if utilization_peak > 1.0 else 0.0
    delay_component = clamp01(delay_days / 20.0) * 40.0

    base = util_component + delay_component
    return float(clamp01(base / 100.0) * 100.0 if base > 100 else base)


# ============================================
# DATE UTILITIES
# ============================================

def daterange(d0: date, d1: date) -> list:
    """Return a list of dates from d0 to d1 (inclusive)."""
    if d0 is None or d1 is None:
        return []
    if d1 < d0:
        return [d0]
    days = (d1 - d0).days
    return [d0 + timedelta(days=i) for i in range(days + 1)]


# ============================================
# CAPACITY & LOAD MANAGEMENT
# ============================================

def window_peak_util(
    emp_id: str,
    d0: date,
    d1: date,
    daily_load: Dict[str, Dict[date, float]],
    emp_fte: Dict[str, float],
) -> float:
    """Calculate peak utilization for an employee during a time window."""
    days = daterange(d0, d1)
    if not days:
        return 0.0
    cap = float(emp_fte.get(emp_id, 1.0))
    if cap <= 0:
        cap = 0.01
    return max((daily_load[emp_id].get(d, 0.0) / cap) for d in days)


def has_capacity_for_task(
    emp_id: str,
    d0: date,
    d1: date,
    total_effort: float,
    daily_load: Dict[str, Dict[date, float]],
    emp_fte: Dict[str, float],
    max_utilization: float = 1.0,
) -> Tuple[bool, float]:
    """
    Check if employee has capacity for a task BEFORE assignment.

    Returns (has_capacity, estimated_peak_util).
    """
    days = daterange(d0, d1)
    if not days:
        return False, 0.0

    cap = float(emp_fte.get(emp_id, 1.0))
    if cap <= 0:
        cap = 0.01

    num_days = len(days)
    weights = [2.0 - (1.5 * i / max(1, num_days - 1)) for i in range(num_days)]
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w * num_days / total_weight for w in weights]

    peak_util = 0.0
    for i, d in enumerate(days):
        current_load = daily_load[emp_id].get(d, 0.0)
        additional_load = total_effort * weights[i] / num_days
        total_load = current_load + additional_load
        util = total_load / cap
        peak_util = max(peak_util, util)

    return peak_util <= max_utilization, peak_util


def add_task_load(
    emp_id: str,
    d0: date,
    d1: date,
    total_effort: float,
    daily_load: Dict[str, Dict[date, float]],
):
    """Add task load to employee's daily schedule with front-loaded distribution."""
    days = daterange(d0, d1)
    if not days:
        return

    num_days = len(days)
    if num_days == 0:
        return

    weights = [2.0 - (1.5 * i / max(1, num_days - 1)) for i in range(num_days)]
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w * num_days / total_weight for w in weights]

    for i, d in enumerate(days):
        if d in daily_load[emp_id]:
            daily_load[emp_id][d] += total_effort * weights[i] / num_days


def estimate_delay_days(
    emp_id: str,
    d0: date,
    d1: date,
    total_effort: float,
    daily_load: Dict[str, Dict[date, float]],
    emp_fte: Dict[str, float],
) -> int:
    """Estimate how many days past d1 the task would be delayed."""
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


# ============================================
# SKILL MATCHING
# ============================================

def person_allocated_skill_total(
    emp_id: str, skills_req: list, people_raw: pd.DataFrame
) -> float:
    """Calculate total allocated skill score for an employee against task requirements."""
    allocated = 0.0
    for s in skills_req:
        sk = s["skill"]
        imp = float(s["skill_importance"])
        prow = people_raw[
            (people_raw["employee_id"] == emp_id) & (people_raw["skill"] == sk)
        ]
        if not prow.empty:
            allocated += float(prow.iloc[0]["proficiency_output"]) * imp
    return allocated


def coverage_missing_and_risk(
    emp_id: str, skills_req: list, people_raw: pd.DataFrame
) -> Tuple[list, float]:
    """Return (missing_skills, coverage_risk_0_100)."""
    total_w = 0.0
    missing_w = 0.0
    missing = []

    for s in skills_req:
        sk = str(s["skill"]).strip()
        imp = float(s["skill_importance"])
        total_w += imp
        prow = people_raw[
            (people_raw["employee_id"] == emp_id) & (people_raw["skill"] == sk)
        ]
        if prow.empty:
            missing.append(sk)
            missing_w += imp

    if total_w <= 0:
        return missing, 0.0
    return missing, float(clamp01(missing_w / total_w) * 100.0)


def has_mandatory_skills(
    emp_id: str,
    skills_req: list,
    mandatory_threshold: int,
    people_raw: pd.DataFrame,
) -> bool:
    """Check if employee has all mandatory skills (importance >= threshold)."""
    for s in skills_req:
        skill_importance = float(s["skill_importance"])
        if skill_importance >= mandatory_threshold:
            sk = s["skill"]
            prow = people_raw[
                (people_raw["employee_id"] == emp_id) & (people_raw["skill"] == sk)
            ]
            if prow.empty:
                return False
    return True


def has_minimum_skill_coverage(
    emp_id: str,
    skills_req: list,
    people_raw: pd.DataFrame,
    min_coverage: float = 0.01,
) -> bool:
    """
    Check that the employee has at least *some* matching skills for the task.
    Returns False when the employee has zero of the required skills.
    `min_coverage` is a fraction (0-1); default 0.01 means >= 1% weighted coverage.
    """
    if not skills_req:
        return True  # No skills required → everyone qualifies
    total_w = 0.0
    matched_w = 0.0
    for s in skills_req:
        sk = str(s["skill"]).strip()
        imp = float(s["skill_importance"])
        total_w += imp
        prow = people_raw[
            (people_raw["employee_id"] == emp_id) & (people_raw["skill"] == sk)
        ]
        if not prow.empty:
            matched_w += imp
    if total_w <= 0:
        return True
    return (matched_w / total_w) >= min_coverage
