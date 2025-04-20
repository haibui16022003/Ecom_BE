## Các bước chạy BE:
### 1. Clone dự án về
### 2. Mở môi trường ảo:
Nhập câu lệnh sau vào terminal: \
`python -m venv venv`
#### Đối với Macs: 
`source venv/bin/activate`
#### Đối với Windows: 
`venv\Scripts\activate`

### 3. Cài đặt các thư viện phụ thuộc: 
`pip install -r requirements.txt`

### 4.Tạo file `.env`:

### 5. Setup để connect vào PostgreSQL

### 6. Chạy server: 
`uvicorn main:app --reload`

API sẽ được chạy tại: `http://127.0.0.1:8000`

Sử dụng Swagger UI để test và đọc API: `http://127.0.0.1:8000/docs`

