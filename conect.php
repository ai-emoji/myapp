<?php
// File kết nối cơ sở dữ liệu
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "myapp";

try {
    // Tạo kết nối PDO
    $pdo = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Thông báo kết nối thành công
    echo "Kết nối cơ sở dữ liệu thành công";
    
} catch(PDOException $e) {
    die("Lỗi kết nối: " . $e->getMessage());
}

// Hoặc sử dụng MySQLi (tuỳ chọn thay thế)
/*
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Kết nối thất bại: " . $conn->connect_error);
}
echo "Kết nối thành công";
*/
?>