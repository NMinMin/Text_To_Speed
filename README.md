Text-to-Speech API 🎙️
API chuyển đổi văn bản thành giọng nói (Text-to-Speech) đơn giản được xây dựng bằng Python và sẵn sàng để deploy lên Render.

🚀 Tính năng
Chuyển đổi văn bản thành tệp âm thanh nhanh chóng.

Thiết lập sẵn để deploy lên Render thông qua Procfile.

📁 Cấu trúc dự án
Plaintext
├── main.py          # File mã nguồn chính của ứng dụng
├── requirements.txt # Danh sách các thư viện Python phụ thuộc
└── Procfile         # Cấu hình khởi chạy cho Render
🛠️ Cài đặt và Chạy cục bộ (Local)
Clone repository:

Bash
git clone https://github.com/NMinMin/Text_To_Speed.git
cd Text_To_Speed
Cài đặt các thư viện phụ thuộc:

Bash
pip install -r requirements.txt
Chạy ứng dụng:

Bash
python main.py
☁️ Deploy lên Render
Tạo một Web Service mới trên Render.

Kết nối với repository GitHub này (NMinMin/Text_To_Speed).

Render sẽ tự động nhận diện Procfile và requirements.txt để tiến hành build và chạy ứng dụng.
