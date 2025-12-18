# dialog_absence_symbol.py
# Dialog cấu hình các ký hiệu loại vắng

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
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QCheckBox,
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from core.resource import (
    BG_DIALOG,
    BUTTON_BG,
    ABSENCE_DIALOG_WIDTH,
    ABSENCE_DIALOG_HEIGHT,
    ABSENCE_TABLE_BG,
    ABSENCE_TABLE_BORDER,
    ABSENCE_TABLE_GRIDLINE,
    ABSENCE_HEADER_BG,
    ABSENCE_HEADER_TEXT,
    ABSENCE_ROW_ODD_BG,
    ABSENCE_ROW_EVEN_BG,
    ABSENCE_ROW_SELECTED_BG,
    ABSENCE_TEXT_COLOR,
)


def create_emoji_checkbox(checked=False):
    """Tạo checkbox với emoji ✅/❌"""
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

    return checkbox


class DialogAbsenceSymbol(QDialog):
    """
    Mô tả:
        Dialog hiển thị và cấu hình các ký hiệu loại vắng
    Args:
        parent: QWidget cha (nếu có)
    Returns:
        None
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Các ký hiệu loại vắng")
        from core.resource import APP_ICO_PATH

        self.setWindowIcon(QIcon(APP_ICO_PATH))
        self.setFixedSize(ABSENCE_DIALOG_WIDTH, ABSENCE_DIALOG_HEIGHT)
        self.setStyleSheet(f"background: {BG_DIALOG};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Tiêu đề
        from PySide6.QtWidgets import QLabel

        title = QLabel("Cấu hình các ký hiệu loại vắng")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {ABSENCE_TEXT_COLOR}; padding: 5px 0;"
        )
        main_layout.addWidget(title)
        main_layout.addSpacing(5)

        # Tạo bảng
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Mã", "Mô tả", "Ký hiệu", "Sử dụng", "Tính công"]
        )

        # Styling cho bảng với màu text luôn đen khi select
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                background: {ABSENCE_TABLE_BG};
                border: 2px solid {ABSENCE_TABLE_BORDER};
                border-radius: 6px;
                gridline-color: {ABSENCE_TABLE_GRIDLINE};
                selection-background-color: {ABSENCE_ROW_SELECTED_BG};
                selection-color: {ABSENCE_TEXT_COLOR};
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                color: {ABSENCE_TEXT_COLOR};
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {ABSENCE_ROW_SELECTED_BG};
                color: {ABSENCE_TEXT_COLOR};
            }}
            QTableWidget::item:alternate {{
                background: {ABSENCE_ROW_ODD_BG};
            }}
            QHeaderView::section {{
                background: {ABSENCE_HEADER_BG};
                color: {ABSENCE_HEADER_TEXT};
                padding: 12px 8px;
                border: none;
                border-right: 1px solid {ABSENCE_TABLE_BORDER};
                font-weight: bold;
                font-size: 13px;
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}
        """
        )

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(
            QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setShowGrid(True)

        # Thiết lập độ rộng cột
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)

        self.table.setColumnWidth(0, 90)  # Mã
        self.table.setColumnWidth(2, 110)  # Ký hiệu
        self.table.setColumnWidth(3, 110)  # Sử dụng
        self.table.setColumnWidth(4, 110)  # Tính công

        # Thiết lập row height
        self.table.verticalHeader().setDefaultSectionSize(45)

        main_layout.addWidget(self.table)
        main_layout.addSpacing(15)

        # Ghi chú hướng dẫn
        from PySide6.QtWidgets import QLabel

        hint_label = QLabel("💡 Double-click vào ô Mô tả hoặc Ký hiệu để chỉnh sửa")
        hint_label.setStyleSheet(
            f"font-size: 12px; color: #666; font-style: italic; padding: 5px;"
        )
        main_layout.addWidget(hint_label)
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
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setMinimumWidth(150)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # Kết nối signal
        self.btn_save.clicked.connect(self.save_and_close)
        self.table.itemChanged.connect(self.on_item_changed)

        # Load dữ liệu
        self.load_data()

    def load_data(self):
        """Load dữ liệu từ database và hiển thị trong bảng"""
        try:
            log_to_debug("DialogAbsenceSymbol: load_data() called")
            from services.absence_symbol_services import AbsenceSymbolService

            service = AbsenceSymbolService()
            symbols = service.get_all()

            # Block signal khi load data để tránh trigger itemChanged
            self.table.blockSignals(True)
            self.table.setRowCount(len(symbols))

            for row_idx, symbol in enumerate(symbols):
                # Cột Mã
                code_item = QTableWidgetItem(symbol["code"])
                code_item.setData(Qt.UserRole, symbol["id"])
                self.table.setItem(row_idx, 0, code_item)

                # Cột Mô tả
                desc_item = QTableWidgetItem(symbol["description"])
                self.table.setItem(row_idx, 1, desc_item)

                # Cột Ký hiệu
                symbol_item = QTableWidgetItem(symbol["symbol"])
                self.table.setItem(row_idx, 2, symbol_item)

                # Checkbox Sử dụng
                used_widget = QWidget()
                used_layout = QHBoxLayout(used_widget)
                used_layout.setContentsMargins(0, 0, 0, 0)
                used_layout.setAlignment(Qt.AlignCenter)
                used_checkbox = create_emoji_checkbox(symbol["is_used"])
                used_checkbox.setProperty("row", row_idx)
                used_checkbox.setProperty("id", symbol["id"])
                used_layout.addWidget(used_checkbox)
                self.table.setCellWidget(row_idx, 3, used_widget)

                # Checkbox Tính công
                paid_widget = QWidget()
                paid_layout = QHBoxLayout(paid_widget)
                paid_layout.setContentsMargins(0, 0, 0, 0)
                paid_layout.setAlignment(Qt.AlignCenter)
                paid_checkbox = create_emoji_checkbox(symbol["is_paid"])
                paid_checkbox.setProperty("row", row_idx)
                paid_checkbox.setProperty("id", symbol["id"])
                paid_layout.addWidget(paid_checkbox)
                self.table.setCellWidget(row_idx, 4, paid_widget)

            # Unblock signal sau khi load xong
            self.table.blockSignals(False)

            log_to_debug(f"DialogAbsenceSymbol: Loaded {len(symbols)} symbols")
        except Exception as e:
            log_to_debug(
                f"DialogAbsenceSymbol: load_data() error: {e}\n{traceback.format_exc()}"
            )

    def on_item_changed(self, item):
        """Xử lý khi item trong bảng thay đổi (sửa trực tiếp)"""
        try:
            row = item.row()
            col = item.column()

            # Chỉ cho phép sửa cột Mô tả (1) và Ký hiệu (2)
            if col not in [1, 2]:
                return

            log_to_debug(f"DialogAbsenceSymbol: Item changed at row={row}, col={col}")
        except Exception as e:
            log_to_debug(
                f"DialogAbsenceSymbol: on_item_changed() error: {e}\n{traceback.format_exc()}"
            )

    def save_and_close(self):
        """Lưu tất cả thay đổi và đóng dialog"""
        try:
            log_to_debug("DialogAbsenceSymbol: save_and_close() called")
            from services.absence_symbol_services import AbsenceSymbolService

            service = AbsenceSymbolService()
            success_count = 0

            for row in range(self.table.rowCount()):
                # Lấy ID từ item
                symbol_id = self.table.item(row, 0).data(Qt.UserRole)

                # Lấy dữ liệu từ bảng
                code = self.table.item(row, 0).text()
                description = self.table.item(row, 1).text()
                symbol = self.table.item(row, 2).text()

                # Lấy trạng thái checkbox
                is_used = self.table.cellWidget(row, 3).findChild(QCheckBox).isChecked()
                is_paid = self.table.cellWidget(row, 4).findChild(QCheckBox).isChecked()

                # Cập nhật vào database
                if service.update(
                    symbol_id, code, description, symbol, is_used, is_paid
                ):
                    success_count += 1
                    log_to_debug(
                        f"DialogAbsenceSymbol: Updated row {row} (id={symbol_id})"
                    )
                else:
                    log_to_debug(
                        f"DialogAbsenceSymbol: Failed to update row {row} (id={symbol_id})"
                    )

            log_to_debug(
                f"DialogAbsenceSymbol: Saved {success_count}/{self.table.rowCount()} records"
            )
            self.accept()

        except Exception as e:
            log_to_debug(
                f"DialogAbsenceSymbol: save_and_close() error: {e}\n{traceback.format_exc()}"
            )
