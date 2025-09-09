# GradeFlow Configuration File

# Application Settings
APP_TITLE = "GradeFlow - Student Grade Management"
APP_ICON = "📊"
LAYOUT = "wide"

# Required Columns (must be present in uploaded files)
REQUIRED_COLUMNS = ["Roll No", "Name", "Gender", "Total"]

# Valid Gender Values (case insensitive)
VALID_GENDERS = ["Male", "Female", "M", "F"]

# Grade Scale Configuration
# Format: "Grade": (min_score, max_score)
GRADE_SCALE = {
    "A+": (90, 100),
    "A": (80, 89),
    "B": (70, 79),
    "C": (60, 69),
    "D": (40, 49),
    "F": (0, 39)
}

# Validation Settings
MIN_SCORE = 0
MAX_SCORE = 100
PASSING_SCORE = 40

# File Upload Settings
ALLOWED_FILE_TYPES = ["csv", "xlsx"]
MAX_FILE_SIZE_MB = 200

# Display Settings
DEFAULT_CHART_HEIGHT = 400
DATAFRAME_HEIGHT = 400
SIDEBAR_INITIAL_STATE = "expanded"

# Export Settings
EXPORT_DATE_FORMAT = "%Y%m%d_%H%M"
EXCEL_ENGINE = "openpyxl"
