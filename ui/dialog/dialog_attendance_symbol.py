# dialog_attendance_symbol.py
# Dialog cấu hình các ký hiệu chấm công

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
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
    QGridLayout,
    QWidget,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from core.resource import (
    FONT_WEIGHT_BOLD,
    BUTTON_BG,
    CANCEL_BUTTON_BG,
    BG_DIALOG,
    ATTENDANCE_DIALOG_WIDTH,
    ATTENDANCE_DIALOG_HEIGHT,
    ATTENDANCE_BG,
    ATTENDANCE_TITLE_COLOR,
    ATTENDANCE_LABEL_COLOR,
    ATTENDANCE_INPUT_BG,
    ATTENDANCE_INPUT_BORDER,
    ATTENDANCE_INPUT_FOCUS_BORDER,
    ATTENDANCE_SECTION_BG,
    ATTENDANCE_SECTION_BORDER,
)


def create_emoji_checkbox(text="Hiện", checked=False):
    """Tạo checkbox với emoji ✅/❌"""
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)

    checkbox = QCheckBox()
    checkbox.setText("")
    checkbox.setChecked(checked)
    checkbox.setCursor(Qt.PointingHandCursor)

    # Ẩn indicator mặc định, chỉ dùng emoji
    checkbox.setStyleSheet(
        """
        QCheckBox::indicator {
            width: 0;
            height: 0;
        }
        QCheckBox {
            font-size: 20px;
        }
        """
    )

    def update_emoji(is_checked: bool):
        checkbox.setText("✅" if is_checked else "❌")

    update_emoji(checkbox.isChecked())
    checkbox.toggled.connect(update_emoji)

    layout.addWidget(checkbox)

    # Add label if text is provided
    if text:
        label = QLabel(text)
        label.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        layout.addWidget(label)

    return container, checkbox


class DialogAttendanceSymbol(QDialog):
    """
    Mô tả:
        Dialog cấu hình các ký hiệu chấm công
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Các ký hiệu chấm công")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(ATTENDANCE_DIALOG_WIDTH, ATTENDANCE_DIALOG_HEIGHT)
        self.setStyleSheet(f"background: {ATTENDANCE_BG};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Container với background
        from PySide6.QtWidgets import QFrame

        container = QFrame()
        container.setStyleSheet(
            f"QFrame {{ background: {ATTENDANCE_SECTION_BG}; border: 1px solid {ATTENDANCE_SECTION_BORDER}; border-radius: 8px; padding: 15px; }}"
        )
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)

        # Grid layout cho các trường
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        grid_layout.setColumnStretch(0, 4)  # Label column - wider
        grid_layout.setColumnStretch(1, 2)  # Input column
        grid_layout.setColumnStretch(2, 1)  # Checkbox column
        grid_layout.setColumnMinimumWidth(0, 280)  # Min width for labels
        grid_layout.setColumnMinimumWidth(1, 120)  # Min width for inputs
        grid_layout.setColumnMinimumWidth(2, 80)  # Min width for checkbox

        # Kí hiệu đi trễ
        label_late = QLabel("Kí hiệu đi trễ:")
        label_late.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_late.setWordWrap(True)
        self.edit_late = QLineEdit()
        self.edit_late.setMaxLength(10)
        self.edit_late.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        late_checkbox_widget, self.check_show_late = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_late, 0, 0)
        grid_layout.addWidget(self.edit_late, 0, 1)
        grid_layout.addWidget(late_checkbox_widget, 0, 2)

        # Kí hiệu về sớm
        label_early = QLabel("Kí hiệu về sớm:")
        label_early.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_early.setWordWrap(True)
        self.edit_early = QLineEdit()
        self.edit_early.setMaxLength(10)
        self.edit_early.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        early_checkbox_widget, self.check_show_early = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_early, 1, 0)
        grid_layout.addWidget(self.edit_early, 1, 1)
        grid_layout.addWidget(early_checkbox_widget, 1, 2)

        # Kí hiệu đúng giờ
        label_on_time = QLabel("Kí hiệu đúng giờ:")
        label_on_time.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_on_time.setWordWrap(True)
        self.edit_on_time = QLineEdit()
        self.edit_on_time.setMaxLength(10)
        self.edit_on_time.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        on_time_checkbox_widget, self.check_show_on_time = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_on_time, 2, 0)
        grid_layout.addWidget(self.edit_on_time, 2, 1)
        grid_layout.addWidget(on_time_checkbox_widget, 2, 2)

        # Kí hiệu tăng ca
        label_overtime = QLabel("Kí hiệu tăng ca:")
        label_overtime.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_overtime.setWordWrap(True)
        self.edit_overtime = QLineEdit()
        self.edit_overtime.setMaxLength(10)
        self.edit_overtime.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        overtime_checkbox_widget, self.check_show_overtime = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_overtime, 3, 0)
        grid_layout.addWidget(self.edit_overtime, 3, 1)
        grid_layout.addWidget(overtime_checkbox_widget, 3, 2)

        # Kí hiệu thiếu giờ ra
        label_missing_out = QLabel("Kí hiệu thiếu giờ ra:")
        label_missing_out.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_missing_out.setWordWrap(True)
        self.edit_missing_out = QLineEdit()
        self.edit_missing_out.setMaxLength(10)
        self.edit_missing_out.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        missing_out_checkbox_widget, self.check_show_missing_out = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_missing_out, 4, 0)
        grid_layout.addWidget(self.edit_missing_out, 4, 1)
        grid_layout.addWidget(missing_out_checkbox_widget, 4, 2)

        # Kí hiệu thiếu giờ vào
        label_missing_in = QLabel("Kí hiệu thiếu giờ vào:")
        label_missing_in.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_missing_in.setWordWrap(True)
        self.edit_missing_in = QLineEdit()
        self.edit_missing_in.setMaxLength(10)
        self.edit_missing_in.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        missing_in_checkbox_widget, self.check_show_missing_in = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_missing_in, 5, 0)
        grid_layout.addWidget(self.edit_missing_in, 5, 1)
        grid_layout.addWidget(missing_in_checkbox_widget, 5, 2)

        # Kí hiệu vắng (mặc định không chấm công)
        label_absent = QLabel("Kí hiệu vắng (mặc định không chấm công):")
        label_absent.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_absent.setWordWrap(True)
        self.edit_absent = QLineEdit()
        self.edit_absent.setMaxLength(10)
        self.edit_absent.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        absent_checkbox_widget, self.check_show_absent = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_absent, 6, 0)
        grid_layout.addWidget(self.edit_absent, 6, 1)
        grid_layout.addWidget(absent_checkbox_widget, 6, 2)

        # Kí hiệu đúng giờ ca có qua đêm
        label_overnight = QLabel("Kí hiệu đúng giờ ca có qua đêm:")
        label_overnight.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_overnight.setWordWrap(True)
        self.edit_overnight = QLineEdit()
        self.edit_overnight.setMaxLength(10)
        self.edit_overnight.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        overnight_checkbox_widget, self.check_show_overnight = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_overnight, 7, 0)
        grid_layout.addWidget(self.edit_overnight, 7, 1)
        grid_layout.addWidget(overnight_checkbox_widget, 7, 2)

        # Kí hiệu ngày không xếp ca
        label_no_schedule = QLabel("Kí hiệu ngày không xếp ca:")
        label_no_schedule.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        label_no_schedule.setWordWrap(True)
        self.edit_no_schedule = QLineEdit()
        self.edit_no_schedule.setMaxLength(10)
        self.edit_no_schedule.setStyleSheet(
            f"QLineEdit {{ background: {ATTENDANCE_INPUT_BG}; border: 2px solid {ATTENDANCE_INPUT_BORDER}; border-radius: 5px; padding: 8px; font-size: 13px; }}"
            f"QLineEdit:focus {{ border: 2px solid {ATTENDANCE_INPUT_FOCUS_BORDER}; }}"
        )
        no_schedule_checkbox_widget, self.check_show_no_schedule = create_emoji_checkbox("Hiện")
        grid_layout.addWidget(label_no_schedule, 8, 0)
        grid_layout.addWidget(self.edit_no_schedule, 8, 1)
        grid_layout.addWidget(no_schedule_checkbox_widget, 8, 2)

        container_layout.addLayout(grid_layout)
        main_layout.addWidget(container)
        main_layout.addSpacing(15)

        # Hint label
        hint = QLabel(
            "💡 Nhập ký hiệu và đánh dấu 'Hiện' để hiển thị trong báo cáo chấm công"
        )
        hint.setStyleSheet(
            f"font-size: 11px; color: #666; font-style: italic; padding: 5px;"
        )
        main_layout.addWidget(hint)
        main_layout.addSpacing(0)

        # Nút Lưu và Thoát
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        self.btn_save = QPushButton("💾 Lưu và Thoát")
        self.btn_save.setStyleSheet(
            f"""
            QPushButton {{
                background: {BUTTON_BG};
                color: white;
                padding: 12px 30px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background: #0003DD;
            }}
            QPushButton:pressed {{
                background: #0002BB;
            }}
            """
        )
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setMinimumWidth(150)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # Kết nối signal
        self.btn_save.clicked.connect(self.save_symbols)

        # Load dữ liệu hiện tại
        self.load_current_symbols()

    def load_current_symbols(self):
        """Load cấu hình ký hiệu hiện tại từ database"""
        try:
            log_to_debug("DialogAttendanceSymbol: load_current_symbols() called")
            from services.attendance_symbol_services import AttendanceSymbolService

            service = AttendanceSymbolService()
            symbols = service.get_attendance_symbols()

            if symbols:
                self.edit_late.setText(symbols.get("late_symbol", "Tr"))
                self.edit_early.setText(symbols.get("early_leave_symbol", "Sm"))
                self.edit_on_time.setText(symbols.get("on_time_symbol", "X"))
                self.edit_overtime.setText(symbols.get("overtime_symbol", "+"))
                self.edit_missing_out.setText(
                    symbols.get("missing_checkout_symbol", "KR")
                )
                self.edit_missing_in.setText(
                    symbols.get("missing_checkin_symbol", "KV")
                )
                self.edit_absent.setText(symbols.get("absent_symbol", "V"))
                self.edit_overnight.setText(
                    symbols.get("on_time_overnight_symbol", "D")
                )
                self.edit_no_schedule.setText(symbols.get("no_schedule_symbol", "Off"))

                # Load checkbox states
                show_late_val = symbols.get("show_late", True)
                show_early_val = symbols.get("show_early_leave", True)
                show_on_time_val = symbols.get("show_on_time", True)
                show_overtime_val = symbols.get("show_overtime", True)
                show_missing_out_val = symbols.get("show_missing_checkout", True)
                show_missing_in_val = symbols.get("show_missing_checkin", True)
                show_absent_val = symbols.get("show_absent", True)
                show_overnight_val = symbols.get("show_on_time_overnight", True)
                show_no_schedule_val = symbols.get("show_no_schedule", True)

                log_to_debug(
                    f"DialogAttendanceSymbol: Checkbox values from DB - late:{show_late_val}, early:{show_early_val}, on_time:{show_on_time_val}, overtime:{show_overtime_val}, missing_out:{show_missing_out_val}, missing_in:{show_missing_in_val}, absent:{show_absent_val}, overnight:{show_overnight_val}, no_schedule:{show_no_schedule_val}"
                )

                self.check_show_late.setChecked(show_late_val)
                self.check_show_early.setChecked(show_early_val)
                self.check_show_on_time.setChecked(show_on_time_val)
                self.check_show_overtime.setChecked(show_overtime_val)
                self.check_show_missing_out.setChecked(show_missing_out_val)
                self.check_show_missing_in.setChecked(show_missing_in_val)
                self.check_show_absent.setChecked(show_absent_val)
                self.check_show_overnight.setChecked(show_overnight_val)
                self.check_show_no_schedule.setChecked(show_no_schedule_val)

                log_to_debug("DialogAttendanceSymbol: Loaded symbols successfully")
        except Exception as e:
            log_to_debug(
                f"DialogAttendanceSymbol: load_current_symbols() error: {e}\n{traceback.format_exc()}"
            )

    def save_symbols(self):
        """Lưu cấu hình ký hiệu vào database"""
        try:
            log_to_debug("DialogAttendanceSymbol: save_symbols() called")
            from services.attendance_symbol_services import AttendanceSymbolService

            service = AttendanceSymbolService()

            late_symbol = self.edit_late.text().strip() or "Tr"
            early_symbol = self.edit_early.text().strip() or "Sm"
            on_time_symbol = self.edit_on_time.text().strip() or "X"
            overtime_symbol = self.edit_overtime.text().strip() or "+"
            missing_out_symbol = self.edit_missing_out.text().strip() or "KR"
            missing_in_symbol = self.edit_missing_in.text().strip() or "KV"
            absent_symbol = self.edit_absent.text().strip() or "V"
            overnight_symbol = self.edit_overnight.text().strip() or "D"
            no_schedule_symbol = self.edit_no_schedule.text().strip() or "Off"

            # Lấy trạng thái checkbox cho tất cả các trường
            show_late = self.check_show_late.isChecked()
            show_early = self.check_show_early.isChecked()
            show_on_time = self.check_show_on_time.isChecked()
            show_overtime = self.check_show_overtime.isChecked()
            show_missing_out = self.check_show_missing_out.isChecked()
            show_missing_in = self.check_show_missing_in.isChecked()
            show_absent = self.check_show_absent.isChecked()
            show_overnight = self.check_show_overnight.isChecked()
            show_no_schedule = self.check_show_no_schedule.isChecked()

            log_to_debug(
                f"DialogAttendanceSymbol: Checkbox states to save - late:{show_late}, early:{show_early}, on_time:{show_on_time}, overtime:{show_overtime}, missing_out:{show_missing_out}, missing_in:{show_missing_in}, absent:{show_absent}, overnight:{show_overnight}, no_schedule:{show_no_schedule}"
            )

            if service.update_attendance_symbols(
                late_symbol,
                early_symbol,
                on_time_symbol,
                overtime_symbol,
                missing_out_symbol,
                missing_in_symbol,
                absent_symbol,
                overnight_symbol,
                no_schedule_symbol,
                show_late,
                show_early,
                show_on_time,
                show_overtime,
                show_missing_out,
                show_missing_in,
                show_absent,
                show_overnight,
                show_no_schedule,
            ):
                log_to_debug("DialogAttendanceSymbol: Symbols saved successfully")
                self.accept()
            else:
                log_to_debug("DialogAttendanceSymbol: Failed to save symbols")
        except Exception as e:
            log_to_debug(
                f"DialogAttendanceSymbol: save_symbols() error: {e}\n{traceback.format_exc()}"
            )
