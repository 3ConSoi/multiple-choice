# 📝 HỆ THỐNG THI TRẮC NGHIỆM TRỰC TUYẾN (QUIZ ONLINE)

## 1. Giới thiệu
Hệ thống Quiz Online là một ứng dụng web cho phép người dùng tham gia làm bài thi trắc nghiệm trực tuyến.
Hệ thống hỗ trợ lấy câu hỏi ngẫu nhiên từ cơ sở dữ liệu, giới hạn thời gian làm bài và có khả năng mở rộng thêm nhiều chức năng trong tương lai.

Dự án được xây dựng theo mô hình Backend – Frontend tách biệt, sử dụng FastAPI cho backend và giao diện web cho frontend.

---

## 2. Công nghệ sử dụng

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn

### Frontend
- HTML / CSS
- JavaScript
- ReactJS

### Công cụ
- VS Code
- pgAdmin 4
- Git & GitHub

---

## 3. Kiến trúc hệ thống
Hệ thống được xây dựng theo mô hình Client – Server.

- Frontend: hiển thị giao diện và gửi request
- Backend: xử lý logic và API
- Database: lưu trữ câu hỏi và đáp án

---

## 4. Cấu trúc thư mục

app/
├── core/
├── routes/
│   ├── api_routes.py
│   ├── crud.py
│   └── quiz_route.py
├── templates/
│   └── index.html
├── database.py
├── main.py
├── models.py
├── schemas.py
├── session.py
├── seed_questions.sql
├── start.py
└── backend_requirements.txt

---

## 5. Chức năng chính
- Hiển thị bài thi trắc nghiệm
- Lấy câu hỏi ngẫu nhiên
- Đếm thời gian làm bài
- Dễ dàng mở rộng chức năng

---

## 6. Hướng dẫn chạy hệ thống

### Cài thư viện
pip install -r backend_requirements.txt

### Chạy backend
uvicorn main:app --reload

### Truy cập
http://127.0.0.1:8000

---

## 7. Định hướng phát triển
- Lưu kết quả người dùng
- Chấm điểm tự động
- Phân quyền người dùng
- Giao diện giống Google Form

---

## 8. Tác giả
- Nguyễn Minh Nhật
