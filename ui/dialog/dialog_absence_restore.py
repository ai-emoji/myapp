# dialog_absence_restore.py
# Dialog restore database từ file backup

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
    ATTENDANCE_LABEL_COLOR,
    CANCEL_BUTTON_BG,
)


class DialogAbsenceRestore(QDialog):
    """
    Mô tả:
        Dialog restore database từ file backup
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Khôi phục dữ liệu")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(500, 650)
        self.setStyleSheet(f"background: {WEEKEND_BG};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Tiêu đề
        title = QLabel("🔄 Khôi phục dữ liệu")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {WEEKEND_TITLE_COLOR}; padding: 5px 0;"
        )
        main_layout.addWidget(title)
        # Container với background
        container = QFrame()
        container.setStyleSheet(
            f"QFrame {{ background: {WEEKEND_SECTION_BG}; border: 1px solid {WEEKEND_SECTION_BORDER}; border-radius: 8px; padding: 20px; }}"
        )
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)

        # Đường dẫn file backup
        path_label = QLabel("Chọn file backup:")
        path_label.setStyleSheet(
            f"color: {ATTENDANCE_LABEL_COLOR}; font-size: 13px; font-weight: 500;"
        )
        container_layout.addWidget(path_label)

        # Input và button chọn file
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Chọn file backup (.duckdb)...")
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

        self.btn_browse = QPushButton("📁 Chọn file")
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
        self.btn_browse.clicked.connect(self.browse_backup_file)
        path_layout.addWidget(self.btn_browse)

        container_layout.addLayout(path_layout)

        # Thông tin file được chọn
        self.file_info_label = QLabel("📄 Chưa chọn file")
        self.file_info_label.setStyleSheet(
            "font-size: 12px; color: #666; padding: 10px; background: #F0F0F0; border-radius: 4px;"
        )
        self.file_info_label.setWordWrap(True)
        container_layout.addWidget(self.file_info_label)

        main_layout.addWidget(container)
        main_layout.addSpacing(15)

        # Thông tin database hiện tại
        from core.database import Database

        db_path = Database.get_db_path()
        current_db_info = QLabel(f"📍 Database hiện tại:\n{db_path}")
        current_db_info.setStyleSheet(
            "font-size: 12px; color: #333; padding: 10px; background: #E8F5E9; border-radius: 4px; border-left: 4px solid #4CAF50;"
        )
        current_db_info.setWordWrap(True)
        main_layout.addWidget(current_db_info)
        main_layout.addSpacing(10)
        # Hint label
        hint = QLabel("💡 Dữ liệu hiện tại sẽ được backup tự động trước khi restore")
        hint.setStyleSheet(
            f"font-size: 11px; color: #666; font-style: italic; padding: 5px;"
        )
        main_layout.addWidget(hint)
        main_layout.addSpacing(5)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_restore = QPushButton("🔄 Khôi phục ngay")
        self.btn_restore.setStyleSheet(
            f"""
            QPushButton {{
                background: {CANCEL_BUTTON_BG};
                color: white;
                padding: 12px 30px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background: #B00606;
            }}
            QPushButton:pressed {{
                background: #900505;
            }}
            QPushButton:disabled {{
                background: #CCCCCC;
                color: #666666;
            }}
            """
        )
        self.btn_restore.setCursor(Qt.PointingHandCursor)
        self.btn_restore.setMinimumWidth(150)
        self.btn_restore.setEnabled(False)
        self.btn_restore.clicked.connect(self.perform_restore)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_restore)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

    def browse_backup_file(self):
        """Mở dialog chọn file backup"""
        log_to_debug("DialogAbsenceRestore: browse_backup_file() called")
        try:
            # Mở file dialog
            log_to_debug("DialogAbsenceRestore: Opening QFileDialog.getOpenFileName")
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Chọn file backup để khôi phục",
                "",
                "DuckDB Database (*.duckdb);;All Files (*.*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            log_to_debug(f"DialogAbsenceRestore: QFileDialog returned: {file_path}")

            if file_path:
                self.path_input.setText(file_path)
                log_to_debug(f"DialogAbsenceRestore: Selected file: {file_path}")

                # Hiển thị thông tin file
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    size_mb = file_size / (1024 * 1024)
                    from datetime import datetime

                    mod_time = os.path.getmtime(file_path)
                    mod_date = datetime.fromtimestamp(mod_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    info_text = f"📄 File: {os.path.basename(file_path)}\n"
                    info_text += (
                        f"📊 Kích thước: {size_mb:.2f} MB ({file_size:,} bytes)\n"
                    )
                    info_text += f"📅 Ngày tạo: {mod_date}"

                    self.file_info_label.setText(info_text)
                    self.btn_restore.setEnabled(True)
                else:
                    self.file_info_label.setText("❌ File không tồn tại")
                    self.btn_restore.setEnabled(False)

        except Exception as e:
            log_to_debug(
                f"DialogAbsenceRestore: browse_backup_file error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(
                self, "Lỗi", f"Không thể mở dialog chọn file: {str(e)}"
            )

    def perform_restore(self):
        """Thực hiện restore database"""
        try:
            backup_path = self.path_input.text().strip()

            if not backup_path:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file backup!")
                return

            # Xác nhận lần cuối
            reply = QMessageBox.question(
                self,
                "Xác nhận",
                "Bạn có chắc chắn muốn khôi phục dữ liệu?\n\n"
                "Dữ liệu hiện tại sẽ bị ghi đè!\n\n"
                "Ứng dụng sẽ cần khởi động lại sau khi hoàn tất.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply != QMessageBox.Yes:
                return

            log_to_debug(f"DialogAbsenceRestore: Starting restore from {backup_path}")

            from services.backup_services import BackupService

            # Thực hiện restore
            success, message = BackupService.restore_database(backup_path)

            if success:
                QMessageBox.information(
                    self,
                    "Thành công",
                    f"{message}\n\nVui lòng đóng và mở lại ứng dụng để áp dụng thay đổi.",
                )
                log_to_debug(f"DialogAbsenceRestore: Restore successful - {message}")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", message)
                log_to_debug(f"DialogAbsenceRestore: Restore failed - {message}")

        except Exception as e:
            error_msg = f"Lỗi khi restore: {str(e)}"
            log_to_debug(
                f"DialogAbsenceRestore: perform_restore error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self, "Lỗi", error_msg)
