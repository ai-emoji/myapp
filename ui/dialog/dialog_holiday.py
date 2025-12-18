import traceback


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        # Nếu ghi log lỗi, in ra stderr
        print(f"[LogError] {e}")


# Dialog ngày nghỉ
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QDateEdit,
    QCalendarWidget,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate, QLocale

from core.resource import (
    FONT_WEIGHT_BOLD,
    BUTTON_BG,
    CANCEL_BUTTON_BG,
    DELETE_SVG,
    BG_DIALOG,
    GUIDELINE_COLOR,
)


class DialogHolidayBase(QDialog):
    """
    Mô tả:
            Dialog cơ bản cho ngày nghỉ
    Args:
            parent: QWidget cha (nếu có)
    Returns:
            None
    """

    def __init__(self, parent=None, title="Dialog Ngày Nghỉ", width=400, height=280):
        super().__init__(parent)
        self.setWindowTitle(title)
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(width, height)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        main_layout = QVBoxLayout(self)
        from PySide6.QtCore import Qt

        main_layout.setAlignment(Qt.AlignTop)

        # Group: Ngày nghỉ
        group_date = QGroupBox("Ngày nghỉ")
        group_date.setFixedHeight(80)
        form_date = QFormLayout()
        self.edit_holiday_date = QDateEdit()
        self.edit_holiday_date.setCalendarPopup(True)
        self.edit_holiday_date.setDate(QDate.currentDate())
        self.edit_holiday_date.setDisplayFormat("dd-MM-yyyy")
        self.edit_holiday_date.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_holiday = QCalendarWidget()
        calendar_holiday.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_holiday.setNavigationBarVisible(True)
        calendar_holiday.setMinimumSize(400, 280)
        calendar_holiday.setStyleSheet(
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
        self.edit_holiday_date.setCalendarWidget(calendar_holiday)
        self.edit_holiday_date.setStyleSheet(
            "QDateEdit { background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; }"
        )
        form_date.addRow(self.edit_holiday_date)
        group_date.setLayout(form_date)
        main_layout.addWidget(group_date)

        # Group: Tên ngày nghỉ
        group_name = QGroupBox("Tên ngày nghỉ")
        group_name.setFixedHeight(80)
        form_name = QFormLayout()
        self.edit_holiday_name = QLineEdit()
        self.edit_holiday_name.setMaxLength(50)
        self.edit_holiday_name.setPlaceholderText("Nhập tên ngày nghỉ...")
        self.edit_holiday_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_name.addRow(self.edit_holiday_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Tăng khoảng cách giữa input và button
        main_layout.addSpacing(16)

        # Nút lưu và hủy - nằm trên 1 dòng, mỗi nút 50% chiều rộng
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.setStyleSheet(
            f"background: {BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.btn_save, 1)  # 50% chiều rộng
        btn_layout.addWidget(self.btn_cancel, 1)  # 50% chiều rộng
        main_layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)


class DialogHolidayAdd(DialogHolidayBase):
    """
    Mô tả:
            Dialog thêm mới ngày nghỉ
    Args:
            parent: QWidget cha (nếu có)
    Returns:
            None
    """

    def __init__(self, parent=None):
        super().__init__(parent, title="Thêm Ngày Nghỉ Mới", width=400, height=280)
        log_to_debug("DialogHolidayAdd: Khởi tạo")

        # Kết nối signal lưu
        self.btn_save.clicked.connect(self.save_holiday)
        self.edit_holiday_name.textChanged.connect(self._on_text_changed)

    def save_holiday(self):
        try:
            holiday_date = self.edit_holiday_date.date().toString("yyyy-MM-dd")
            holiday_name = self.edit_holiday_name.text().strip()
            if not holiday_name:
                log_to_debug("DialogHolidayAdd: Tên ngày nghỉ trống")
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên ngày nghỉ!")
                return

            log_to_debug(
                f"DialogHolidayAdd: Lưu ngày nghỉ mới: {holiday_date} - {holiday_name}"
            )

            # Gọi service để lưu vào DB
            try:
                from services.holiday_services import HolidayService

                service = HolidayService()

                # Kiểm tra trùng cả date và name
                existing_holidays = service.get_all_holidays()
                for holiday in existing_holidays:
                    if (
                        str(holiday["holiday_date"]) == holiday_date
                        and holiday["name"].lower() == holiday_name.lower()
                    ):
                        log_to_debug(
                            f"DialogHolidayAdd: Ngày nghỉ '{holiday_date} - {holiday_name}' đã tồn tại"
                        )
                        QMessageBox.warning(
                            self,
                            "Cảnh báo",
                            f"Ngày nghỉ '{holiday_date} - {holiday_name}' đã tồn tại!\nVui lòng chọn ngày khác hoặc đặt tên khác.",
                        )
                        return

                if service.add_holiday(holiday_date, holiday_name):
                    log_to_debug(
                        f"DialogHolidayAdd: Ngày nghỉ '{holiday_name}' đã được lưu"
                    )
                else:
                    log_to_debug(
                        f"DialogHolidayAdd: Lỗi lưu ngày nghỉ '{holiday_name}'"
                    )
                    QMessageBox.critical(
                        self, "Lỗi", "Không thể lưu ngày nghỉ. Vui lòng thử lại!"
                    )
                    return
            except Exception as e:
                log_to_debug(
                    f"DialogHolidayAdd: Lỗi lưu ngày nghỉ: {e}\n{traceback.format_exc()}"
                )
                QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")
                return

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogHolidayAdd: Lỗi save_holiday: {e}\n{traceback.format_exc()}"
            )

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu của mỗi từ (Xin Chào)"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu của mỗi từ
        words = text.split()
        capitalized = " ".join(word.capitalize() for word in words)
        if text != capitalized:
            cursor_pos = self.edit_holiday_name.cursorPosition()
            self.edit_holiday_name.blockSignals(True)
            self.edit_holiday_name.setText(capitalized)
            self.edit_holiday_name.setCursorPosition(cursor_pos)
            self.edit_holiday_name.blockSignals(False)


class DialogHolidayEdit(QDialog):
    """
    Mô tả:
            Dialog sửa đổi ngày nghỉ
    Args:
            parent: QWidget cha (nếu có)
            holiday_id: ID của ngày nghỉ cần sửa
    Returns:
            None
    """

    def __init__(self, parent=None, holiday_id=None):
        super().__init__(parent)
        self.holiday_id = holiday_id
        self.setWindowTitle("Sửa Đổi Ngày Nghỉ")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(500, 280)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        log_to_debug(f"DialogHolidayEdit: Khởi tạo (ID: {holiday_id})")

        from PySide6.QtCore import Qt

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Group: Ngày nghỉ
        group_date = QGroupBox("Ngày nghỉ")
        group_date.setFixedHeight(80)
        form_date = QFormLayout()
        self.edit_holiday_date = QDateEdit()
        self.edit_holiday_date.setCalendarPopup(True)
        self.edit_holiday_date.setDate(QDate.currentDate())
        self.edit_holiday_date.setDisplayFormat("yyyy-MM-dd")
        self.edit_holiday_date.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))

        # Tạo calendar widget với style giống dialog_employee
        calendar_widget_edit = QCalendarWidget()
        calendar_widget_edit.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        calendar_widget_edit.setNavigationBarVisible(True)
        calendar_widget_edit.setMinimumSize(400, 280)
        calendar_widget_edit.setStyleSheet(
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
        self.edit_holiday_date.setCalendarWidget(calendar_widget_edit)
        self.edit_holiday_date.setStyleSheet(
            f"QDateEdit {{ font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 0 8px; height: 28px; }}"
        )
        form_date.addRow(self.edit_holiday_date)
        group_date.setLayout(form_date)
        main_layout.addWidget(group_date)

        # Group: Tên ngày nghỉ
        group_name = QGroupBox("Tên ngày nghỉ")
        group_name.setFixedHeight(80)
        form_name = QFormLayout()
        self.edit_holiday_name = QLineEdit()
        self.edit_holiday_name.setMaxLength(50)
        self.edit_holiday_name.setPlaceholderText("Nhập tên ngày nghỉ...")
        self.edit_holiday_name.setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; background: white; border: 1px solid black; border-radius: 4px; padding: 8px 12px;"
        )
        form_name.addRow(self.edit_holiday_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Tăng khoảng cách giữa input và button
        main_layout.addSpacing(16)

        # Nút lưu và hủy
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.setStyleSheet(
            f"background: {BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        self.btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.btn_save, 1)
        btn_layout.addWidget(self.btn_cancel, 1)
        main_layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)

        # Kết nối signal lưu
        self.btn_save.clicked.connect(self.save_holiday)
        self.edit_holiday_name.textChanged.connect(self._on_text_changed)

        # Load dữ liệu ngày nghỉ
        self.load_holiday_data()

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu của mỗi từ (Xin Chào)"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu của mỗi từ
        words = text.split()
        capitalized = " ".join(word.capitalize() for word in words)
        if text != capitalized:
            cursor_pos = self.edit_holiday_name.cursorPosition()
            self.edit_holiday_name.blockSignals(True)
            self.edit_holiday_name.setText(capitalized)
            self.edit_holiday_name.setCursorPosition(cursor_pos)
            self.edit_holiday_name.blockSignals(False)

    def load_holiday_data(self):
        try:
            if self.holiday_id:
                log_to_debug(
                    f"DialogHolidayEdit: Load dữ liệu ngày nghỉ ID {self.holiday_id}"
                )
                # Gọi service để load dữ liệu từ DB
                try:
                    from services.holiday_services import HolidayService

                    service = HolidayService()
                    holiday_info = service.get_holiday_by_id(self.holiday_id)
                    if holiday_info:
                        # Load date
                        date_str = str(holiday_info.get("holiday_date", ""))
                        if date_str:
                            date_obj = QDate.fromString(date_str, "yyyy-MM-dd")
                            self.edit_holiday_date.setDate(date_obj)

                        # Load name
                        self.edit_holiday_name.setText(holiday_info.get("name", ""))
                        log_to_debug(
                            f"DialogHolidayEdit: Loaded holiday: {date_str} - {holiday_info.get('name')}"
                        )
                except Exception as e:
                    log_to_debug(
                        f"DialogHolidayEdit: Lỗi load dữ liệu: {e}\n{traceback.format_exc()}"
                    )
        except Exception as e:
            log_to_debug(
                f"DialogHolidayEdit: Lỗi load_holiday_data: {e}\n{traceback.format_exc()}"
            )

    def save_holiday(self):
        try:
            holiday_date = self.edit_holiday_date.date().toString("yyyy-MM-dd")
            holiday_name = self.edit_holiday_name.text().strip()
            if not holiday_name:
                log_to_debug("DialogHolidayEdit: Tên ngày nghỉ trống")
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên ngày nghỉ!")
                return

            log_to_debug(
                f"DialogHolidayEdit: Lưu ngày nghỉ: {holiday_date} - {holiday_name}"
            )

            # Gọi service để lưu vào DB
            try:
                from services.holiday_services import HolidayService

                service = HolidayService()

                # Kiểm tra trùng cả date và name (trừ chính bản ghi đang edit)
                existing_holidays = service.get_all_holidays()
                for holiday in existing_holidays:
                    if holiday["id"] != self.holiday_id:  # Bỏ qua chính nó
                        if (
                            str(holiday["holiday_date"]) == holiday_date
                            and holiday["name"].lower() == holiday_name.lower()
                        ):
                            log_to_debug(
                                f"DialogHolidayEdit: Ngày nghỉ '{holiday_date} - {holiday_name}' đã tồn tại"
                            )
                            QMessageBox.warning(
                                self,
                                "Cảnh báo",
                                f"Ngày nghỉ '{holiday_date} - {holiday_name}' đã tồn tại!\nVui lòng chọn ngày khác hoặc đặt tên khác.",
                            )
                            return

                if service.update_holiday(self.holiday_id, holiday_date, holiday_name):
                    log_to_debug(
                        f"DialogHolidayEdit: Ngày nghỉ '{holiday_name}' đã được cập nhật"
                    )
                else:
                    log_to_debug(
                        f"DialogHolidayEdit: Lỗi cập nhật ngày nghỉ '{holiday_name}'"
                    )
                    QMessageBox.critical(
                        self, "Lỗi", "Không thể cập nhật ngày nghỉ. Vui lòng thử lại!"
                    )
                    return
            except Exception as e:
                log_to_debug(
                    f"DialogHolidayEdit: Lỗi lưu ngày nghỉ: {e}\n{traceback.format_exc()}"
                )
                QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")
                return

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogHolidayEdit: Lỗi save_holiday: {e}\n{traceback.format_exc()}"
            )

    def _on_text_changed(self, text):
        """Viết hoa chữ cái đầu tiên"""
        if not text:
            return
        # Không xử lý nếu đang gõ khoảng trắng
        if text.endswith(" "):
            return

        # Viết hoa chữ cái đầu tiên, giữ nguyên phần còn lại
        capitalized = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        if text != capitalized:
            cursor_pos = self.edit_holiday_name.cursorPosition()
            self.edit_holiday_name.blockSignals(True)
            self.edit_holiday_name.setText(capitalized)
            self.edit_holiday_name.setCursorPosition(cursor_pos)
            self.edit_holiday_name.blockSignals(False)


class DialogHolidayDelete(QDialog):
    """
    Mô tả:
            Dialog xác nhận xóa ngày nghỉ
    Args:
            parent: QWidget cha (nếu có)
            holiday_name: Tên ngày nghỉ cần xóa
            holiday_id: ID của ngày nghỉ cần xóa
    Returns:
            None
    """

    def __init__(self, parent=None, holiday_date="", holiday_name="", holiday_id=None):
        super().__init__(parent)
        self.holiday_date = holiday_date
        self.holiday_name = holiday_name
        self.holiday_id = holiday_id

        self.setWindowTitle("Xác Nhận Xóa")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(450, 220)
        self.setContentsMargins(10, 20, 10, 20)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        log_to_debug(
            f"DialogHolidayDelete: Khởi tạo (ID: {holiday_id}, Date: {holiday_date}, Tên: {holiday_name})"
        )

        main_layout = QVBoxLayout(self)
        from PySide6.QtCore import Qt

        main_layout.setAlignment(Qt.AlignTop)

        # Input hiển thị thông tin ngày nghỉ
        group_name = QGroupBox("Ngày nghỉ cần xóa")
        group_name.setFixedHeight(70)
        form_name = QFormLayout()
        self.edit_delete_name = QLineEdit()
        self.edit_delete_name.setText(f"{holiday_date} - {holiday_name}")
        self.edit_delete_name.setReadOnly(True)
        self.edit_delete_name.setStyleSheet(
            "background: #f5f5f5; color: #d32f2f; font-weight: bold; padding: 8px 12px;"
        )
        form_name.addRow(self.edit_delete_name)
        group_name.setLayout(form_name)
        main_layout.addWidget(group_name)

        # Icon cảnh báo + thông báo
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)  # Giảm khoảng cách giữa icon và text
        delete_icon = QLabel()
        delete_qicon = QIcon(DELETE_SVG)
        delete_icon.setPixmap(delete_qicon.pixmap(24, 24))  # Icon nhỏ hơn
        header_layout.addWidget(delete_icon)

        message_label = QLabel(
            "Bạn có chắc chắn muốn xóa? Hành động này không thể khôi phục!"
        )
        message_label.setStyleSheet(
            "font-size: 12px; color: #d32f2f; font-weight: bold;"
        )
        message_label.setWordWrap(True)
        header_layout.addWidget(message_label, 1)
        header_layout.addStretch()  # Đẩy về bên trái
        main_layout.addLayout(header_layout)

        # Tăng khoảng cách giữa cảnh báo và button
        main_layout.addSpacing(16)

        # Nút xóa và hủy - nằm trên 1 dòng, mỗi nút 50% chiều rộng
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_confirm = QPushButton("Xóa")
        btn_cancel = QPushButton("Hủy")
        btn_confirm.setStyleSheet(
            f"background: #d32f2f; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;"
        )
        btn_cancel.setStyleSheet(
            f"background: {CANCEL_BUTTON_BG}; color: white; padding: 8px 16px; border-radius: 4px;"
        )
        btn_confirm.setCursor(Qt.PointingHandCursor)
        btn_cancel.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(btn_confirm, 1)  # 50% chiều rộng
        btn_layout.addWidget(btn_cancel, 1)  # 50% chiều rộng
        main_layout.addLayout(btn_layout)

        btn_confirm.clicked.connect(self.confirm_delete)
        btn_cancel.clicked.connect(self.reject)

    def confirm_delete(self):
        try:
            log_to_debug(f"DialogHolidayDelete: Xóa ngày nghỉ ID {self.holiday_id}")

            # Gọi service để xóa từ DB
            try:
                from services.holiday_services import HolidayService

                service = HolidayService()
                if service.delete_holiday(self.holiday_id):
                    log_to_debug(
                        f"DialogHolidayDelete: Ngày nghỉ '{self.holiday_name}' đã được xóa"
                    )
                else:
                    log_to_debug(
                        f"DialogHolidayDelete: Lỗi xóa ngày nghỉ '{self.holiday_name}'"
                    )
            except Exception as e:
                log_to_debug(
                    f"DialogHolidayDelete: Lỗi xóa ngày nghỉ: {e}\n{traceback.format_exc()}"
                )

            self.accept()
        except Exception as e:
            log_to_debug(
                f"DialogHolidayDelete: Lỗi confirm_delete: {e}\n{traceback.format_exc()}"
            )
