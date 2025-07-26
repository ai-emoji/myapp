<?php
define("BASE_PATH", realpath(__DIR__ . "/../"));

// Kết nối với cơ sở dữ liệu
include(BASE_PATH . "/conect.php");

// Biến URL để dùng cho JS/CSS:
$base_url = '/myapp';
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập/Đăng ký</title>
    <link rel="stylesheet" href="<?php echo $base_url; ?>/data/css/menu2.css">
    <link rel="stylesheet" href="<?php echo $base_url; ?>/data/css/login.css">
</head>
<body>
<?php
// include(BASE_PATH . "/menu/menu1.php");
include(BASE_PATH . "/menu/menu2.php");
?>
<main>
  <div class="wrapper" id="loginFormContent">
    <form action="/myapp/login/login-register.php" method="post">
      <h1>Đăng nhập</h1>
      <div class="input-box">
        <input type="text" name="username" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Tên đăng nhập</label>
      </div>
      <div class="input-box">
        <input type="password" name="password" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Mật khẩu</label>
      </div>
      <div class="checkbox1">
        <label for="forgotForm">Quên mật khẩu?</label>
      </div>
      <button type="submit" class="btn">Đăng nhập</button>
      <div class="link">
        <p>Bạn chưa có tài khoản? <label for="registerForm">Đăng ký</label></p>
      </div>
    </form>
  </div>
  <div class="wrapper" id="registerFormContent">
    <form action="/myapp/login/login-register.php" method="post"> 
      <h1>Đăng ký</h1>
      <div class="input-box">
        <input type="text" name="username" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Tên đăng nhập</label>
      </div>
      <div class="input-box">
        <input type="email" name="email" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Email</label>
      </div>
      <div class="input-box">
        <input type="tel" name="phone" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Số điện thoại</label>
      </div>
      <div class="input-box">
        <input type="password" name="password" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Mật khẩu</label>
      </div>
      <div class="input-box confirm-password">
        <input type="password" name="confirm_password" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Xác nhận mật khẩu</label>
      </div>
      <div class="checkbox1">
        <label><input type="checkbox" required>Tôi đồng ý với điều khoản</label>
      </div>
      <button type="submit" class="btn">Đăng ký</button>
      <div class="link">
        <p>Đã có tài khoản? <label for="loginForm">Đăng nhập</label></p>
      </div>
    </form>
  </div>

  <div class="wrapper" id="forgotFormContent">
    <form action="/myapp/login/login-register.php" method="post">
      <h1>Khôi phục mật khẩu</h1>
      <div class="input-box">
        <input type="email" name="email" required autocomplete="off" placeholder=" " />
        <label class="floating-label">Email</label>
      </div>
      <button type="submit" class="btn">Gửi yêu cầu</button>
      <div class="link">
        <p>Bạn chưa có tài khoản? <label for="registerForm">Đăng ký</label></p>
      </div>
    </form>
  </div>
</main>

<!-- <script src="<?php echo $base_url; ?>/data/js/menu1.js"></script> -->
<script src="<?php echo $base_url; ?>/data/js/menu2.js"></script>
<script src="<?php echo $base_url; ?>/data/js/login.js"></script>
</body>
</html>