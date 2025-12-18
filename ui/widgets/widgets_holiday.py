# widgets_holiday.py
# Widget khai báo ngày nghỉ

import logging
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from core.resource import (
    DELETE_SVG,
    HOLIDAY_MIN_WIDTH,
    HOLIDAY_MIN_HEIGHT,
    HOLIDAY_HEADER_HEIGHT,
    HOLIDAY_BG_HEADER,
    HOLIDAY_MAIN_HEIGHT,
    HOLIDAY_BG_MAIN,
    HOLIDAY_SVG,
    FONT_WEIGHT_SEMIBOLD,
    HOLIDAY_MAIN_1_HEIGHT,
    HOLIDAY_MAIN_2_HEIGHT,
    ADD_SVG,
    EDIT_SVG,
    DELETE_SVG,
    HOLIDAY_ROW_HEIGHT,
    FONT_WEIGHT_BOLD,
    HOVER_ROW,
    ACTIVE,
    TOTAL_SVG,
    ODD_ROW_BG,
    EVEN_ROW_BG,
)


logging.basicConfig(
    filename="debug.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)


class WidgetsHoliday(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_width = HOLIDAY_MIN_WIDTH
        self.min_height = HOLIDAY_MIN_HEIGHT
        self.setMinimumWidth(self.min_width)
        self.setMinimumHeight(self.min_height)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.header = WidgetsHolidayHeader(self)
        self.main = WidgetsHolidayMain(self)
        layout.addWidget(self.header, 0)
        layout.addWidget(self.main, 1)


class WidgetsHolidayHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(HOLIDAY_HEADER_HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background: {HOLIDAY_BG_HEADER};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(8)

        icon_label = QLabel(self)

        icon = QIcon(HOLIDAY_SVG)  # SVG
        pixmap = icon.pixmap(20, 20)  # Qt render vector → nét tuyệt đối
        icon_label.setPixmap(pixmap)

        layout.addWidget(icon_label)

        title_label = QLabel("Khai báo ngày nghỉ", self)
        title_label.setStyleSheet(
            f"font-size: 18px; font-weight: {FONT_WEIGHT_SEMIBOLD}; color: #222;"
        )
        layout.addWidget(title_label)

        layout.addStretch(1)


class WidgetsHolidayMain(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.info("WidgetsHolidayMain initialized")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background: {HOLIDAY_BG_MAIN};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.part1 = QWidget(self)
        self.part1.setObjectName("mainPart1")
        self.part1.setFixedHeight(HOLIDAY_MAIN_1_HEIGHT)
        btn_layout = QHBoxLayout(self.part1)
        btn_layout.setContentsMargins(16, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_add = QPushButton(QIcon(ADD_SVG), "Thêm mới", self.part1)
        btn_edit = QPushButton(QIcon(EDIT_SVG), "Sửa đổi", self.part1)
        btn_delete = QPushButton(QIcon(DELETE_SVG), "Xóa", self.part1)

        btn_add.clicked.connect(self._on_btn_add_clicked)
        btn_edit.clicked.connect(self._on_btn_edit_clicked)
        btn_delete.clicked.connect(self._on_btn_delete_clicked)

        for btn in [btn_add, btn_edit, btn_delete]:
            btn.setFixedSize(100, 36)
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("border: none; font-size: 14px;")
            btn.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(btn)
        # Thêm label tổng sau nút Xóa
        total_label_container = QHBoxLayout()
        total_label_container.setContentsMargins(0, 0, 0, 0)
        total_label_container.setSpacing(4)

        total_icon = QLabel(self.part1)
        total_icon_qicon = QIcon(TOTAL_SVG)
        total_icon.setPixmap(total_icon_qicon.pixmap(16, 16))
        total_label_container.addWidget(total_icon)

        self.total_label = QLabel("Tổng:", self.part1)
        self.total_label.setStyleSheet(
            "font-size: 14px; color: #1976d2; font-weight: bold;"
        )
        self.total_counter = 0  # Khởi tạo bộ đếm
        total_label_container.addWidget(self.total_label)

        btn_layout.addLayout(total_label_container)
        btn_layout.addStretch(1)

        self.part2 = QWidget(self)
        self.part2.setObjectName("mainPart2")
        self.part2.setMinimumHeight(HOLIDAY_MAIN_2_HEIGHT)
        part2_layout = QVBoxLayout(self.part2)
        part2_layout.setContentsMargins(0, 0, 0, 0)
        part2_layout.setSpacing(0)

        # Tạo table với selection behavior là SelectRows
        self.table = QTableWidget(50, 2, self.part2)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setMouseTracking(True)

        self.table.setHorizontalHeaderLabels(["Ngày nghỉ", "Tên ngày nghỉ"])
        self.table.horizontalHeader().setStyleSheet(
            f"font-weight: {FONT_WEIGHT_BOLD}; font-size: 15px;"
        )
        self.table.horizontalHeader().setFixedHeight(40)
        self.table.setColumnWidth(0, 150)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(HOLIDAY_ROW_HEIGHT)
        # Cập nhật stylesheet để hover và select áp dụng cho cả row (cả 2 columns)
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                font-size: 14px;
                gridline-color: #e0e0e0;
                background: {EVEN_ROW_BG};
                alternate-background-color: {ODD_ROW_BG};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:hover {{
                background: {HOVER_ROW};
            }}
            QTableWidget::item:selected {{
                background: {ACTIVE};
                color: black;
            }}
            """
        )
        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)

        # Tạo 50 dòng trống
        for i in range(50):
            # Cột Ngày nghỉ
            item_date = QTableWidgetItem("")
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item_date)

            # Cột Tên ngày nghỉ
            item_name = QTableWidgetItem("")
            item_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(i, 1, item_name)

        part2_layout.addWidget(self.table)
        layout.addWidget(self.part1)
        layout.addWidget(self.part2)

        # Tải dữ liệu ngày nghỉ khi khởi tạo
        self._refresh_holidays()

    def _on_btn_add_clicked(self):
        """Hiển thị dialog thêm mới ngày nghỉ"""
        try:
            logging.info("WidgetsHoliday: btn_add clicked")
            from ui.dialog.dialog_holiday import DialogHolidayAdd

            dialog = DialogHolidayAdd(self)
            # Lấy vị trí cửa sổ chính để đặt dialog ở giữa
            from PySide6.QtCore import Qt

            main_window = self.window()
            geometry = main_window.frameGeometry()
            dialog_geometry = dialog.frameGeometry()
            x = geometry.x() + (geometry.width() - dialog_geometry.width()) // 2
            y = geometry.y() + (geometry.height() - dialog_geometry.height()) // 2
            dialog.move(x, y)

            if dialog.exec() == 1:  # QDialog.Accepted = 1
                logging.info("WidgetsHoliday: Dialog accepted, refreshing data")
                self._refresh_holidays()
        except Exception as e:
            logging.error(f"WidgetsHoliday: Error in _on_btn_add_clicked: {e}")

    def _on_btn_edit_clicked(self):
        """Hiển thị dialog sửa đổi ngày nghỉ"""
        try:
            logging.info("WidgetsHoliday: btn_edit clicked")
            # Lấy dòng được chọn
            selected_row = self.table.currentRow()
            if selected_row < 0:
                logging.warning("WidgetsHoliday: No row selected for edit")
                # Hiển thị cảnh báo
                from PySide6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self, "Cảnh báo", "Vui lòng chọn ngày nghỉ cần sửa đổi!"
                )
                return

            # Lấy ID từ UserRole của item
            holiday_id = self.table.item(selected_row, 0).data(Qt.UserRole)

            from ui.dialog.dialog_holiday import DialogHolidayEdit

            dialog = DialogHolidayEdit(self, holiday_id)
            # Lấy vị trí cửa sổ chính để đặt dialog ở giữa
            main_window = self.window()
            geometry = main_window.frameGeometry()
            dialog_geometry = dialog.frameGeometry()
            x = geometry.x() + (geometry.width() - dialog_geometry.width()) // 2
            y = geometry.y() + (geometry.height() - dialog_geometry.height()) // 2
            dialog.move(x, y)

            if dialog.exec() == 1:  # QDialog.Accepted = 1
                logging.info("WidgetsHoliday: Dialog accepted, refreshing data")
                self._refresh_holidays()
        except Exception as e:
            logging.error(f"WidgetsHoliday: Error in _on_btn_edit_clicked: {e}")

    def _on_btn_delete_clicked(self):
        """Hiển thị dialog xác nhận xóa ngày nghỉ"""
        try:
            logging.info("WidgetsHoliday: btn_delete clicked")
            # Lấy dòng được chọn
            selected_row = self.table.currentRow()
            if selected_row < 0:
                logging.warning("WidgetsHoliday: No row selected for delete")
                # Hiển thị cảnh báo
                from PySide6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self, "Cảnh báo", "Vui lòng chọn ngày nghỉ cần xóa!"
                )
                return

            # Lấy ID và dữ liệu từ dòng
            holiday_id = self.table.item(selected_row, 0).data(Qt.UserRole)
            holiday_date = self.table.item(selected_row, 0).text()
            holiday_name = self.table.item(selected_row, 1).text()

            from ui.dialog.dialog_holiday import DialogHolidayDelete

            dialog = DialogHolidayDelete(self, holiday_date, holiday_name, holiday_id)
            # Lấy vị trí cửa sổ chính để đặt dialog ở giữa
            main_window = self.window()
            geometry = main_window.frameGeometry()
            dialog_geometry = dialog.frameGeometry()
            x = geometry.x() + (geometry.width() - dialog_geometry.width()) // 2
            y = geometry.y() + (geometry.height() - dialog_geometry.height()) // 2
            dialog.move(x, y)

            if dialog.exec() == 1:  # QDialog.Accepted = 1
                logging.info("WidgetsHoliday: Dialog accepted, refreshing data")
                self._refresh_holidays()
        except Exception as e:
            logging.error(f"WidgetsHoliday: Error in _on_btn_delete_clicked: {e}")

    def _refresh_holidays(self):
        """Làm mới dữ liệu ngày nghỉ từ DB"""
        try:
            logging.info("WidgetsHoliday: Refreshing holidays")
            from services.holiday_services import HolidayService

            service = HolidayService()
            holidays = service.get_all_holidays()

            # Đảm bảo luôn có tối thiểu 50 dòng
            row_count = max(50, len(holidays))
            self.table.setRowCount(row_count)

            # Xóa toàn bộ dữ liệu cũ
            for i in range(row_count):
                self.table.setItem(i, 0, QTableWidgetItem(""))
                self.table.setItem(i, 1, QTableWidgetItem(""))

            # Cập nhật bảng với dữ liệu mới
            for row, holiday in enumerate(holidays):
                # Cột Ngày nghỉ - Format từ yyyy-MM-dd sang dd-MM-yyyy
                date_str = str(holiday["holiday_date"])
                from datetime import datetime

                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d-%m-%Y")
                except:
                    formatted_date = date_str  # Fallback nếu format không đúng

                date_item = QTableWidgetItem(formatted_date)
                date_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 0, date_item)

                # Cột Tên
                name_item = QTableWidgetItem(holiday["name"])
                self.table.setItem(row, 1, name_item)

                # Lưu ID vào item để sử dụng khi edit/delete
                date_item.setData(Qt.UserRole, holiday["id"])

            # Cập nhật label tổng
            total_count = service.get_total_count()
            self.total_label.setText(f"Tổng: {total_count}")
            self.total_counter = total_count

            logging.info(f"WidgetsHoliday: Refreshed {len(holidays)} holidays")
        except Exception as e:
            logging.error(f"WidgetsHoliday: Error in _refresh_holidays: {e}")
