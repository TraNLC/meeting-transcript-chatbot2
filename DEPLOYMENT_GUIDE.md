# Hướng dẫn Deploy "Real Web" (Chi phí 0đ)

Bạn muốn deploy web thật (public cho mọi người dùng) nhưng vẫn muốn né chi phí Server GPU đắt đỏ? Đây là giải pháp "Hybrid" tối ưu nhất:

## 🏗️ Kiến trúc Hybrid (Lai)
1.  **Web App (Nhẹ):** Deploy lên **Render** hoặc **Railway** (Miễn phí 24/7).
2.  **AI Worker (Nặng):** Vẫn dùng **Google Colab** (Khi nào cần xử lý mới bật).

---

## Phần 1: Deploy Web App (Flask) lên Render
Render là lựa chọn tốt nhất hiện tại vì nó miễn phí và dễ dùng hơn AWS rất nhiều.

### Bước 1: Chuẩn bị Code
1.  Đảm bảo file `requirements.txt` đã có `gunicorn` (đã kiểm tra: OK).
2.  Tạo file `Procfile` (không đuôi) ở thư mục gốc với nội dung:
    ```
    web: gunicorn run:app
    ```
3.  Đẩy code lên **GitHub** (chế độ Public hoặc Private đều được).

### Bước 2: Setup trên Render
1.  Đăng ký tài khoản tại [render.com](https://render.com).
2.  Chọn **New +** -> **Web Service**.
3.  Kết nối với GitHub repo của bạn.
4.  Điền thông tin:
    *   **Name:** `meeting-ai-app` (tùy ý)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn run:app`
    *   **Instance Type:** `Free`
5.  Bấm **Create Web Service**.

### Bước 3: Cấu hình Môi trường (Environment Variables)
Trên trang Dashboard của Render, vào mục **Environment** và thêm các biến giống file `.env` của bạn:
*   `GEMINI_API_KEY`: <Key của bạn>
*   `SECRET_KEY`: <Điền chuỗi ngẫu nhiên>

👉 **Kết quả:** Bạn sẽ có một đường link `https://meeting-ai-app.onrender.com` chạy 24/7, gửi cho ai cũng vào được!

---

## Phần 2: Kết nối AI (WhisperX)
Vì Web App trên Render rất yếu (không có GPU), nó không thể tự chạy WhisperX. Nó cần kết nối với "Bộ não" Colab.

### Cách vận hành:
1.  Khi bạn (Admin) muốn hệ thống hoạt động đầy đủ tính năng Audio:
    *   Mở **Google Colab**.
    *   Chạy **Run All**.
    *   Copy URL ngrok mới.
2.  Vào web thật (`https://meeting-ai-app.onrender.com`), vào menu **Settings** (hoặc trang Upload) dán URL ngrok vào.
3.  Lúc này khách hàng truy cập web sẽ được dùng tính năng AI xịn sò (xử lý dưới nền bởi Colab của bạn).

---

## ❓ Tại sao không dùng AWS Free Tier?
AWS EC2 Free Tier (`t2.micro` hoặc `t3.micro`) chỉ có **1GB RAM** và **1 vCPU**.
*   Nó chạy Web Flask thì được (nhưng setup cực hơn Render nhiều: phải cài Linux, Nginx, SSL, Docker...).
*   Nó **TUYỆT ĐỐI KHÔNG** chạy nổi mô hình AI (WhisperX cần ít nhất 6-8GB VRAM GPU).
*   Nếu thuê Server có GPU trên AWS (ví dụ `g4dn.xlarge`), giá khoảng **$0.5/giờ** (~$360/tháng) => Quá đắt!

👉 **Chốt lại:** Hãy dùng **Render + Colab**. Đây là combo "Vô đối" cho startup ít vốn.
