# 🦊 Lynx Resource Planning System - Enhanced Version

A professional, enterprise-grade resource planning application with enhanced UI/UX for intelligent skill-based resource allocation and capacity planning.

## ✨ Features

- **Professional UI/UX**: Modern, clean interface with color-coded risk indicators
- **Skill-Based Assignment**: Intelligent matching of tasks to employees based on skills and proficiency
- **Capacity Planning**: Real-time workload analysis and utilization tracking
- **Risk Assessment**: Comprehensive risk scoring for skill gaps and schedule delays
- **Interactive Visualizations**: Gantt charts, workload heatmaps, and utilization trends
- **Data Management**: Easy file upload and skill configuration interface

## 📋 Requirements

- Python 3.8 or higher
- All dependencies listed in `requirements.txt`

## 🚀 Quick Start

### 1. Navigate to the project directory

```bash
cd "/Users/tovamiller/Documents/LYNX/Lynx_skill_gantt_enhanced"
```

### 2. Create a virtual environment (recommended)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
Lynx_skill_gantt_enhanced/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── employee_template.xlsx      # Template for employee/skill data
├── task_template.xlsx          # Template for task data
└── README.md                   # This file
```

## 📊 Data Templates

### Tasks Template (`task_template.xlsx`)

Required columns:
- `task_id`: Unique identifier for the task
- `task_name`: Name/description of the task
- `department`: Department or team
- `priority`: Priority level (Critical, High, Medium, Low)
- `start_date`: Planned start date
- `end_date`: Planned end date
- `work_size`: T-shirt size (XS, S, M, L, XL)

### Employee Template (`employee_template.xlsx`)

Required columns:
- `employee_id`: Unique identifier for the employee
- `skill`: Skill name
- `proficiency`: Skill proficiency level (typically 1-5)
- `job_level`: Job level/grade (typically 1-5)
- `fte`: Full-time equivalent (e.g., 1.0 for full-time)

## 🎯 Usage Guide

1. **Upload Data**: 
   - Go to the "📥 Data Input" tab
   - Upload your tasks Excel file (from Jira)
   - Upload your people Excel file (from HiBob + Lattice)

2. **Configure Skills**:
   - Define required skills for each task
   - Set importance levels (1-5) for each skill
   - Skills with importance > threshold are mandatory

3. **Review Allocation**:
   - Check the "📊 Allocation Results" tab for assignments
   - Filter by risk level or assignee
   - Review risk scores and delays

4. **Visualize Timeline**:
   - View the "📅 Gantt Chart" for timeline visualization
   - Tasks are color-coded by risk level

5. **Analyze Workload**:
   - Check "💼 Workload Analysis" for capacity planning
   - View utilization trends and heatmaps
   - Identify overloaded or underutilized employees

6. **Task Details**:
   - Use "🔍 Task Details" to drill into specific tasks
   - Review skill requirements and assignment rationale

## ⚙️ Configuration

### Sidebar Settings

- **Mandatory Skill Threshold**: Skills with importance above this value are required for assignment (default: 3)
- **Prefer Same Department**: Prioritize assignees from the same department as the task (default: enabled)

## 🎨 UI Features

- **Color-Coded Risk Levels**:
  - 🟢 Low (Green)
  - 🟡 Medium (Yellow)
  - 🟠 High (Orange)
  - 🔴 Critical (Red)

- **Interactive Charts**: 
  - Hover for detailed information
  - Zoom and pan on visualizations
  - Filter and sort data tables

- **Real-Time Metrics**: 
  - System status in sidebar
  - Summary statistics on each tab
  - Risk distribution breakdowns

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **File Upload Errors**: 
   - Verify Excel files have the required columns
   - Check that dates are in a valid format
   - Ensure column names match exactly (case-insensitive)

3. **No Assignments**: 
   - Check that skills are defined for tasks
   - Verify employees have matching skills
   - Adjust mandatory skill threshold if needed

## 📝 Notes

- Effort is approximated from t-shirt size (XS=1, S=2, M=3, L=5, XL=8)
- 1.0 FTE is treated as 1 effort unit/day for utilization calculations
- Mandatory skills are enforced when importance > threshold
- Tasks are assigned based on skill match, capacity, and risk minimization

## 🆚 Differences from Original

This enhanced version includes:
- Professional CSS styling and modern UI
- Enhanced visualizations with better color schemes
- Improved information hierarchy and organization
- Interactive filtering and sorting
- Real-time metrics and summaries
- Better error handling and user feedback
- More detailed workload analysis tools

## 📞 Support

For issues or questions, refer to the original documentation or contact your system administrator.

---

**Version**: 2.0 Enhanced  
**Last Updated**: 2024

