# Hướng dẫn sử dụng file upload nhân viên

## File mẫu: upload_nhanvien_mau.xlsx

File Excel này được sử dụng để upload hàng loạt nhân viên vào danh sách tải lên máy chấm công.

### Cấu trúc file:

**Cột bắt buộc:**
- `Mã nhân viên`: Mã nhân viên trong hệ thống (phải khớp với DB)

**Cột tùy chọn:**
- `Tên nhân viên`: Tên nhân viên (chỉ để tham khảo)
- `Ghi chú`: Ghi chú bổ sung

### Định dạng hỗ trợ:
- **Excel (*.xlsx, *.xls)** - Định dạng chính (khuyến nghị)
- CSV (*.csv) - UTF-8 encoding

### Tạo file mẫu Excel:
Chạy script để tạo file mẫu:
```bash
python create_upload_template.py
```
File `upload_nhanvien_mau.xlsx` sẽ được tạo với định dạng đẹp, header màu xanh đậm.

### Các tên cột hỗ trợ:
Hệ thống tự động nhận diện các tên cột sau cho "Mã nhân viên":
- `Mã nhân viên`
- `Ma nhan vien`
- `employee_code`
- `Employee Code`

### Cách sử dụng:

1. **Tạo file mẫu (nếu chưa có):**
   ```bash
   python create_upload_template.py
   ```

2. **Chuẩn bị file:**
   - Mở file `upload_nhanvien_mau.xlsx` bằng Excel
   - Chỉnh sửa danh sách mã nhân viên theo nhu cầu
   - Lưu file

3. **Upload vào hệ thống:**
   - Vào màn hình "Tải NV lên máy chấm công"
   - Click nút "📤 Upload danh sách"
   - Chọn file Excel đã chuẩn bị
   - Hệ thống sẽ tự động thêm nhân viên vào danh sách

4. **Kiểm tra kết quả:**
   - Hệ thống sẽ hiển thị số lượng nhân viên đã thêm thành công
   - Nếu có mã không tìm thấy trong DB, sẽ hiển thị cảnh báo

5. **Tải lên máy chấm công:**
   - Sau khi upload file, click "📤 Chọn máy & Tải lên"
   - Chọn thiết bị chấm công
   - Đợi quá trình tải lên hoàn tất

### Lưu ý:
- **Cần cài đặt thư viện openpyxl:**
  ```bash
  pip install openpyxl
  ```
- Mã nhân viên trong file phải tồn tại trong hệ thống
- Không được để trống cột "Mã nhân viên"
- Nếu nhân viên đã có trong danh sách tải lên, sẽ bỏ qua (không thêm trùng)
- File Excel có header được tô màu xanh đậm, dễ nhận biết

### Cấu trúc file Excel:

| Mã nhân viên | Tên nhân viên | Ghi chú |
|--------------|---------------|---------|
| 00001 | Nguyễn Văn A | Nhân viên phòng kế toán |
| 00002 | Trần Thị B | Nhân viên phòng kinh doanh |
| 00003 | Lê Văn C | Nhân viên phòng kỹ thuật |

### Tính năng file Excel mẫu:
- ✅ Header màu xanh đậm (#2C3E50), chữ trắng, in đậm
- ✅ Border cho tất cả các ô
- ✅ Căn giữa cột mã nhân viên
- ✅ Tự động điều chỉnh độ rộng cột
- ✅ Đóng băng dòng header khi cuộn
- ✅ 10 dòng dữ liệu mẫu
