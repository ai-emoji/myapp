 $allowedPages

Cách đẩy (push) một file hoặc toàn bộ project lên Git
<!-- Tạo tên nếu chưa có -->
<!-- Tạo email nếu chưa có -->
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"

cd đường/dẫn/tới/project
git init
git add .
git commit -m "Thông điệp commit"
git remote add origin https://github.com/ai-emoji/myapp.git
git push -u origin master

Cách pull (kéo) code từ GitHub về máy tính (Git pull)
cd đường/dẫn/đến/thu_muc
git clone https://github.com/ai-emoji/myapp.git


Thiết lập kiểm tra git
git --version                                           # Kiểm tra phiên bản Git
git config --global user.name "Tên bạn"                 # Thiết lập tên người dùng
git config --global user.email "email@example.com"      # Thiết lập email
git config --list                                       # Xem toàn bộ cấu hình Git

Khởi tạo hoặc kết nối Git Repository
git init                                                # Khởi tạo Git repo mới trong thư mục hiện tại
git clone <url>                                         # Tải một repo từ GitHub về
git remote add origin <url>                             # Kết nối repo local với repo GitHub
git remote -v                                           # Kiểm tra thông tin remote đã kết nối

Quy trình commit và push tiêu chuẩn hằng ngày
git pull                                                 # 🔁 Bước 1: Lấy code mới nhất từ GitHub
git add .                                                # 📥 Bước 2: Thêm tất cả thay đổi vào staging
git commit -m "Update"                                   # 📝 Bước 3: Ghi lại thay đổi vào Git
git push                                                 # ⬆️ Bước 4: Đẩy thay đổi lên GitHub

Gắn lại remote URL chính xác
git remote remove origin  # Chỉ nếu đã từng gắn sai
git remote add origin https://github.com/ai-emoji/myapp.git
git branch -M main



Nếu chỉ thay đổi các file đã từng được theo dõi
git commit -am "Update nhanh"   # 📝 Thêm + commit một bước (chỉ áp dụng cho file cũ)

Quản lý file và trạng thái
git status                       # Kiểm tra trạng thái các file
git add <file>                   # Thêm file riêng lẻ vào staging
git rm <file>                    # Xóa file đang theo dõi
git restore <file>               # Khôi phục file về trạng thái đã commit

Quản lý nhánh (branch)
git branch                       # Xem danh sách nhánh
git branch <ten-nhanh>           # Tạo nhánh mới
git checkout <ten-nhanh>         # Chuyển sang nhánh khác
git checkout -b <ten-nhanh>      # Tạo và chuyển sang nhánh mới
git merge <ten-nhanh>            # Gộp nhánh vào nhánh hiện tại 
git branch -d <ten-nhanh>        # Xóa nhánh cục bộ

Xem lịch sử & khác biệt
git log                          # Xem lịch sử commit
git log --oneline                # Xem lịch sử ngắn gọn
git diff                         # So sánh thay đổi chưa commit
git show                         # Xem chi tiết nội dung một commit

Các lệnh nâng cao (xử lý lỗi hoặc tạm thời)
git stash                        # Lưu tạm thay đổi chưa commit
git stash pop                    # Lấy lại phần đã stash
git reset --hard                 # Hủy toàn bộ thay đổi chưa commit
git reflog                       # Xem lịch sử các vị trí HEAD (phục hồi commit mất)
git cherry-pick <commit-id>      # Áp dụng một commit từ nhánh khác

Ghi chú thêm:
Sử dụng git push -u origin main lần đầu để thiết lập upstream cho nhánh main.

Nếu bị lỗi xác thực khi push: dùng Personal Access Token thay vì mật khẩu.