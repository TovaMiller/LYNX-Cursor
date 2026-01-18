# Specific Employee Recommendations - Implementation Guide

## Summary
Enhanced the Action Items section to show **SPECIFIC employee names** who can be reallocated to unassigned tasks, instead of just saying "consider reallocating". This makes recommendations immediately actionable.

---

## 🎯 What Changed

### Before (Not Actionable)
```
⚡ IMMEDIATE ACTION - Reallocate now: 1 overdue task can be saved.
   → Who to reallocate: Check employees with matching skills who have capacity.
```
❌ **Problem**: Tells you to "check" but doesn't tell you WHO

---

### After (Immediately Actionable)
```
⚡ IMMEDIATE ACTION - Reallocate now: 1 overdue task can be saved.

🎯 Specific Recommendations:

**WTR-1234: Sensor Integration** (13 days overdue)
   Required skills: Embedded Systems, SDLC
   👥 Suggested employees to reallocate:
      1. john.doe@company.com - Low workload (2 tasks) ✓
      2. jane.smith@company.com - Medium workload (4 tasks) ✓
      3. bob.jones@company.com - High workload (7 tasks) ✓
```
✅ **Solution**: Shows exact people, their workload, and priority order

---

## 🔧 New Features

### 1. **Smart Employee Matching Function**

**What it does:**
- Finds employees who have ALL required skills for a task
- Checks their current workload (# of assigned tasks)
- Sorts by workload (lowest first = most available)
- Returns top 3 best candidates

**Code:**
```python
def find_employees_for_task(required_skills_str: str, assigned_tasks_df, max_results: int = 3):
    # Parse required skills
    # Find employees with ALL skills
    # Calculate current workload
    # Sort by workload (lowest first)
    # Return top candidates
```

---

### 2. **Detailed Overdue Task Recommendations**

**When shown:** Tasks are already past due AND can be assigned to existing team

**Example output:**
```
🎯 Specific Recommendations:

**WTR-1234: Sensor Integration** (13 days overdue)
   Required skills: Embedded Systems, SDLC
   👥 Suggested employees to reallocate:
      1. john.doe@company.com - Low workload (2 tasks) ✓
      2. jane.smith@company.com - Medium workload (4 tasks) ✓

**WTR-5678: API Design** (8 days overdue)
   Required skills: System Integration
   👥 Suggested employees to reallocate:
      1. alice.wang@company.com - Low workload (1 tasks) ✓
      2. charlie.brown@company.com - Medium workload (3 tasks) ✓
```

**Shows:** Top 3 most urgent overdue tasks with employee suggestions

---

### 3. **Alternative Suggestions for "Hiring Too Late" Scenarios**

**When shown:** Tasks need hiring but there's < 40 days until due

**Example:**
```
⚠️ Hiring needed but may be too late: 6 tasks require hiring, but only 5 days until due date.
   → Issue: Hiring takes ~40 days, but tasks are due sooner.

💡 Alternative - Consider reallocation:
   • WTR-9012: Test Framework (Due in 5 days)
     Missing skills: Test Automation, CI/CD
     ⚠️ No exact match found, but consider upskilling or stretching existing team.
```

**Purpose:** Even when no perfect match exists, shows what's needed so you can make informed decisions

---

### 4. **📋 Quick Reallocation Guide Table**

**New section at bottom** with summary table of ALL reallocatable tasks:

| Task ID | Task Name | Due Date | Risk | Suggested Employee 1 | Suggested Employee 2 |
|---------|-----------|----------|------|---------------------|---------------------|
| WTR-1234 | Sensor Integration... | 2026-02-01 | Critical | john.doe (2 tasks) | jane.smith (4 tasks) |
| WTR-5678 | API Design | 2026-02-15 | High | alice.wang (1 tasks) | charlie.brown (3 tasks) |
| WTR-9012 | Test Framework | 2026-03-01 | Medium | bob.jones (3 tasks) | diana.lee (5 tasks) |

**Features:**
- Shows top 10 most urgent tasks
- Two suggested employees per task
- Workload counts in parentheses
- Sortable and filterable

**Action guidance:**
```
💡 Action: Choose employees with lower workload counts for faster turnaround.
```

---

## 🎯 Decision Logic

### How Employees Are Selected

```
For each unassigned task:
  │
  ├─► Parse required skills (e.g., "Embedded Systems, SDLC")
  │
  ├─► Find employees who have ALL required skills
  │    └─► Check people_raw for each employee_id × skill combination
  │
  ├─► For each matching employee:
  │    └─► Count their current assigned tasks (workload)
  │
  ├─► Sort by workload (ascending)
  │    └─► Employee with 2 tasks ranks higher than one with 7 tasks
  │
  └─► Return top 3 candidates
```

### Workload Categories

| Workload | Tasks Assigned | Priority |
|----------|---------------|----------|
| **Low** | 0-2 tasks | 🟢 High priority (most available) |
| **Medium** | 3-5 tasks | 🟡 Good option |
| **High** | 6+ tasks | 🟠 Last resort (busy) |

---

## 💡 How to Use These Recommendations

### Step 1: Review Overdue Tasks
Look at the "🎯 Specific Recommendations" section for overdue tasks

### Step 2: Choose Employee
- Pick employee with **lowest workload** for fastest start
- If all are busy, consider:
  - Removing lower-priority tasks from their plate
  - Extending deadline
  - Escalating for hiring approval

### Step 3: Take Action
- Go to project management tool
- Reassign task to selected employee
- Notify employee and stakeholders
- Update due date if needed (add 7 days for ramp-up)

### Step 4: Reference Quick Guide
- Scroll to "📋 Quick Reallocation Guide" table
- See all reallocatable tasks at a glance
- Plan batch reassignments

---

## 📊 Example: Full Action Items Section

```
Action Items:

🚨 Already overdue: 13 days late (2 tasks)
   → Action required: 1 can be allocated (7 days), 1 require hiring (40 days)
   → Total project impact: 53 days (current delay + resolution time)

⚡ IMMEDIATE ACTION - Reallocate now: 1 overdue task can be saved by 
   reallocating existing employees (7 days to complete).

##### 🎯 Specific Recommendations:

**WTR-1234: Sensor Integration** (13 days overdue)
   Required skills: Embedded Systems, SDLC
   👥 Suggested employees to reallocate:
      1. john.doe@company.com - Low workload (2 tasks) ✓
      2. jane.smith@company.com - Medium workload (4 tasks) ✓
      3. bob.jones@company.com - High workload (7 tasks) ✓

   → Urgency: These tasks are already late. Reassign within 1-2 days to minimize further delay.

⚠️ Additionally: 7 more tasks due within 14 weeks are unassigned.

---

#### 📋 Quick Reallocation Guide
Tasks that can be immediately assigned to existing employees:

[TABLE WITH 10 TASKS AND EMPLOYEE SUGGESTIONS]

💡 Action: Choose employees with lower workload counts for faster turnaround.
```

---

## 🔄 Integration Points

### Data Sources
1. **Skills**: From `people_raw` DataFrame (employee_id × skill)
2. **Workload**: From `assigned_df` (count of assigned tasks per employee)
3. **Tasks**: From `unassigned_df` (tasks marked as UNASSIGNED)

### Related Sections
- **Resource Gaps**: Shows which skills are missing overall
- **Allocation Results** tab: Full assignment details
- **Workload Analysis** tab: Capacity planning

---

## ✅ Benefits

| Before | After |
|--------|-------|
| "Consider reallocating" | "Reallocate to john.doe (2 tasks)" |
| Manual search required | Instant recommendations |
| Unclear who has capacity | Workload counts shown |
| Generic advice | Task-specific suggestions |
| Time-consuming | Actionable in seconds |

---

## 📁 Files Modified

- `/Users/tovamiller/Documents/LYNX/LYNX-Cursor/app.py`
  - **Lines 1733-1770**: Added `find_employees_for_task()` function
  - **Lines 1982-2013**: Added specific recommendations for overdue tasks
  - **Lines 2054-2067**: Added alternative suggestions for hiring-too-late tasks
  - **Lines 2091-2118**: Added Quick Reallocation Guide table

---

## 🧪 Testing Checklist

- [ ] Upload tasks with overdue dates
- [ ] Verify employees with matching skills are shown
- [ ] Check workload counts are accurate
- [ ] Confirm employees are sorted by workload (lowest first)
- [ ] Verify table shows top 10 reallocatable tasks
- [ ] Test with various skill combinations
- [ ] Check behavior when no employees have skills (hiring scenario)

---

## 🚀 Next Steps for Users

1. **Run the app**: `streamlit run app.py`
2. **Upload your data**: Tasks + employees Excel files
3. **Navigate to**: Gantt Chart tab → Scroll to "Project Impact Analysis"
4. **Review recommendations**: Look for employee names with workload counts
5. **Take action**: Reassign tasks in your project management tool
6. **Track results**: Re-run app to see updated metrics

---

**Created**: January 2026
**Version**: 3.0 - Specific Employee Recommendations
