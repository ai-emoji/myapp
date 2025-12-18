# Khai báo thông số UI, font, màu sắc, icon, constants
# Tất cả comment, docstring đều bằng tiếng Việt
import sys
import os

# Kích thước cửa sổ chính
VERSION = "1.0.0"
MIN_MAINWINDOW_WIDTH = 1366
MIN_MAINWINDOW_HEIGHT = 768

MAIN_HEADER_HEIGHT = 140
MAIN_HEIGHT = 598
FOOTER_HEIGHT = 30


# FOOTER
FOOTER_HEIGHT = 30
FOOTER_MIN_WIDTH = 1366
FOOTER_BG: str = "#ADADAD"

# HEADER
HEADER_HEIGHT = 140
HEADER_MIN_WIDTH = 1366
HEADER_1_HEIGHT = 40
HEADER_2_HEIGHT = 100
HEADER_1_BG: str = "#FFF8F8"
HEADER_2_BG: str = "#FFFFFF"
FUNCTON_1_WIDTH = 100  # px, chiều rộng nút chức năng trong header 1
FUNCTON_1_HEIGHT = 39  # px, chiều rộng nút chức năng trong header 1
FUNCTON_2_WIDTH = 100  # px, chiều rộng nút chức năng trong header 1
FUNCTON_2_HEIGHT = 100  # px, chiều rộng nút chức năng trong header 1

# DIALOG COMPANY
DIALOG_COMPANY_WIDTH = 600
DIALOG_COMPANY_HEIGHT = 500
GROUP_COMPANY_HEIGHT = 80
GROUP_4_COMPANY_HEIGHT = 150


# JOB TITLE
JOB_TITLE_MIN_WIDTH = 1366
JOB_TITLE_MIN_HEIGHT = 598
JOB_TITLE_HEADER_HEIGHT = 40
JOB_TITLE_MAIN_HEIGHT = 558
JOB_TITLE_BG_HEADER = "#E6E6E6"
JOB_TITLE_BG_MAIN = "#FFFFFF"
JOB_TITLE_MAIN_1_HEIGHT = 40
JOB_TITLE_MAIN_2_HEIGHT = 518
JOB_TITLE_ROW_HEIGHT = 30

# HOLIDAY
HOLIDAY_MIN_WIDTH = 1366
HOLIDAY_MIN_HEIGHT = 598
HOLIDAY_HEADER_HEIGHT = 40
HOLIDAY_MAIN_HEIGHT = 558
HOLIDAY_BG_HEADER = "#E6E6E6"
HOLIDAY_BG_MAIN = "#FFFFFF"
HOLIDAY_MAIN_1_HEIGHT = 40
HOLIDAY_MAIN_2_HEIGHT = 518
HOLIDAY_ROW_HEIGHT = 30

# Department
DEPARTMENT_MIN_WIDTH = 1366
DEPARTMENT_MIN_HEIGHT = 598
DEPARTMENT_HEADER_HEIGHT = 40
DEPARTMENT_MAIN_HEIGHT = 558
DEPARTMENT_MAIN_1_HEIGHT = 40
DEPARTMENT_MAIN_2_HEIGHT = 518
DEPARTMENT_HEADER_BG = "#E6E6E6"
DEPARTMENT_MAIN_BG = "#FFFFFF"
DEPARTMENT_ROW_HEIGHT = 30

# Employee
EMPLOYEE_MIN_WIDTH = 1366
EMPLOYEE_MIN_HEIGHT = 598
EMPLOYEE_HEADER_HEIGHT = 40
EMPLOYEE_MAIN_HEIGHT = 558
EMPLOYEE_MAIN_1_HEIGHT = 40
EMPLOYEE_MAIN_2_HEIGHT = 518
EMPLOYEE_HEADER_BG = "#E6E6E6"
EMPLOYEE_MAIN_BG = "#FFFFFF"
EMPLOYEE_ROW_HEIGHT = 30
EMPLOYEE_LEFT_PANEL_WIDTH = 366
EMPLOYEE_SEARCH_HEIGHT = 36


# Font & Typography
UI_FONT = "Segoe UI, Inter, Roboto"
TITLE_FONT = 18  # px
CONTENT_FONT = 13  # px
BUTTON_FONT = 14  # px
TABLE_FONT = 13  # px
ROW_SPACING = 6  # px
FONT_WEIGHT_NORMAL = 400
FONT_WEIGHT_SEMIBOLD = 500
FONT_WEIGHT_BOLD = 600

# Color Palette
HOVER_BG = "#8CE4FF"
BUTTON_BG = "#0004FF"
ACTIVE = "#8CE4FF"
HOVER_ROW = "#8CE4FF"
BG_DIALOG = "#FFFFFF"
CANCEL_BUTTON_BG = "#CF0707"
GUIDELINE_COLOR = "#000000"

ODD_ROW_BG = "#F4F4F4"
EVEN_ROW_BG = "#FFFFFF"


# Absence Symbol Dialog
ABSENCE_DIALOG_WIDTH = 750
ABSENCE_DIALOG_HEIGHT = 550
ABSENCE_TABLE_BG = "#FFFFFF"
ABSENCE_TABLE_BORDER = "#E0E0E0"
ABSENCE_TABLE_GRIDLINE = "#F0F0F0"
ABSENCE_HEADER_BG = "#2C3E50"
ABSENCE_HEADER_TEXT = "#FFFFFF"
ABSENCE_ROW_ODD_BG = "#FAFAFA"
ABSENCE_ROW_EVEN_BG = "#FFFFFF"
ABSENCE_ROW_SELECTED_BG = "#E3F2FD"
ABSENCE_TEXT_COLOR = "#000000"
ABSENCE_CHECKBOX_BORDER = "#333333"
ABSENCE_CHECKBOX_CHECKED_BG = "#4CAF50"
ABSENCE_CHECKBOX_UNCHECKED_BG = "#FFFFFF"

# Attendance Symbol Dialog
ATTENDANCE_DIALOG_WIDTH = 750
ATTENDANCE_DIALOG_HEIGHT = 700
ATTENDANCE_BG = "#FFFFFF"
ATTENDANCE_TITLE_COLOR = "#000000"
ATTENDANCE_LABEL_COLOR = "#333333"
ATTENDANCE_INPUT_BG = "#FFFFFF"
ATTENDANCE_INPUT_BORDER = "#D0D0D0"
ATTENDANCE_INPUT_FOCUS_BORDER = "#2C3E50"
ATTENDANCE_CHECKBOX_BORDER = "#333333"
ATTENDANCE_CHECKBOX_CHECKED_BG = "#4CAF50"
ATTENDANCE_CHECKBOX_UNCHECKED_BG = "#FFFFFF"
ATTENDANCE_SECTION_BG = "#F8F9FA"
ATTENDANCE_SECTION_BORDER = "#E0E0E0"

# Weekend Dialog
WEEKEND_DIALOG_WIDTH = 600
WEEKEND_DIALOG_HEIGHT = 400
WEEKEND_BG = "#FFFFFF"
WEEKEND_TITLE_COLOR = "#000000"
WEEKEND_SUBTITLE_COLOR = "#555555"
WEEKEND_CHECKBOX_BORDER = "#333333"
WEEKEND_CHECKBOX_CHECKED_BG = "#4CAF50"
WEEKEND_CHECKBOX_UNCHECKED_BG = "#FFFFFF"
WEEKEND_SECTION_BG = "#F8F9FA"
WEEKEND_SECTION_BORDER = "#E0E0E0"

# Declare Work Shift
DECLARE_WORK_SHIFT_MIN_WIDTH = 1366
DECLARE_WORK_SHIFT_MIN_HEIGHT = 598
DECLARE_WORK_SHIFT_HEADER_HEIGHT = 40
DECLARE_WORK_SHIFT_MAIN_HEIGHT = 558
DECLARE_WORK_SHIFT_BG_HEADER = "#E6E6E6"
DECLARE_WORK_SHIFT_BG_MAIN = "#FFFFFF"
DECLARE_WORK_SHIFT_MAIN_1_HEIGHT = 40
DECLARE_WORK_SHIFT_MAIN_2_HEIGHT = 518
DECLARE_WORK_SHIFT_ROW_HEIGHT = 30
DECLARE_WORK_SHIFT_LEFT_WIDTH = 360
DECLARE_WORK_SHIFT_RIGHT_WIDTH = 1000

# Icon
ICON_HEIGHT = 24  # px, có thể thay đổi theo từng icon
# Chiều rộng icon tự động theo tỉ lệ gốc

# Layout
DEFAULT_MARGIN = 0
DEFAULT_PADDING = 0


# Đường dẫn tài nguyên (icon, ảnh, database, stylesheet...)
def resource_path(relative_path: str) -> str:
    """
    Mô tả:
        Lấy đường dẫn tuyệt đối đến tài nguyên, hỗ trợ khi build EXE với PyInstaller/Nuitka.
    Args:
        relative_path (str): Đường dẫn tương đối đến file tài nguyên.
    Returns:
        str: Đường dẫn tuyệt đối đến file tài nguyên.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)


# Đường dẫn thư mục ảnh và icon
IMG_PATH = resource_path("assets/images/")
ICON_PATH = resource_path("assets/icons/")

# Khai báo đường dẫn từng file ảnh SVG
ABSENCE_RESTORE_SVG = resource_path("assets/images/absence_restore.svg")
ABSENCE_SYMBOL_SVG = resource_path("assets/images/absence_symbol.svg")
ADD_SVG = resource_path("assets/images/add.svg")
ARRANGE_SCHEDULE_SVG = resource_path("assets/images/arrange_schedule.svg")
ATTENDANCE_SYMBOL_SVG = resource_path("assets/images/attendance_symbol.svg")
BACKUP_SVG = resource_path("assets/images/backup.svg")
COMPANY_SVG = resource_path("assets/images/company.svg")
DELETE_SVG = resource_path("assets/images/delete.svg")
DEPARTMENT_SVG = resource_path("assets/images/department.svg")
DEVICE_SVG = resource_path("assets/images/device.svg")
DOWNLOAD_ATTENDANCE_SVG = resource_path("assets/images/download_attendance.svg")
DOWNLOAD_STAFF_SVG = resource_path("assets/images/download_staff.svg")
DROPDOWN_SVG = resource_path("assets/images/dropdown.svg")
EDIT_SVG = resource_path("assets/images/edit.svg")
EMPLOYEE_SVG = resource_path("assets/images/employee.svg")
EXCEL_SVG = resource_path("assets/images/excel.svg")
EXIT_SVG = resource_path("assets/images/exit.svg")
HOLIDAY_SVG = resource_path("assets/images/holiday.svg")
INPUT_STAFF_NAME_SVG = resource_path("assets/images/input_staff_name.svg")
JOB_TITLE_SVG = resource_path("assets/images/job_title.svg")
LOGIN_SVG = resource_path("assets/images/login.svg")
LOGO_SVG = resource_path("assets/images/logo.svg")
NON_SHIFT_ATTENDANCE_SVG = resource_path("assets/images/non_shift_attendance.svg")
PASSWORD_SVG = resource_path("assets/images/password.svg")
DECLARE_WORK_SHIFT_SVG = resource_path("assets/images/declare_work_shift.svg")
SHIFT_SVG = resource_path("assets/images/shift.svg")
SHIFT_SVG = resource_path("assets/images/shift.svg")
SHIFT_ATTENDANCE_SVG = resource_path("assets/images/shift_attendance.svg")
STAFF_SVG = resource_path("assets/images/staff.svg")
TOTAL_SVG = resource_path("assets/images/total.svg")
UPLOAD_STAFF_SVG = resource_path("assets/images/upload_staff.svg")
WEEKEND_SVG = resource_path("assets/images/weekend.svg")
SAVE_SVG = resource_path("assets/images/save.svg")
REFRESH_SVG = resource_path("assets/images/refresh.svg")

# Đường dẫn file icon app (có thể thay đổi)
APP_ICO_PATH = resource_path("assets/icons/app.ico")


def set_app_ico_path(new_path: str):
    """
    Cập nhật đường dẫn icon ứng dụng.
    Sử dụng resource_path để đảm bảo tương thích khi build exe.
    """
    global APP_ICO_PATH
    import os

    if not os.path.isabs(new_path):
        APP_ICO_PATH = resource_path(new_path)
    else:
        APP_ICO_PATH = new_path


# Đường dẫn file database
# CẢNH BÁO: Không nên thay đổi trong runtime để đảm bảo tính toàn vẹn dữ liệu
DB_PATH = resource_path("database/app.duckdb")


def set_db_path(new_path: str):
    """
    CẢNH BÁO: Chỉ sử dụng khi thực sự cần thiết (testing, migration).
    Thay đổi đường dẫn database trong runtime có thể gây mất dữ liệu.
    """
    global DB_PATH
    if not os.path.isabs(new_path):
        DB_PATH = resource_path(new_path)
    else:
        DB_PATH = new_path
