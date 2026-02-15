"""
LYNX Resource Planning System - Data Parsers

Pure functions for parsing Excel data, skills, dates, and T-shirt sizing.
No Streamlit dependency - can be tested independently.
"""

import re
import numpy as np
import pandas as pd
from datetime import datetime, date


def to_date(v):
    """Convert various date formats to a Python date object."""
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
    text_mapping = {"XS": 0.5, "S": 1.0, "M": 2.0, "L": 4.0, "XL": 8.0}
    numeric_mapping = {1: 0.5, 2: 1.0, 3: 2.0, 4: 4.0, 5: 8.0}

    if pd.isna(s):
        return 2.0

    s_str = str(s).strip().upper()
    if s_str in text_mapping:
        return text_mapping[s_str]

    try:
        num_val = int(float(s))
        if 1 <= num_val <= 5:
            return numeric_mapping[num_val]
    except (ValueError, TypeError):
        pass

    return 2.0


def parse_skills_importance_cell(v, max_items: int = 3):
    """Parse skills and importance from cell.

    Supports formats:
    - "Systems Engineering (5); Product Management (4); Effective Communication (4)"
    - "1. Requirements Engineering - 5\\n2. ADAS System Knowledge - 4"
    - "Skill Name (5)" or "Skill Name - 5"
    """
    if v is None or (isinstance(v, float) and np.isnan(v)) or pd.isna(v):
        return []
    s = str(v).strip()
    if not s:
        return []

    parts = re.split(r";\s*|[\n\r]+", s)
    out = []

    for p in parts:
        p = str(p).strip()
        if not p:
            continue

        skill = None
        imp = None

        # Priority 1: Format "Skill Name (5)"
        m1 = re.match(r"^\s*(.+?)\s*\(\s*(\d+(?:\.\d+)?)\s*\)\s*$", p)
        if m1:
            skill = m1.group(1).strip()
            imp = float(m1.group(2))
            if skill:
                out.append({"skill": skill, "skill_importance": imp})
                if len(out) >= max_items:
                    break
                continue

        # Priority 2: Format "1. Skill Name - 5" or "Skill Name - 5"
        m2 = re.match(
            r"^\s*(?:\d+\s*[\.|\)]\s*)?(.*?)\s*[-\u2013\u2014:]\s*(\d+(?:\.\d+)?)\s*$",
            p,
        )
        if m2:
            skill = m2.group(1).strip()
            imp = float(m2.group(2))
        if skill:
            out.append({"skill": skill, "skill_importance": imp})
            if len(out) >= max_items:
                break
            continue

        # Priority 3: Format "Skill Name 5" or "Skill Name(5)"
        m3 = re.match(r"^\s*(.+?)\s*\(?\s*(\d+(?:\.\d+)?)\s*\)?\s*$", p)
        if m3:
            skill = m3.group(1).strip(" -\u2013\u2014:\t()")
            imp = float(m3.group(2))
            if skill and skill.lower() not in ["nan", "none"]:
                out.append({"skill": skill, "skill_importance": imp})
                if len(out) >= max_items:
                    break

    return out


def normalize_columns(df):
    """Normalize column names to lowercase and handle duplicates."""
    normalized = [c.lower().strip() for c in df.columns]
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
