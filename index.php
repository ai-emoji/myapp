<?php
require_once 'conect.php';
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trang Chủ</title>
    <link rel="icon" href="./data/svg/logo.svg" type="image/svg+xml">
    <link rel="stylesheet" href="./data/css/index.css">
    <link rel="stylesheet" href="./data/css/menu1.css">
    <link rel="stylesheet" href="./data/css/menu2.css">
</head>
<?php include "menu/menu1.php"; ?>
<?php include "menu/menu2.php"; ?>
<body>
</body>
<script src="./data/js/index-force-reload.js"></script>
<script src="./data/js/index-buttonnext.js"></script>
<script src="./data/js/menu1.js"></script>
<script src="./data/js/menu2.js"></script>
<script src="./data/js/login.js"></script>
</html>