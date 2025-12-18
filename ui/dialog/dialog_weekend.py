# dialog_weekend.py
# Dialog cấu hình ngày cuối tuần

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
    QPushButton,
    QLabel,
    QCheckBox,
    QGridLayout,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from core.resource import (
    BUTTON_BG,
    BG_DIALOG,
    WEEKEND_DIALOG_WIDTH,
    WEEKEND_DIALOG_HEIGHT,
    WEEKEND_BG,
    WEEKEND_TITLE_COLOR,
    WEEKEND_SUBTITLE_COLOR,
    WEEKEND_SECTION_BG,
    WEEKEND_SECTION_BORDER,
)


def create_emoji_checkbox(text="", checked=False):
    """Tạo checkbox với emoji ✅/❌"""
    from PySide6.QtWidgets import QWidget, QHBoxLayout
    
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

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
            f"color: {WEEKEND_SUBTITLE_COLOR}; font-size: 14px; font-weight: 500;"
        )
        layout.addWidget(label)

    return container, checkbox


class DialogWeekend(QDialog):
    """
    Mô tả:
        Dialog cấu hình ngày cuối tuần (Thứ 2 - Chủ nhật)
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cấu hình ngày cuối tuần")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(WEEKEND_DIALOG_WIDTH, WEEKEND_DIALOG_HEIGHT)
        self.setStyleSheet(f"background: {WEEKEND_BG};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        # Container với background
        from PySide6.QtWidgets import QFrame

        container = QFrame()
        container.setStyleSheet(
            f"QFrame {{ background: {WEEKEND_SECTION_BG}; border: 1px solid {WEEKEND_SECTION_BORDER}; border-radius: 8px; padding: 8px; }}"
        )
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(5)

        # Grid layout cho các checkbox
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setColumnMinimumWidth(0, 200)
        grid_layout.setColumnMinimumWidth(1, 200)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # Thứ 2
        monday_widget, self.check_monday = create_emoji_checkbox("Thứ 2")
        grid_layout.addWidget(monday_widget, 0, 0)

        # Thứ 3
        tuesday_widget, self.check_tuesday = create_emoji_checkbox("Thứ 3")
        grid_layout.addWidget(tuesday_widget, 0, 1)

        # Thứ 4
        wednesday_widget, self.check_wednesday = create_emoji_checkbox("Thứ 4")
        grid_layout.addWidget(wednesday_widget, 1, 0)

        # Thứ 5
        thursday_widget, self.check_thursday = create_emoji_checkbox("Thứ 5")
        grid_layout.addWidget(thursday_widget, 1, 1)

        # Thứ 6
        friday_widget, self.check_friday = create_emoji_checkbox("Thứ 6")
        grid_layout.addWidget(friday_widget, 2, 0)

        # Thứ 7
        saturday_widget, self.check_saturday = create_emoji_checkbox("Thứ 7")
        grid_layout.addWidget(saturday_widget, 2, 1)

        # Chủ nhật
        sunday_widget, self.check_sunday = create_emoji_checkbox("Chủ nhật")
        grid_layout.addWidget(sunday_widget, 3, 0)

        container_layout.addLayout(grid_layout)
        main_layout.addWidget(container)
        main_layout.addSpacing(15)

        # Hint label
        hint = QLabel("💡 Các ngày được chọn sẽ không tính công khi tính lương")
        hint.setStyleSheet(
            f"font-size: 11px; color: #666; font-style: italic; padding: 5px;"
        )
        main_layout.addWidget(hint)
        main_layout.addSpacing(5)

        # Nút Lưu và Thoát
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
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
        self.btn_save.setMinimumWidth(150)
        self.btn_save.setCursor(Qt.PointingHandCursor)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # Kết nối signal
        self.btn_save.clicked.connect(self.save_config)

        # Load dữ liệu hiện tại
        self.load_current_config()

    def load_current_config(self):
        """Load cấu hình ngày cuối tuần từ database"""
        try:
            log_to_debug("DialogWeekend: load_current_config() called")
            from services.weekend_services import WeekendService

            service = WeekendService()
            config = service.get_weekend_config()

            if config:
                self.check_monday.setChecked(config.get("monday", False))
                self.check_tuesday.setChecked(config.get("tuesday", False))
                self.check_wednesday.setChecked(config.get("wednesday", False))
                self.check_thursday.setChecked(config.get("thursday", False))
                self.check_friday.setChecked(config.get("friday", False))
                self.check_saturday.setChecked(config.get("saturday", True))
                self.check_sunday.setChecked(config.get("sunday", True))

                log_to_debug(
                    f"DialogWeekend: Loaded config - Mon:{config.get('monday')}, Tue:{config.get('tuesday')}, "
                    f"Wed:{config.get('wednesday')}, Thu:{config.get('thursday')}, Fri:{config.get('friday')}, "
                    f"Sat:{config.get('saturday')}, Sun:{config.get('sunday')}"
                )
        except Exception as e:
            log_to_debug(
                f"DialogWeekend: load_current_config() error: {e}\n{traceback.format_exc()}"
            )

    def save_config(self):
        """Lưu cấu hình ngày cuối tuần vào database"""
        try:
            log_to_debug("DialogWeekend: save_config() called")
            from services.weekend_services import WeekendService

            service = WeekendService()

            # Lấy trạng thái checkbox
            monday = self.check_monday.isChecked()
            tuesday = self.check_tuesday.isChecked()
            wednesday = self.check_wednesday.isChecked()
            thursday = self.check_thursday.isChecked()
            friday = self.check_friday.isChecked()
            saturday = self.check_saturday.isChecked()
            sunday = self.check_sunday.isChecked()

            log_to_debug(
                f"DialogWeekend: Config to save - Mon:{monday}, Tue:{tuesday}, Wed:{wednesday}, "
                f"Thu:{thursday}, Fri:{friday}, Sat:{saturday}, Sun:{sunday}"
            )

            if service.update_weekend_config(
                monday, tuesday, wednesday, thursday, friday, saturday, sunday
            ):
                log_to_debug("DialogWeekend: Config saved successfully")
                self.accept()
            else:
                log_to_debug("DialogWeekend: Failed to save config")
        except Exception as e:
            log_to_debug(
                f"DialogWeekend: save_config() error: {e}\n{traceback.format_exc()}"
            )
