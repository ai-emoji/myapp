# dialog_backup.py
# Dialog backup database

import traceback
import os


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
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QFrame,
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
    ATTENDANCE_INPUT_BG,
    ATTENDANCE_INPUT_BORDER,
    ATTENDANCE_INPUT_FOCUS_BORDER,
    ATTENDANCE_LABEL_COLOR,
)


class DialogBackup(QDialog):
    """
    Mô tả:
        Dialog backup database
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sao lưu dữ liệu")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(500, 550)
        self.setStyleSheet(f"background: {WEEKEND_BG};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Tiêu đề
        title = QLabel("💾 Sao lưu dữ liệu")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {WEEKEND_TITLE_COLOR}; padding: 5px 0;"
        )
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Chọn vị trí lưu file backup database")
        subtitle.setStyleSheet(
            f"font-size: 12px; color: {WEEKEND_SUBTITLE_COLOR}; font-style: italic; padding: 0 0 10px 0;"
        )
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(5)

        # Container với background
        container = QFrame()
        container.setStyleSheet(
            f"QFrame {{ background: {WEEKEND_SECTION_BG}; border: 1px solid {WEEKEND_SECTION_BORDER}; border-radius: 8px; padding: 20px; }}"
        )
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)

        # Đường dẫn file backup
        path_label = QLabel("Đường dẫn lưu file:")
        path_label.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        container_layout.addWidget(path_label)

        # Input và button chọn file
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Chọn nơi lưu file backup...")
        self.path_input.setReadOnly(True)
        self.path_input.setStyleSheet(
            f"""
            QLineEdit {{
                background: {ATTENDANCE_INPUT_BG};
                border: 2px solid {ATTENDANCE_INPUT_BORDER};
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                color: #333;
            }}
            """
        )
        path_layout.addWidget(self.path_input, 1)

        self.btn_browse = QPushButton("📁 Chọn")
        self.btn_browse.setStyleSheet(
            f"""
            QPushButton {{
                background: #6C757D;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{
                background: #5A6268;
            }}
            QPushButton:pressed {{
                background: #4E555B;
            }}
            """
        )
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_location)
        path_layout.addWidget(self.btn_browse)

        container_layout.addLayout(path_layout)

        # Thông tin database hiện tại
        from core.database import Database

        db_path = Database.get_db_path()
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
            size_mb = db_size / (1024 * 1024)
            info_text = f"📊 Kích thước database: {size_mb:.2f} MB ({db_size:,} bytes)"
        else:
            info_text = "⚠️ Database chưa tồn tại"

        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "font-size: 12px; color: #666; padding: 10px; background: #F0F0F0; border-radius: 4px;"
        )
        container_layout.addWidget(info_label)

        main_layout.addWidget(container)
        main_layout.addSpacing(15)

        # Hint label
        hint = QLabel("💡 File backup có thể được sử dụng để khôi phục dữ liệu sau này")
        hint.setStyleSheet(
            f"font-size: 11px; color: #666; font-style: italic; padding: 5px;"
        )
        main_layout.addWidget(hint)
        main_layout.addSpacing(5)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_backup = QPushButton("💾 Sao lưu ngay")
        self.btn_backup.setStyleSheet(
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
            QPushButton:disabled {{
                background: #CCCCCC;
                color: #666666;
            }}
            """
        )
        self.btn_backup.setCursor(Qt.PointingHandCursor)
        self.btn_backup.setMinimumWidth(150)
        self.btn_backup.setEnabled(False)
        self.btn_backup.clicked.connect(self.perform_backup)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_backup)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

    def browse_location(self):
        """Mở dialog chọn nơi lưu file backup"""
        log_to_debug("DialogBackup: browse_location() called")
        try:
            from services.backup_services import BackupService

            # Tạo tên file mặc định
            default_filename = BackupService.get_default_backup_filename()

            # Mở file dialog
            log_to_debug("DialogBackup: Opening QFileDialog.getSaveFileName")
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Chọn nơi lưu file backup",
                default_filename,
                "DuckDB Database (*.duckdb);;All Files (*.*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            log_to_debug(f"DialogBackup: QFileDialog returned: {file_path}")

            if file_path:
                # Đảm bảo có extension .duckdb
                if not file_path.lower().endswith(".duckdb"):
                    file_path += ".duckdb"

                self.path_input.setText(file_path)
                self.btn_backup.setEnabled(True)
                log_to_debug(f"DialogBackup: Selected path: {file_path}")

        except Exception as e:
            log_to_debug(
                f"DialogBackup: browse_location error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(
                self, "Lỗi", f"Không thể mở dialog chọn file: {str(e)}"
            )

    def perform_backup(self):
        """Thực hiện backup database"""
        try:
            backup_path = self.path_input.text().strip()

            if not backup_path:
                QMessageBox.warning(
                    self, "Cảnh báo", "Vui lòng chọn nơi lưu file backup!"
                )
                return

            log_to_debug(f"DialogBackup: Starting backup to {backup_path}")

            from services.backup_services import BackupService

            # Thực hiện backup
            success, message = BackupService.backup_database(backup_path)

            if success:
                QMessageBox.information(self, "Thành công", message)
                log_to_debug(f"DialogBackup: Backup successful - {message}")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", message)
                log_to_debug(f"DialogBackup: Backup failed - {message}")

        except Exception as e:
            error_msg = f"Lỗi khi backup: {str(e)}"
            log_to_debug(
                f"DialogBackup: perform_backup error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self, "Lỗi", error_msg)
