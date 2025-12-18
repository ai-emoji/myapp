# controllers_widgets_declare_work_shift.py
# Controller cho widget khai báo ca làm việc

import traceback
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


from services.declare_work_shift_services import DeclareWorkShiftService


class ControllerWidgetsDeclareWorkShift:
    """Controller xử lý sự kiện cho widget khai báo ca làm việc"""

    def __init__(self, widget):
        self.widget = widget
        self.service = DeclareWorkShiftService()
        self.current_id = None  # Lưu ID của ca làm việc đang chọn

        # Kết nối các sự kiện
        self._connect_events()

        # Tải dữ liệu ban đầu
        self.refresh_data()

    def _connect_events(self):
        """Kết nối các sự kiện cho widget"""
        log_to_debug("ControllerWidgetsDeclareWorkShift: Connecting events")

        # Kiểm tra các nút có tồn tại không
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: btn_add exists: {hasattr(self.widget, 'btn_add')}"
        )
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: btn_save exists: {hasattr(self.widget, 'btn_save')}"
        )
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: btn_delete exists: {hasattr(self.widget, 'btn_delete')}"
        )

        # Kết nối sự kiện nút bấm
        self.widget.btn_add.clicked.connect(self.on_add_clicked)
        self.widget.btn_save.clicked.connect(self.on_save_clicked)
        self.widget.btn_delete.clicked.connect(self.on_delete_clicked)

        log_to_debug("ControllerWidgetsDeclareWorkShift: All button events connected")

        # Kết nối sự kiện click vào row trong bảng
        self.widget.table.cellClicked.connect(self.on_table_row_clicked)

    def on_add_clicked(self):
        """Xử lý sự kiện nhấn nút Thêm mới"""
        log_to_debug("ControllerWidgetsDeclareWorkShift: on_add_clicked() STARTED")

        # Reset form và current_id
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: Before reset - current_id={self.current_id}"
        )
        self.current_id = None
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: After reset - current_id={self.current_id}"
        )

        # Bỏ chọn row trong bảng để tránh click nhầm
        self.widget.table.clearSelection()

        self._clear_form()
        log_to_debug("ControllerWidgetsDeclareWorkShift: Form cleared")

        # Focus vào ô mã ca để người dùng có thể nhập ngay
        self.widget.input_shift_code.setFocus()
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: input_shift_code isReadOnly={self.widget.input_shift_code.isReadOnly()}, isEnabled={self.widget.input_shift_code.isEnabled()}"
        )
        log_to_debug(
            "ControllerWidgetsDeclareWorkShift: on_add_clicked() FINISHED - Ready for new entry"
        )

    def on_save_clicked(self):
        """Xử lý sự kiện nhấn nút Lưu"""
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: on_save_clicked() - current_id={self.current_id}"
        )

        # Lấy dữ liệu từ form
        shift_code = self.widget.input_shift_code.text().strip()
        start_time = self.widget.input_start_time.text().strip()
        end_time = self.widget.input_end_time.text().strip()
        lunch_start = self.widget.input_lunch_start.text().strip()
        lunch_end = self.widget.input_lunch_end.text().strip()
        total_minutes = self.widget.input_total_minutes.text().strip()
        work_day_count = self.widget.input_work_day_count.text().strip()

        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: Form data - shift_code='{shift_code}', start={start_time}, end={end_time}, total_minutes='{total_minutes}', work_day_count='{work_day_count}'"
        )

        # Validate dữ liệu
        if not shift_code:
            log_to_debug(
                "ControllerWidgetsDeclareWorkShift: Validation failed - shift_code is empty"
            )
            QMessageBox.warning(
                self.widget, "Cảnh báo", "Vui lòng nhập mã ca làm việc!"
            )
            return

        # Validate format giờ (HH:mm)
        import re

        time_pattern = re.compile(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
        if not time_pattern.match(start_time):
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Invalid start_time format: {start_time}"
            )
            QMessageBox.warning(
                self.widget, "Cảnh báo", "Giờ vào làm việc không đúng định dạng HH:mm!"
            )
            return
        if not time_pattern.match(end_time):
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Invalid end_time format: {end_time}"
            )
            QMessageBox.warning(
                self.widget,
                "Cảnh báo",
                "Giờ kết thúc làm việc không đúng định dạng HH:mm!",
            )
            return
        if lunch_start and not time_pattern.match(lunch_start):
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Invalid lunch_start format: {lunch_start}"
            )
            QMessageBox.warning(
                self.widget,
                "Cảnh báo",
                "Giờ bắt đầu ăn trưa không đúng định dạng HH:mm!",
            )
            return
        if lunch_end and not time_pattern.match(lunch_end):
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Invalid lunch_end format: {lunch_end}"
            )
            QMessageBox.warning(
                self.widget,
                "Cảnh báo",
                "Giờ kết thúc ăn trưa không đúng định dạng HH:mm!",
            )
            return

        # Chuyển sang format HH:mm:ss cho database
        start_time = start_time + ":00"
        end_time = end_time + ":00"
        lunch_start = lunch_start + ":00" if lunch_start else "12:00:00"
        lunch_end = lunch_end + ":00" if lunch_end else "13:00:00"

        # Chuyển đổi kiểu dữ liệu
        try:
            total_minutes = int(total_minutes) if total_minutes else 0
            work_day_count = float(work_day_count) if work_day_count else 0.0
        except ValueError:
            QMessageBox.warning(
                self.widget, "Cảnh báo", "Tổng giờ và đếm công phải là số hợp lệ!"
            )
            return

        # Kiểm tra thêm mới hay cập nhật
        if self.current_id is None:
            # Thêm mới
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Adding new work shift - {shift_code}"
            )
            result = self.service.add_work_shift(
                shift_code,
                start_time,
                end_time,
                lunch_start,
                lunch_end,
                total_minutes,
                work_day_count,
            )
            if result:
                QMessageBox.information(
                    self.widget, "Thành công", "Thêm ca làm việc thành công!"
                )
                self.refresh_data()
                self._clear_form()
            else:
                QMessageBox.critical(self.widget, "Lỗi", "Không thể thêm ca làm việc!")
        else:
            # Cập nhật
            log_to_debug(
                f"ControllerWidgetsDeclareWorkShift: Updating work shift - id={self.current_id}"
            )
            result = self.service.update_work_shift(
                self.current_id,
                shift_code,
                start_time,
                end_time,
                lunch_start,
                lunch_end,
                total_minutes,
                work_day_count,
            )
            if result:
                QMessageBox.information(
                    self.widget, "Thành công", "Cập nhật ca làm việc thành công!"
                )
                self.refresh_data()
            else:
                QMessageBox.critical(
                    self.widget, "Lỗi", "Không thể cập nhật ca làm việc!"
                )

    def on_delete_clicked(self):
        """Xử lý sự kiện nhấn nút Xóa"""
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: on_delete_clicked() - current_id={self.current_id}"
        )

        if self.current_id is None:
            QMessageBox.warning(
                self.widget, "Cảnh báo", "Vui lòng chọn ca làm việc cần xóa!"
            )
            return

        # Xác nhận xóa
        reply = QMessageBox.question(
            self.widget,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa ca làm việc này?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.service.delete_work_shift(self.current_id)
            if result:
                QMessageBox.information(
                    self.widget, "Thành công", "Xóa ca làm việc thành công!"
                )
                self.refresh_data()
                self._clear_form()
                self.current_id = None
            else:
                QMessageBox.critical(self.widget, "Lỗi", "Không thể xóa ca làm việc!")

    def on_table_row_clicked(self, row, column):
        """Xử lý sự kiện click vào row trong bảng"""
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: on_table_row_clicked() - row={row}"
        )

        # Lấy ID từ row data (lưu trong item column 0)
        id_item = self.widget.table.item(row, 0)
        if id_item is None:
            return

        # Lấy ID từ userData của item
        work_shift_id = id_item.data(100)  # Role 100 để lưu ID
        if work_shift_id is None:
            return

        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: Loading work shift id={work_shift_id}"
        )

        # Lấy thông tin đầy đủ từ service
        work_shift = self.service.get_work_shift_by_id(work_shift_id)
        if work_shift is None:
            QMessageBox.warning(
                self.widget, "Lỗi", "Không tìm thấy thông tin ca làm việc!"
            )
            return

        # Cập nhật current_id
        self.current_id = work_shift_id

        # Điền dữ liệu vào form
        self._fill_form(work_shift)

    def refresh_data(self):
        """Tải lại dữ liệu từ database và hiển thị vào bảng"""
        log_to_debug("ControllerWidgetsDeclareWorkShift: refresh_data()")

        # Lấy tất cả ca làm việc
        work_shifts = self.service.get_all_work_shifts()
        log_to_debug(
            f"ControllerWidgetsDeclareWorkShift: Loaded {len(work_shifts)} work shifts"
        )

        # Xóa dữ liệu cũ trong bảng
        self.widget.table.setRowCount(0)

        # Điền dữ liệu mới vào bảng
        for idx, shift in enumerate(work_shifts):
            self.widget.table.insertRow(idx)

            # Cột 0: Mã ca
            item_code = QTableWidgetItem(shift["shift_code"])
            item_code.setData(100, shift["id"])  # Lưu ID vào userData
            item_code.setTextAlignment(Qt.AlignCenter)
            self.widget.table.setItem(idx, 0, item_code)

            # Cột 1: Giờ vào
            start_time = shift["start_time"]
            if hasattr(start_time, "strftime"):
                start_time = start_time.strftime("%H:%M")  # datetime.time -> HH:mm
            elif isinstance(start_time, str):
                start_time = start_time[:5]  # Lấy HH:mm
            item_start = QTableWidgetItem(str(start_time))
            item_start.setTextAlignment(Qt.AlignCenter)
            self.widget.table.setItem(idx, 1, item_start)

            # Cột 2: Giờ ra
            end_time = shift["end_time"]
            if hasattr(end_time, "strftime"):
                end_time = end_time.strftime("%H:%M")  # datetime.time -> HH:mm
            elif isinstance(end_time, str):
                end_time = end_time[:5]  # Lấy HH:mm
            item_end = QTableWidgetItem(str(end_time))
            item_end.setTextAlignment(Qt.AlignCenter)
            self.widget.table.setItem(idx, 2, item_end)

    def _fill_form(self, work_shift):
        """Điền dữ liệu vào form"""
        log_to_debug(f"ControllerWidgetsDeclareWorkShift: _fill_form() - {work_shift}")

        # Mã ca
        self.widget.input_shift_code.setText(work_shift["shift_code"])

        # Giờ vào - chuyển về format HH:mm
        start_time = work_shift["start_time"]
        if hasattr(start_time, "strftime"):
            start_time = start_time.strftime("%H:%M")
        elif isinstance(start_time, str):
            start_time = start_time[:5]  # Lấy HH:mm
        else:
            start_time = "08:00"
        self.widget.input_start_time.setText(start_time)

        # Giờ ra
        end_time = work_shift["end_time"]
        if hasattr(end_time, "strftime"):
            end_time = end_time.strftime("%H:%M")
        elif isinstance(end_time, str):
            end_time = end_time[:5]
        else:
            end_time = "17:00"
        self.widget.input_end_time.setText(end_time)

        # Giờ bắt đầu ăn trưa
        lunch_start = work_shift["lunch_start"]
        if hasattr(lunch_start, "strftime"):
            lunch_start = lunch_start.strftime("%H:%M")
        elif isinstance(lunch_start, str):
            lunch_start = lunch_start[:5]
        else:
            lunch_start = "12:00"
        self.widget.input_lunch_start.setText(lunch_start)

        # Giờ kết thúc ăn trưa
        lunch_end = work_shift["lunch_end"]
        if hasattr(lunch_end, "strftime"):
            lunch_end = lunch_end.strftime("%H:%M")
        elif isinstance(lunch_end, str):
            lunch_end = lunch_end[:5]
        else:
            lunch_end = "13:00"
        self.widget.input_lunch_end.setText(lunch_end)

        # Tổng giờ (phút)
        self.widget.input_total_minutes.setText(str(work_shift["total_minutes"]))

        # Đếm công
        self.widget.input_work_day_count.setText(str(work_shift["work_day_count"]))

    def _clear_form(self):
        """Xóa dữ liệu trong form"""
        log_to_debug("ControllerWidgetsDeclareWorkShift: _clear_form()")

        self.widget.input_shift_code.clear()
        self.widget.input_start_time.setText("08:00")
        self.widget.input_end_time.setText("17:00")
        self.widget.input_lunch_start.setText("12:00")
        self.widget.input_lunch_end.setText("13:00")
        self.widget.input_total_minutes.clear()
        self.widget.input_work_day_count.clear()
