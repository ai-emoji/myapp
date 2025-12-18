# Hướng dẫn cài đặt thư viện pyzk để kết nối máy chấm công

## Cài đặt thư viện pyzk

Thư viện pyzk được sử dụng để kết nối với máy chấm công ZKTeco và các dòng tương thích (bao gồm Ronald Jack X629ID).

### Cài đặt qua pip:

```bash
pip install pyzk
```

### Hoặc cài đặt từ source:

```bash
pip install git+https://github.com/fananimi/pyzk.git
```

## Thông tin máy chấm công Ronald Jack X629ID

- **Model**: Ronald Jack X629ID
- **Tương thích**: ZKTeco protocol
- **Cổng mặc định**: 4370
- **Giao thức**: TCP/IP

## Các tính năng hỗ trợ

1. Kết nối với thiết bị qua TCP/IP
2. Lấy thông tin thiết bị (tên, serial number, firmware version)
3. Quản lý người dùng
4. Tải dữ liệu chấm công
5. Xóa dữ liệu chấm công
6. Đồng bộ thời gian

## Ví dụ sử dụng cơ bản

```python
from zk import ZK

# Khởi tạo kết nối
zk = ZK('192.168.1.100', port=4370, timeout=5, password=0)

try:
    # Kết nối
    conn = zk.connect()
    
    # Lấy thông tin thiết bị
    print('Device Name:', conn.get_device_name())
    print('Serial Number:', conn.get_serialnumber())
    print('Firmware Version:', conn.get_firmware_version())
    
    # Lấy danh sách người dùng
    users = conn.get_users()
    print('Total Users:', len(users))
    
    # Lấy dữ liệu chấm công
    attendances = conn.get_attendance()
    print('Total Records:', len(attendances))
    
    # Ngắt kết nối
    conn.disconnect()
    
except Exception as e:
    print('Error:', e)
```

## Lưu ý

- Đảm bảo máy chấm công và máy tính cùng mạng LAN
- Kiểm tra firewall không chặn cổng 4370
- Một số máy yêu cầu mật mã, mặc định là 0
- Timeout nên đặt từ 5-10 giây tùy điều kiện mạng

## Tham khảo

- GitHub: https://github.com/fananimi/pyzk
- Documentation: https://pyzk.readthedocs.io/
