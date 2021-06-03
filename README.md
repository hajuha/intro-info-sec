## Bài tập môn Nhập môn An toàn thông tin

## Cài đặt
* ``` python -m venv .env ```
* ``` source .env/bin/active ```
* ``` pip install -r requirement.txt ```

## Chạy
#### RSA:
Câu lệnh: ```python rsa.py [bản rõ] [độ lớn]``` \
Ví dụ: \
```python rsa.py 131323245 512``` \
\\\ tạo hệ mật RSA 512 bit, với bản rõ là 131323245
## 1. Hệ mật RSA và chữ ký số
### Xây dựng hệ mật:
* Chọn 2 số nguyên tố lớn p và q với p ≠ q, lựa chọn ngẫu nhiên và độc lập.
* Tính N = pq.
* Tính Φ(N) = (p-1)(q-1).
* Chọn một số tự nhiên e sao cho 1 < e < Φ(N) và là số nguyên tố cùng nhau với Φ(N)
* Tính d sao cho de ≡ 1 (mod(Φ(N)))

* Khóa công khai: (e,N)
* Khóa bí mật: (d,N)

### Mã hóa
Bản rõ : x \
Bản mã c tính theo công thức: c = m ^ e mod n \
Giải mã c theo công thức: x = c ^ d mod n


