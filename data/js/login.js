document.addEventListener('DOMContentLoaded', function () {
  // Hiển thị form đăng nhập mặc định khi trang load
  const loginFormContent = document.getElementById('loginFormContent');
  if (loginFormContent) {
    loginFormContent.style.display = 'block';
  }

  const registerForm = document.querySelector('#registerFormContent form');
  if (registerForm) {
    // Thêm trường xác nhận mật khẩu nếu chưa có
    let confirmBox = registerForm.querySelector('.input-box.confirm-password');
    if (!confirmBox) {
      // Đổi chỉ số sang 3 vì đã thêm trường số điện thoại
      const passwordBox = registerForm.querySelectorAll('.input-box')[3];
      confirmBox = document.createElement('div');
      confirmBox.className = 'input-box confirm-password';
      confirmBox.innerHTML = '<input type="password" placeholder="Xác nhận mật khẩu" required>';
      passwordBox.after(confirmBox);
    }

    // Hàm kiểm tra và báo đỏ realtime
    function validateInput(input, condition, message) {
      if (!condition) {
        input.style.borderColor = 'red';
        input.setCustomValidity(message);
      } else {
        input.style.borderColor = ''; // Để trống để trở về màu mặc định (đen)
        input.setCustomValidity('');
      }
    }

    const username = registerForm.querySelector('input[name="username"]');
    const email = registerForm.querySelector('input[name="email"]');
    const phone = registerForm.querySelector('input[name="phone"]');
    const password = registerForm.querySelector('input[name="password"]');
    const confirmPassword = registerForm.querySelector('.confirm-password input');

    username.addEventListener('input', function () {
      // Không báo đỏ khi trống, chỉ báo đỏ khi có nội dung nhưng không hợp lệ (ở đây username chỉ cần không rỗng)
      if (username.value.trim() === '') {
        username.style.borderColor = 'white';
        username.setCustomValidity('');
      } else {
        validateInput(username, true, '');
      }
    });

    email.addEventListener('input', function () {
      if (email.value === '') {
        email.style.borderColor = 'white';
        email.setCustomValidity('');
      } else {
        validateInput(
          email,
          /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email.value),
          'Email không hợp lệ!'
        );
      }
    });

    phone.addEventListener('input', function () {
      if (phone.value === '') {
        phone.style.borderColor = 'white';
        phone.setCustomValidity('');
      } else {
        validateInput(
          phone,
          /^(0|\+84)[0-9]{9,10}$/.test(phone.value),
          'Số điện thoại không hợp lệ!'
        );
      }
    });

    password.addEventListener('input', function () {
      if (password.value === '') {
        password.style.borderColor = 'white';
        password.setCustomValidity('');
        // Ẩn báo đỏ cho xác nhận mật khẩu nếu trường mật khẩu trống
        confirmPassword.style.borderColor = 'white';
        confirmPassword.setCustomValidity('');
      } else {
        validateInput(
          password,
          password.value.length >= 6,
          'Mật khẩu phải có ít nhất 6 ký tự!'
        );
        // Kiểm tra lại xác nhận mật khẩu nếu đã nhập
        if (confirmPassword.value) {
          confirmPassword.dispatchEvent(new Event('input'));
        }
      }
    });

    confirmPassword.addEventListener('input', function () {
      if (confirmPassword.value === '' || password.value === '') {
        confirmPassword.style.borderColor = 'white';
        confirmPassword.setCustomValidity('');
      } else {
        validateInput(
          confirmPassword,
          password.value === confirmPassword.value,
          'Mật khẩu xác nhận không khớp!'
        );
      }
    });

    registerForm.addEventListener('submit', function (e) {
      // Kiểm tra các input
      const username = registerForm.querySelector('input[name="username"]');
      const email = registerForm.querySelector('input[name="email"]');
      const phone = registerForm.querySelector('input[name="phone"]');
      const password = registerForm.querySelector('input[name="password"]');
      const confirmPassword = registerForm.querySelector('.confirm-password input');
      let valid = true;
      let message = '';

      // Reset border màu mặc định
      [username, email, phone, password, confirmPassword].forEach(input => {
        input.style.borderColor = '';
      });

      if (!username.value.trim()) {
        valid = false;
        message = 'Vui lòng nhập tên đăng nhập!';
        username.style.borderColor = 'red';
        username.focus();
      } else if (!email.value.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)) {
        valid = false;
        message = 'Email không hợp lệ!';
        email.style.borderColor = 'red';
        email.focus();
      } else if (!phone.value.match(/^(0|\+84)[0-9]{9,10}$/)) {
        valid = false;
        message = 'Số điện thoại không hợp lệ!';
        phone.style.borderColor = 'red';
        phone.focus();
      } else if (password.value.length < 6) {
        valid = false;
        message = 'Mật khẩu phải có ít nhất 6 ký tự!';
        password.style.borderColor = 'red';
        password.focus();
      } else if (password.value !== confirmPassword.value) {
        valid = false;
        message = 'Mật khẩu xác nhận không khớp!';
        confirmPassword.style.borderColor = 'red';
        confirmPassword.focus();
      }

      if (!valid) {
        alert(message);
        e.preventDefault();
      }
    });

    // Thêm nút ẩn/hiện mật khẩu cho các trường mật khẩu
    const passwordInputs = registerForm.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
      // Tạo nút toggle
      const toggle = document.createElement('span');
      toggle.textContent = '👁️';
      toggle.style.cursor = 'pointer';
      toggle.style.position = 'absolute';
      toggle.style.right = '20px';
      toggle.style.top = '50%';
      toggle.style.transform = 'translateY(-50%)';
      toggle.style.userSelect = 'none';

      // Đặt toggle vào .input-box
      const box = input.parentElement;
      box.style.position = 'relative';
      box.appendChild(toggle);

      toggle.addEventListener('click', function() {
        input.type = input.type === 'password' ? 'text' : 'password';
        toggle.textContent = input.type === 'password' ? '👁️' : '🙈';
      });
    });
  }

  // Thêm cho form đăng nhập
  const loginForm = document.querySelector('#loginFormContent form');
  if (loginForm) {
    const passwordInput = loginForm.querySelector('input[type="password"]');
    if (passwordInput) {
      const toggle = document.createElement('span');
      toggle.textContent = '👁️';
      toggle.style.cursor = 'pointer';
      toggle.style.position = 'absolute';
      toggle.style.right = '20px';
      toggle.style.top = '50%';
      toggle.style.transform = 'translateY(-50%)';
      toggle.style.userSelect = 'none';

      const box = passwordInput.parentElement;
      box.style.position = 'relative';
      box.appendChild(toggle);

      toggle.addEventListener('click', function() {
        passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
        toggle.textContent = passwordInput.type === 'password' ? '👁️' : '🙈';
      });
    }
  }

  // Xử lý chuyển đổi giữa các form
  function showForm(formId) {
    // Ẩn tất cả form
    document.getElementById('loginFormContent').style.display = 'none';
    document.getElementById('registerFormContent').style.display = 'none';
    document.getElementById('forgotFormContent').style.display = 'none';
    
    // Hiển thị form được chọn
    document.getElementById(formId).style.display = 'block';
  }

  // Thêm event listeners cho các link chuyển đổi form
  document.addEventListener('click', function(e) {
    if (e.target.getAttribute('for') === 'registerForm') {
      e.preventDefault();
      showForm('registerFormContent');
    } else if (e.target.getAttribute('for') === 'loginForm') {
      e.preventDefault();
      showForm('loginFormContent');
    } else if (e.target.getAttribute('for') === 'forgotForm') {
      e.preventDefault();
      showForm('forgotFormContent');
    }
  });
});