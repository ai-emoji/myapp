# controllers_widgets_download_attendence.py
# Controller cho widgets_download_attendence.py

import traceback
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, QThread, Signal
from datetime import datetime


def log_to_debug(message):
    try:
        with open("log/debug.log", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {message}\n")
    except Exception as e:
        print(f"[LogError] {e}")


class DownloadThread(QThread):
    """Thread để tải dữ liệu chấm công trong background"""
    progress = Signal(int, str)  # progress value, status message
    finished_signal = Signal(bool, str, int)  # success, message, count
    
    def __init__(self, device_id, from_date, to_date):
        super().__init__()
        self.device_id = device_id
        self.from_date = from_date
        self.to_date = to_date
    
    def run(self):
        try:
            from services.attendance_raw_services import AttendanceRawService
            
            # Emit progress
            self.progress.emit(0, "Đang chuẩn bị...")
            
            service = AttendanceRawService()
            
            # Tạo callback để cập nhật progress
            def progress_callback(progress_value, message):
                # progress_value từ 0-100 trực tiếp từ service
                self.progress.emit(progress_value, message)
            
            # Tải dữ liệu với callback
            success, message, count = service.download_from_device(
                self.device_id, 
                self.from_date, 
                self.to_date,
                progress_callback
            )
            
            # Complete
            self.progress.emit(100, "Hoàn tất!")
            self.finished_signal.emit(success, message, count)
            
        except Exception as e:
            log_to_debug(f"DownloadThread error: {e}\n{traceback.format_exc()}")
            self.finished_signal.emit(False, f"Lỗi: {str(e)}", 0)


class ControllerWidgetsDownloadAttendence:
    """Controller xử lý logic cho widgets_download_attendence.py"""

    def __init__(self, widget):
        self.widget = widget
        self._connect_signals()
        self._load_devices()
        self._load_attendance_data()

    def _connect_signals(self):
        """Kết nối signals với slots"""
        try:
            # Kết nối các nút chức năng
            self.widget.btn_download.clicked.connect(self._on_download_clicked)
            self.widget.btn_clear.clicked.connect(self._on_clear_clicked)
            
            # Kết nối thay đổi ngày hoặc thiết bị để reload data
            self.widget.date_from.dateChanged.connect(self._load_attendance_data)
            self.widget.date_to.dateChanged.connect(self._load_attendance_data)
            self.widget.combo_device.currentIndexChanged.connect(self._load_attendance_data)
            
            # Kết nối search box
            self.widget.txt_search.textChanged.connect(self._on_search_text_changed)

            log_to_debug("ControllerWidgetsDownloadAttendence: Signals connected")
        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDownloadAttendence: _connect_signals() error: {e}\n{traceback.format_exc()}"
            )

    def _load_devices(self):
        """Load danh sách thiết bị vào combo box"""
        try:
            log_to_debug("ControllerWidgetsDownloadAttendence: _load_devices() called")
            from services.device_services import DeviceService

            service = DeviceService()
            devices = service.get_all_devices()

            # Clear combo box
            self.widget.combo_device.clear()

            # Thêm tùy chọn "Tất cả thiết bị"
            self.widget.combo_device.addItem("Tất cả thiết bị", None)

            # Thêm các thiết bị
            for device in devices:
                display_text = f"{device['device_number']} - {device['device_name']} ({device['ip_address']})"
                self.widget.combo_device.addItem(display_text, device['id'])

            log_to_debug(f"ControllerWidgetsDownloadAttendence: Loaded {len(devices)} devices")

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDownloadAttendence: _load_devices() error: {e}\n{traceback.format_exc()}"
            )

    def _load_attendance_data(self):
        """Load dữ liệu chấm công từ database và hiển thị lên bảng"""
        try:
            log_to_debug("ControllerWidgetsDownloadAttendence: _load_attendance_data() called")
            from services.attendance_raw_services import AttendanceRawService
            from collections import defaultdict

            service = AttendanceRawService()

            # Lấy thông tin filter
            from_date = self.widget.date_from.date().toPython()
            to_date = self.widget.date_to.date().toPython()
            device_id = self.widget.combo_device.currentData()

            # Load dữ liệu
            records = service.get_all_records(from_date, to_date, device_id)

            # Log để debug
            log_to_debug(f"Filter: from_date={from_date}, to_date={to_date}, device_id={device_id}")
            log_to_debug(f"Total records loaded: {len(records)}")
            
            if len(records) > 0:
                log_to_debug(f"Sample record: {records[0]}")
            
            # Nhóm dữ liệu theo user_id và ngày, lưu tất cả các bản ghi
            grouped_data = defaultdict(lambda: {
                "user_name": "",
                "date": "",
                "records": [],  # Lưu tất cả records để ghép cặp
                "punch": "",
                "uid": ""
            })
            
            for record in records:
                timestamp = record["timestamp"]
                if isinstance(timestamp, str):
                    from datetime import datetime
                    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                
                user_id = str(record["user_id"])
                date_str = timestamp.strftime("%d/%m/%Y")
                time_str = timestamp.strftime("%H:%M")
                status = record.get("status", 0)
                
                key = f"{user_id}_{date_str}"
                
                # Lưu thông tin cơ bản
                grouped_data[key]["user_name"] = record.get("user_name", "")
                grouped_data[key]["date"] = date_str
                grouped_data[key]["punch"] = self._get_punch_text(record.get("punch", 0))
                grouped_data[key]["uid"] = str(record.get("uid", ""))
                
                # Lưu tất cả bản ghi với timestamp, time_str và status
                grouped_data[key]["records"].append({
                    "timestamp": timestamp,
                    "time_str": time_str,
                    "status": status,
                    "record_id": record.get("id")
                })

            # Clear bảng
            self.widget.table.setSortingEnabled(False)  # Tắt sorting khi load data
            self.widget.table.setRowCount(0)

            # Thêm dữ liệu vào bảng
            for key in sorted(grouped_data.keys()):
                data = grouped_data[key]
                user_id = key.split("_")[0]
                
                # Sắp xếp tất cả records theo thời gian
                sorted_records = sorted(data["records"], key=lambda x: x["timestamp"])
                
                # Tách riêng giờ vào và giờ ra THEO THỜI GIAN (không dùng status vì máy không phân biệt)
                in_times = []  # [(time_str, record_id)] - Giờ sáng (< 12:00)
                out_times = []  # [(time_str, record_id)] - Giờ chiều (>= 12:00)
                
                for rec in sorted_records:
                    # Phân loại theo thời gian: sáng = vào, chiều/tối = ra
                    hour = rec["timestamp"].hour
                    if hour < 12:  # Sáng (00:00 - 11:59) = Giờ vào
                        in_times.append((rec["time_str"], rec["record_id"]))
                    else:  # Chiều/Tối (12:00 - 23:59) = Giờ ra
                        out_times.append((rec["time_str"], rec["record_id"]))
                
                # Lấy tối đa 3 giờ vào và 3 giờ ra (mới nhất)
                in_times = in_times[-3:] if len(in_times) > 3 else in_times
                out_times = out_times[-3:] if len(out_times) > 3 else out_times
                
                # Debug log
                log_to_debug(f"User {user_id} on {data['date']}: in_times={len(in_times)}, out_times={len(out_times)}")
                
                # Tạo pairs để hiển thị (không cần ghép chặt chẽ)
                pairs = []
                max_len = max(len(in_times), len(out_times))
                all_record_ids = []
                
                for i in range(max_len):
                    in_time = in_times[i][0] if i < len(in_times) else ""
                    in_id = in_times[i][1] if i < len(in_times) else None
                    out_time = out_times[i][0] if i < len(out_times) else ""
                    out_id = out_times[i][1] if i < len(out_times) else None
                    
                    pairs.append((in_time, out_time))
                    if in_id:
                        all_record_ids.append(in_id)
                    if out_id:
                        all_record_ids.append(out_id)
                
                row = self.widget.table.rowCount()
                self.widget.table.insertRow(row)

                # Cột 0: Mã NV (format 5 số)
                formatted_user_id = user_id.zfill(5)  # Thêm số 0 đằng trước để đủ 5 số
                item = QTableWidgetItem(formatted_user_id)
                self.widget.table.setItem(row, 0, item)

                # Cột 1: Tên NV
                item = QTableWidgetItem(data["user_name"])
                self.widget.table.setItem(row, 1, item)

                # Cột 2: Ngày
                item = QTableWidgetItem(data["date"])
                self.widget.table.setItem(row, 2, item)

                # Cặp 1: Giờ vào 1, Giờ ra 1
                item = QTableWidgetItem(pairs[0][0] if len(pairs) > 0 else "")
                self.widget.table.setItem(row, 3, item)
                
                item = QTableWidgetItem(pairs[0][1] if len(pairs) > 0 else "")
                self.widget.table.setItem(row, 4, item)

                # Cặp 2: Giờ vào 2, Giờ ra 2
                item = QTableWidgetItem(pairs[1][0] if len(pairs) > 1 else "")
                self.widget.table.setItem(row, 5, item)
                
                item = QTableWidgetItem(pairs[1][1] if len(pairs) > 1 else "")
                self.widget.table.setItem(row, 6, item)

                # Cặp 3: Giờ vào 3, Giờ ra 3
                item = QTableWidgetItem(pairs[2][0] if len(pairs) > 2 else "")
                self.widget.table.setItem(row, 7, item)
                
                item = QTableWidgetItem(pairs[2][1] if len(pairs) > 2 else "")
                self.widget.table.setItem(row, 8, item)

                # Cột 9: Vân tay
                item = QTableWidgetItem(data["punch"])
                self.widget.table.setItem(row, 9, item)

                # Cột 10: Mã chấm công (UID)
                item = QTableWidgetItem(data["uid"])
                self.widget.table.setItem(row, 10, item)
                
                # Lưu record_ids vào row để xóa sau này
                if len(all_record_ids) > 0:
                    first_item = self.widget.table.item(row, 0)
                    if first_item:
                        first_item.setData(Qt.UserRole, all_record_ids)
                        log_to_debug(f"Saved {len(all_record_ids)} record_ids to row {row}")

            log_to_debug(f"ControllerWidgetsDownloadAttendence: Loaded {len(grouped_data)} grouped records")
            
            # Bật lại sorting sau khi load xong
            self.widget.table.setSortingEnabled(True)

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDownloadAttendence: _load_attendance_data() error: {e}\n{traceback.format_exc()}"
            )

    def _on_search_text_changed(self, text):
        """Xử lý khi text search thay đổi - Tìm theo mã NV, tên NV, và ngày"""
        try:
            search_text = text.strip()
            
            # Nếu search text là số, format thành 5 số để tìm mã NV
            search_formatted = search_text.zfill(5) if search_text.isdigit() else search_text
            
            # Chuyển thành lowercase để so sánh không phân biệt hoa thường
            search_lower = search_formatted.lower()
            
            # Duyệt qua tất cả các rows và ẩn/hiện theo search
            visible_count = 0
            for row in range(self.widget.table.rowCount()):
                # Lấy mã NV, tên NV, và ngày
                ma_nv_item = self.widget.table.item(row, 0)
                ten_nv_item = self.widget.table.item(row, 1)
                ngay_item = self.widget.table.item(row, 2)
                
                ma_nv = ma_nv_item.text().lower() if ma_nv_item else ""
                ten_nv = ten_nv_item.text().lower() if ten_nv_item else ""
                ngay = ngay_item.text().lower() if ngay_item else ""
                
                # Hiện row nếu match với search text (tìm trong mã NV, tên NV, hoặc ngày)
                if search_text == "" or search_lower in ma_nv or search_lower in ten_nv or search_lower in ngay:
                    self.widget.table.setRowHidden(row, False)
                    visible_count += 1
                else:
                    self.widget.table.setRowHidden(row, True)
            
            log_to_debug(f"Search '{search_text}': {visible_count} rows visible (mã NV/tên NV/ngày)")
                    
        except Exception as e:
            log_to_debug(f"_on_search_text_changed error: {e}")

    def _get_status_text(self, status):
        """Chuyển đổi status code thành text"""
        status_map = {
            0: "Vào",
            1: "Ra",
            2: "Nghỉ ra",
            3: "Nghỉ vào",
            4: "Tăng ca vào",
            5: "Tăng ca ra",
        }
        return status_map.get(status, f"Khác ({status})")

    def _get_punch_text(self, punch):
        """Chuyển đổi punch code thành text"""
        punch_map = {
            0: "Vân tay",
            1: "Mật khẩu",
            2: "Thẻ",
            3: "Khuôn mặt",
            4: "Iris",
            15: "Khác",
        }
        return punch_map.get(punch, f"Khác ({punch})")

    def _on_download_clicked(self):
        """Xử lý khi click nút Tải dữ liệu"""
        try:
            log_to_debug("ControllerWidgetsDownloadAttendence: Download button clicked")

            # Kiểm tra đã chọn thiết bị chưa
            device_id = self.widget.combo_device.currentData()
            if device_id is None:
                QMessageBox.warning(
                    self.widget,
                    "Cảnh báo",
                    "Vui lòng chọn một thiết bị cụ thể để tải dữ liệu"
                )
                return

            # Lấy khoảng ngày
            from_date = self.widget.date_from.date().toPython()
            to_date = self.widget.date_to.date().toPython()

            # Disable button
            self.widget.btn_download.setEnabled(False)

            # Tạo progress dialog
            self.progress_dialog = QProgressDialog(
                "Đang chuẩn bị...", 
                "Hủy", 
                0, 
                100, 
                self.widget
            )
            self.progress_dialog.setWindowTitle("Tải dữ liệu chấm công")
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setAutoReset(False)
            self.progress_dialog.canceled.connect(self._on_download_canceled)
            
            # Style cho progress dialog
            self.progress_dialog.setStyleSheet(
                """
                QProgressDialog {
                    min-width: 400px;
                    min-height: 120px;
                }
                QProgressBar {
                    border: 2px solid #d0d0d0;
                    border-radius: 5px;
                    text-align: center;
                    background: #f0f0f0;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #8BC34A);
                    border-radius: 3px;
                }
                QPushButton {
                    min-width: 80px;
                    padding: 5px 15px;
                }
                """
            )

            # Tạo và khởi động thread
            self.download_thread = DownloadThread(device_id, from_date, to_date)
            self.download_thread.progress.connect(self._on_download_progress)
            self.download_thread.finished_signal.connect(self._on_download_finished)
            self.download_thread.start()

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDownloadAttendence: _on_download_clicked() error: {e}\n{traceback.format_exc()}"
            )
            self.widget.btn_download.setEnabled(True)
            QMessageBox.critical(self.widget, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def _on_download_progress(self, value, message):
        """Cập nhật progress dialog"""
        try:
            if hasattr(self, 'progress_dialog') and self.progress_dialog:
                self.progress_dialog.setValue(value)
                self.progress_dialog.setLabelText(message)
        except Exception as e:
            log_to_debug(f"_on_download_progress error: {e}")

    def _on_download_finished(self, success, message, count):
        """Xử lý khi download hoàn tất"""
        try:
            # Đóng progress dialog
            if hasattr(self, 'progress_dialog') and self.progress_dialog:
                self.progress_dialog.close()
                self.progress_dialog = None

            # Enable button
            self.widget.btn_download.setEnabled(True)

            # Hiển thị kết quả
            if success:
                QMessageBox.information(self.widget, "Thành công", message)
                # Reload dữ liệu
                self._load_attendance_data()
            else:
                QMessageBox.warning(self.widget, "Lỗi", message)

        except Exception as e:
            log_to_debug(f"_on_download_finished error: {e}\n{traceback.format_exc()}")

    def _on_download_canceled(self):
        """Xử lý khi người dùng hủy download"""
        try:
            if hasattr(self, 'download_thread') and self.download_thread:
                self.download_thread.terminate()
                self.download_thread.wait()
            
            self.widget.btn_download.setEnabled(True)
            log_to_debug("Download canceled by user")
        except Exception as e:
            log_to_debug(f"_on_download_canceled error: {e}")

    def _on_clear_clicked(self):
        """Xử lý khi click nút Xóa dữ liệu"""
        try:
            log_to_debug("ControllerWidgetsDownloadAttendence: Clear button clicked")

            # Kiểm tra xem có row nào được chọn không
            selected_rows = self.widget.table.selectionModel().selectedRows()
            
            log_to_debug(f"Selected rows count: {len(selected_rows)}")
            
            if selected_rows and len(selected_rows) > 0:
                # Xóa các row được chọn
                reply = QMessageBox.question(
                    self.widget,
                    "Xác nhận xóa",
                    f"Bạn có chắc chắn muốn xóa {len(selected_rows)} bản ghi đã chọn?\n"
                    "Hành động này không thể hoàn tác!",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                
                if reply == QMessageBox.Yes:
                    from services.attendance_raw_services import AttendanceRawService
                    service = AttendanceRawService()
                    
                    deleted_count = 0
                    total_record_ids = 0
                    
                    for index in selected_rows:
                        row = index.row()
                        log_to_debug(f"Processing row {row}")
                        
                        # Lấy record_ids từ item
                        first_item = self.widget.table.item(row, 0)
                        if first_item:
                            record_ids = first_item.data(Qt.UserRole)
                            log_to_debug(f"Row {row} has record_ids: {record_ids}")
                            
                            if record_ids:
                                # Xóa từng record
                                for record_id in record_ids:
                                    if record_id:  # Kiểm tra record_id không None
                                        total_record_ids += 1
                                        if service.delete_record_by_id(record_id):
                                            deleted_count += 1
                                            log_to_debug(f"Deleted record_id: {record_id}")
                        else:
                            log_to_debug(f"Row {row} has no item at column 0")
                    
                    log_to_debug(f"Total record_ids: {total_record_ids}, Deleted: {deleted_count}")
                    
                    QMessageBox.information(
                        self.widget, 
                        "Thành công", 
                        f"Đã xóa {deleted_count} bản ghi chấm công (từ {len(selected_rows)} dòng được chọn)"
                    )
                    # Reload dữ liệu
                    self._load_attendance_data()
            else:
                # Không có row nào được chọn -> xóa toàn bộ
                reply = QMessageBox.question(
                    self.widget,
                    "Xác nhận xóa",
                    "Bạn có chắc chắn muốn xóa toàn bộ dữ liệu chấm công?\n"
                    "Hành động này không thể hoàn tác!",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

                if reply == QMessageBox.Yes:
                    from services.attendance_raw_services import AttendanceRawService

                    service = AttendanceRawService()
                    success, message = service.delete_all_records()

                    if success:
                        QMessageBox.information(self.widget, "Thành công", message)
                        # Reload dữ liệu
                        self._load_attendance_data()
                    else:
                        QMessageBox.warning(self.widget, "Lỗi", message)

        except Exception as e:
            log_to_debug(
                f"ControllerWidgetsDownloadAttendence: _on_clear_clicked() error: {e}\n{traceback.format_exc()}"
            )
            QMessageBox.critical(self.widget, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")


