<?php
define("BASE_PATH", realpath(__DIR__ . "/../"));

// Kết nối với cơ sở dữ liệu
include(BASE_PATH . "/conect.php");

// Biến URL để dùng cho JS/CSS:
$base_url = '/myapp';
include(BASE_PATH . "/menu/menu1.php");
include(BASE_PATH . "/menu/menu2.php");
?>
<link rel="stylesheet" href="<?php echo $base_url; ?>/data/css/menu1.css">
<script src="<?php echo $base_url; ?>/data/js/menu1.js"></script>
<link rel="stylesheet" href="<?php echo $base_url; ?>/data/css/menu2.css">
<script src="<?php echo $base_url; ?>/data/js/menu2.js"></script>

<title>Đăng nhập/Đăng ký</title>