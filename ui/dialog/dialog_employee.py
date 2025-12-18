import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
    QDateEdit,
    QScrollArea,
    QWidget,
    QLabel,
    QCalendarWidget,
)
from PySide6.QtGui import QIcon, QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import Qt, QDate, QLocale, QRegularExpression

from core.resource import (
    FONT_WEIGHT_BOLD,
    BUTTON_BG,
    CANCEL_BUTTON_BG,
    APP_ICO_PATH,
    BG_DIALOG,
    GUIDELINE_COLOR,
)
from services.employee_services import EmployeeService
from services.department_services import DepartmentService
from services.job_title_services import JobTitleService


class DialogEmployeeBase(QDialog):
    def __init__(self, parent=None, title="Nhân Viên", width=500, height=700):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(width, height)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        self.employee_service = EmployeeService()
        self.department_service = DepartmentService()
        self.job_title_service = JobTitleService()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_widget = QWidget()
        form_layout = QVBoxLayout(scroll_widget)
        form_layout.setAlignment(Qt.AlignTop)

        # Group 1: Thông tin cơ bản
        group_basic = QGroupBox("Thông tin cơ bản")
        form_basic = QFormLayout()
        form_basic.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_basic.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.edit_employee_code = QLineEdit()
        self.edit_employee_code.setPlaceholderText(
            "Mã nhân viên (tự động nếu để trống)"
        )
        self.edit_employee_code.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_employee_code.setValidator(QIntValidator(1, 99999))
        self.edit_employee_code.textChanged.connect(self._on_employee_code_changed)
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("Họ và tên *")
        self.edit_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )

        self.combo_department = QComboBox()
        self.combo_department.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px;"
        )
        self.combo_job_title = QComboBox()
        self.combo_job_title.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px;"
        )
        self.combo_gender = QComboBox()
        self.combo_gender.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px;"
        )
        self.combo_gender.addItems(["", "Nam", "Nữ", "Khác"])

        self.date_hire = QDateEdit()
        self.date_hire.setCalendarPopup(True)
        self.date_hire.setDate(QDate.currentDate())
        self.date_hire.setDisplayFormat("dd/MM/yyyy")
        self.date_hire.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_hire = QCalendarWidget()
        calendar_hire.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_hire.setNavigationBarVisible(True)
        calendar_hire.setMinimumSize(400, 280)
        calendar_hire.setStyleSheet(
            f"""
            QCalendarWidget QTableView {{ 
                selection-background-color: #007bff;
                gridline-color: {GUIDELINE_COLOR};
            }}
            QCalendarWidget QToolButton {{ 
                height: 40px; 
                width: 30px;
                min-width: 30px;
                max-width: 30px;
                background: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                color: black;
            }}
            QCalendarWidget QToolButton:hover {{ 
                background: #e8f4f8;
                border-color: #007bff;
                color: black;
            }}
            QCalendarWidget QToolButton#qt_calendar_monthbutton,
            QCalendarWidget QToolButton#qt_calendar_yearbutton {{
                width: 120px;
                min-width: 120px;
                max-width: 120px;
            }}
            QCalendarWidget QMenu {{
                width: 120px;
                min-width: 120px;
                max-width: 120px;
            }}
            QCalendarWidget QMenu::item {{
                min-width: 100px;
                padding: 4px 8px;
            }}
            QCalendarWidget QSpinBox {{ 
                min-height: 35px;
                background: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{ 
                background-color: #f8f9fa;
                min-height: 50px;
            }}
        """
        )
        self.date_hire.setCalendarWidget(calendar_hire)
        self.date_hire.setStyleSheet(
            "QDateEdit { background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; }"
        )

        form_basic.addRow("Mã NV:", self.edit_employee_code)
        form_basic.addRow("Họ tên:", self.edit_name)
        form_basic.addRow("Phòng ban:", self.combo_department)
        form_basic.addRow("Chức vụ:", self.combo_job_title)
        form_basic.addRow("Giới tính:", self.combo_gender)
        form_basic.addRow("Ngày vào:", self.date_hire)

        group_basic.setLayout(form_basic)
        form_layout.addWidget(group_basic)

        # Group 2: Thông tin chấm công
        group_attendance = QGroupBox("Thông tin chấm công")
        form_attendance = QFormLayout()
        form_attendance.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_attendance.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.edit_attendance_code = QLineEdit()
        self.edit_attendance_code.setPlaceholderText("Mã chấm công")
        self.edit_attendance_code.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_attendance_name = QLineEdit()
        self.edit_attendance_name.setPlaceholderText("Tên chấm công")
        self.edit_attendance_name.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )

        form_attendance.addRow("Mã CC:", self.edit_attendance_code)
        form_attendance.addRow("Tên CC:", self.edit_attendance_name)

        group_attendance.setLayout(form_attendance)
        form_layout.addWidget(group_attendance)

        # Group 3: Thông tin cá nhân
        group_personal = QGroupBox("Thông tin cá nhân")
        form_personal = QFormLayout()
        form_personal.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_personal.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.date_birth = QDateEdit()
        self.date_birth.setCalendarPopup(True)
        self.date_birth.setDate(QDate.currentDate().addYears(-25))
        self.date_birth.setDisplayFormat("dd/MM/yyyy")
        self.date_birth.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_birth = QCalendarWidget()
        calendar_birth.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_birth.setNavigationBarVisible(True)
        calendar_birth.setMinimumSize(400, 280)
        calendar_birth.setStyleSheet(
            f"""
            QCalendarWidget QTableView {{ 
                selection-background-color: #007bff;
                gridline-color: {GUIDELINE_COLOR};
            }}
            QCalendarWidget QToolButton {{ 
                height: 40px; 
                width: 30px;
                min-width: 30px;
                max-width: 30px;
                background: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                color: black;
            }}
            QCalendarWidget QToolButton:hover {{ 
                background: #e8f4f8;
                border-color: #007bff;
                color: black;
            }}
            QCalendarWidget QToolButton#qt_calendar_monthbutton,
            QCalendarWidget QToolButton#qt_calendar_yearbutton {{
                width: 120px;
                min-width: 120px;
                max-width: 120px;
            }}
            QCalendarWidget QMenu {{
                width: 120px;
                min-width: 120px;
                max-width: 120px;
            }}
            QCalendarWidget QMenu::item {{
                min-width: 100px;
                padding: 4px 8px;
            }}
            QCalendarWidget QSpinBox {{ 
                min-height: 35px;
                background: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{ 
                background-color: #f8f9fa;
                min-height: 50px;
            }}
        """
        )
        self.date_birth.setCalendarWidget(calendar_birth)
        self.date_birth.setStyleSheet(
            "QDateEdit { background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; }"
        )

        self.edit_birthplace = QLineEdit()
        self.edit_birthplace.setPlaceholderText("Nơi sinh")
        self.edit_birthplace.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_birthplace.textChanged.connect(self._on_text_capitalize)
        self.edit_hometown = QLineEdit()
        self.edit_hometown.setPlaceholderText("Nguyên quán")
        self.edit_hometown.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_hometown.textChanged.connect(self._on_text_capitalize)

        self.edit_id_number = QLineEdit()
        self.edit_id_number.setPlaceholderText("Số CMND/CCCD")
        self.edit_id_number.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_id_number.setValidator(
            QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        )
        self.edit_id_place = QLineEdit()
        self.edit_id_place.setPlaceholderText("Nơi cấp")
        self.edit_id_place.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_id_place.textChanged.connect(self._on_text_capitalize)

        self.edit_ethnicity = QLineEdit()
        self.edit_ethnicity.setPlaceholderText("Dân tộc")
        self.edit_ethnicity.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_ethnicity.textChanged.connect(self._on_text_capitalize)
        self.edit_nationality = QLineEdit()
        self.edit_nationality.setPlaceholderText("Quốc tịch")
        self.edit_nationality.setText("Việt Nam")
        self.edit_nationality.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )

        form_personal.addRow("Ngày sinh:", self.date_birth)
        form_personal.addRow("Nơi sinh:", self.edit_birthplace)
        form_personal.addRow("Nguyên quán:", self.edit_hometown)
        form_personal.addRow("CMND/CCCD:", self.edit_id_number)
        form_personal.addRow("Nơi cấp:", self.edit_id_place)
        form_personal.addRow("Dân tộc:", self.edit_ethnicity)
        form_personal.addRow("Quốc tịch:", self.edit_nationality)

        group_personal.setLayout(form_personal)
        form_layout.addWidget(group_personal)

        # Group 4: Liên hệ
        group_contact = QGroupBox("Thông tin liên hệ")
        form_contact = QFormLayout()
        form_contact.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_contact.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.edit_address = QLineEdit()
        self.edit_address.setPlaceholderText("Địa chỉ hiện tại")
        self.edit_address.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_address.textChanged.connect(self._on_text_capitalize)
        self.edit_phone = QLineEdit()
        self.edit_phone.setPlaceholderText("Số điện thoại")
        self.edit_phone.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_phone.setValidator(
            QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        )
        self.edit_emergency = QLineEdit()
        self.edit_emergency.setPlaceholderText("Người liên hệ khẩn cấp")
        self.edit_emergency.setStyleSheet(
            "background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; line-height: 28px;"
        )
        self.edit_emergency.textChanged.connect(self._on_text_capitalize)

        form_contact.addRow("Địa chỉ:", self.edit_address)
        form_contact.addRow("Điện thoại:", self.edit_phone)
        form_contact.addRow("Liên hệ KC:", self.edit_emergency)

        group_contact.setLayout(form_contact)
        form_layout.addWidget(group_contact)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.setStyleSheet(
            f"background: {BUTTON_BG}; color: white; padding: 10px 20px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 10px 20px; border-radius: 4px;"
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_save, 1)
        btn_layout.addWidget(self.btn_cancel, 1)
        main_layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.edit_name.textChanged.connect(self._on_name_changed)

        self._load_departments()
        self._load_job_titles()

    def _load_departments(self):
        """Load danh sách phòng ban"""
        self.combo_department.clear()
        self.combo_department.addItem("-- Chọn phòng ban --", None)
        try:
            for dept in self.department_service.get_hierarchy():
                self.combo_department.addItem(dept["display_name"], dept["id"])
        except Exception as e:
            log_to_debug(f"DialogEmployeeBase: Lỗi load departments: {e}")

    def _load_job_titles(self):
        """Load danh sách chức vụ"""
        self.combo_job_title.clear()
        self.combo_job_title.addItem("-- Chọn chức vụ --", None)
        try:
            for title in self.job_title_service.get_all_job_titles():
                self.combo_job_title.addItem(title["name"], title["id"])
        except Exception as e:
            log_to_debug(f"DialogEmployeeBase: Lỗi load job titles: {e}")

    def _on_employee_code_changed(self, text):
        """Chỉ cho phép nhập tối đa 5 chữ số, không tự thêm số 0"""
        sender = self.sender()
        if text and (not text.isdigit() or len(text) > 5):
            # Loại bỏ ký tự không phải số hoặc vượt quá 5 ký tự
            filtered = "".join(filter(str.isdigit, text))[:5]
            pos = sender.cursorPosition()
            sender.blockSignals(True)
            sender.setText(filtered)
            sender.setCursorPosition(min(pos, len(filtered)))
            sender.blockSignals(False)

    def _on_name_changed(self, text):
        """Capitalize first letter"""
        if text and len(text) > 0:
            # Không xử lý nếu đang gõ khoảng trắng
            if text.endswith(" "):
                return
            cap = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
            if text != cap:
                pos = self.edit_name.cursorPosition()
                self.edit_name.blockSignals(True)
                self.edit_name.setText(cap)
                self.edit_name.setCursorPosition(pos)
                self.edit_name.blockSignals(False)

    def _on_text_capitalize(self, text):
        """Capitalize first letter của mỗi từ (Xin Chào)"""
        if text and len(text) > 0:
            # Không xử lý nếu đang gõ khoảng trắng (text kết thúc bằng space)
            if text.endswith(" "):
                return
            sender = self.sender()
            words = text.split()
            capitalized = " ".join(word.capitalize() for word in words)
            if capitalized != text:
                pos = sender.cursorPosition()
                sender.blockSignals(True)
                sender.setText(capitalized)
                sender.setCursorPosition(pos)
                sender.blockSignals(False)

    def _validate(self):
        """Kiểm tra dữ liệu hợp lệ"""
        if not self.edit_name.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên nhân viên!")
            self.edit_name.setFocus()
            return False
        return True


class DialogEmployeeAdd(DialogEmployeeBase):
    def __init__(self, parent=None):
        super().__init__(parent, title="Thêm Nhân Viên Mới")
        log_to_debug("DialogEmployeeAdd: Khởi tạo")
        self.btn_save.clicked.connect(self._on_save)

    def _on_save(self):
        if not self._validate():
            return

        try:
            employee_code = self.edit_employee_code.text().strip() or None

            # Kiểm tra xem mã nhân viên đã tồn tại chưa
            if employee_code and self.employee_service.is_employee_code_exists(
                employee_code
            ):
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    f"Mã nhân viên '{employee_code}' đã tồn tại! Vui lòng chọn mã khác.",
                )
                self.edit_employee_code.setFocus()
                return

            name = self.edit_name.text().strip()
            dept_id = self.combo_department.currentData()
            job_id = self.combo_job_title.currentData()
            gender = self.combo_gender.currentText() or None
            hire_date = self.date_hire.date().toString("yyyy-MM-dd")

            attendance_code = self.edit_attendance_code.text().strip() or None
            attendance_name = self.edit_attendance_name.text().strip() or None
            date_of_birth = self.date_birth.date().toString("yyyy-MM-dd")
            birthplace = self.edit_birthplace.text().strip() or None
            hometown = self.edit_hometown.text().strip() or None
            id_number = self.edit_id_number.text().strip() or None
            id_place_issued = self.edit_id_place.text().strip() or None
            ethnicity = self.edit_ethnicity.text().strip() or None
            nationality = self.edit_nationality.text().strip() or None
            current_address = self.edit_address.text().strip() or None
            phone_number = self.edit_phone.text().strip() or None
            emergency_contact = self.edit_emergency.text().strip() or None

            self.employee_service.add_employee(
                name=name,
                department_id=dept_id,
                job_title_id=job_id,
                employee_code=employee_code,
                gender=gender,
                hire_date=hire_date,
                attendance_code=attendance_code,
                attendance_name=attendance_name,
                date_of_birth=date_of_birth,
                birthplace=birthplace,
                hometown=hometown,
                id_number=id_number,
                id_place_issued=id_place_issued,
                ethnicity=ethnicity,
                nationality=nationality,
                current_address=current_address,
                phone_number=phone_number,
                emergency_contact=emergency_contact,
            )

            QMessageBox.information(self, "Thành công", f"Đã thêm nhân viên: {name}")
            self.accept()
        except Exception as e:
            log_to_debug(f"DialogEmployeeAdd: Lỗi thêm: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm nhân viên:\n{e}")


class DialogEmployeeEdit(DialogEmployeeBase):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent, title="Sửa Thông Tin Nhân Viên")
        log_to_debug("DialogEmployeeEdit: Khởi tạo")

        self.employee_id = employee_data.get("id")
        self.btn_save.clicked.connect(self._on_save)

        # Fill data
        self.edit_employee_code.setText(employee_data.get("employee_code") or "")
        self.edit_name.setText(employee_data.get("name") or "")

        # Set department
        dept_id = employee_data.get("department_id")
        if dept_id:
            for i in range(self.combo_department.count()):
                if self.combo_department.itemData(i) == dept_id:
                    self.combo_department.setCurrentIndex(i)
                    break

        # Set job title
        job_id = employee_data.get("job_title_id")
        if job_id:
            for i in range(self.combo_job_title.count()):
                if self.combo_job_title.itemData(i) == job_id:
                    self.combo_job_title.setCurrentIndex(i)
                    break

        self.combo_gender.setCurrentText(employee_data.get("gender") or "")

        hire_date = employee_data.get("hire_date")
        if hire_date:
            hire_date_str = (
                str(hire_date) if not isinstance(hire_date, str) else hire_date
            )
            self.date_hire.setDate(QDate.fromString(hire_date_str, "yyyy-MM-dd"))

        self.edit_attendance_code.setText(employee_data.get("attendance_code") or "")
        self.edit_attendance_name.setText(employee_data.get("attendance_name") or "")

        dob = employee_data.get("date_of_birth")
        if dob:
            dob_str = str(dob) if not isinstance(dob, str) else dob
            self.date_birth.setDate(QDate.fromString(dob_str, "yyyy-MM-dd"))

        self.edit_birthplace.setText(employee_data.get("birthplace") or "")
        self.edit_hometown.setText(employee_data.get("hometown") or "")
        self.edit_id_number.setText(employee_data.get("id_number") or "")
        self.edit_id_place.setText(employee_data.get("id_place_issued") or "")
        self.edit_ethnicity.setText(employee_data.get("ethnicity") or "")
        self.edit_nationality.setText(employee_data.get("nationality") or "")
        self.edit_address.setText(employee_data.get("current_address") or "")
        self.edit_phone.setText(employee_data.get("phone_number") or "")
        self.edit_emergency.setText(employee_data.get("emergency_contact") or "")

    def _on_save(self):
        if not self._validate():
            return

        try:
            employee_code = self.edit_employee_code.text().strip() or None

            # Kiểm tra xem mã nhân viên đã tồn tại chưa (loại trừ nhân viên hiện tại)
            if employee_code and self.employee_service.is_employee_code_exists(
                employee_code, exclude_emp_id=self.employee_id
            ):
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    f"Mã nhân viên '{employee_code}' đã tồn tại! Vui lòng chọn mã khác.",
                )
                self.edit_employee_code.setFocus()
                return

            name = self.edit_name.text().strip()
            dept_id = self.combo_department.currentData()
            job_id = self.combo_job_title.currentData()
            gender = self.combo_gender.currentText() or None
            hire_date = self.date_hire.date().toString("yyyy-MM-dd")

            attendance_code = self.edit_attendance_code.text().strip() or None
            attendance_name = self.edit_attendance_name.text().strip() or None
            date_of_birth = self.date_birth.date().toString("yyyy-MM-dd")
            birthplace = self.edit_birthplace.text().strip() or None
            hometown = self.edit_hometown.text().strip() or None
            id_number = self.edit_id_number.text().strip() or None
            id_place_issued = self.edit_id_place.text().strip() or None
            ethnicity = self.edit_ethnicity.text().strip() or None
            nationality = self.edit_nationality.text().strip() or None
            current_address = self.edit_address.text().strip() or None
            phone_number = self.edit_phone.text().strip() or None
            emergency_contact = self.edit_emergency.text().strip() or None

            self.employee_service.update_employee(
                emp_id=self.employee_id,
                name=name,
                department_id=dept_id,
                job_title_id=job_id,
                employee_code=employee_code,
                gender=gender,
                hire_date=hire_date,
                attendance_code=attendance_code,
                attendance_name=attendance_name,
                date_of_birth=date_of_birth,
                birthplace=birthplace,
                hometown=hometown,
                id_number=id_number,
                id_place_issued=id_place_issued,
                ethnicity=ethnicity,
                nationality=nationality,
                current_address=current_address,
                phone_number=phone_number,
                emergency_contact=emergency_contact,
            )

            QMessageBox.information(
                self, "Thành công", f"Đã cập nhật nhân viên: {name}"
            )
            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogEmployeeEdit: Lỗi cập nhật: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật:\n{e}")


class DialogEmployeeDelete(QDialog):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.setWindowTitle("Xác Nhận Xóa Nhân Viên")
        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(400, 200)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        self.employee_id = employee_data.get("id")
        self.employee_name = employee_data.get("name")
        self.employee_service = EmployeeService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Warning message
        msg = QLabel(f"Bạn có chắc chắn muốn xóa nhân viên:\n\n'{self.employee_name}'?")
        msg.setStyleSheet("font-size: 14px; padding: 10px;")
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_delete = QPushButton("Xóa")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_delete.setStyleSheet(
            "background: #d32f2f; color: white; padding: 10px 20px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 10px 20px; border-radius: 4px;"
        )
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_delete, 1)
        btn_layout.addWidget(self.btn_cancel, 1)
        layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_delete.clicked.connect(self._on_delete)

    def _on_delete(self):
        try:
            self.employee_service.delete_employee(self.employee_id)
            QMessageBox.information(
                self, "Thành công", f"Đã xóa nhân viên: {self.employee_name}"
            )
            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogEmployeeDelete: Lỗi xóa: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa:\n{e}")
