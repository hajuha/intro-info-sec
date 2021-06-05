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
#### Elgamal:
Câu lệnh: ```python elgamal.py [bản rõ] [độ lớn]``` \
Ví dụ: \
```python elgamal.py 131323245 160``` \
\\\ tạo hệ mật Elgamal 512 bit, với bản rõ là 131323245
#### ECC:
Câu lệnh: ```python ECC.py [độ lớn]``` \
Ví dụ: \
```python ECC.py  16``` \
\\\ tạo hệ mật ECC 16 bit
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
## 2. Hệ mật Elgamal và chữ ký số
### Xây dựng hệ mật:
* Chọn số nguyên tố lớn *p*.
* Chọn *a* là một số thuộc Zp, *α* là một phần tử nguyên thuỷ của Zp
* Tính *β = α ^ a mod p*.

* Khóa công khai: *(p, α, β)*
* Khóa bí mật: *(a)*

### Mã hóa
Bản rõ : x \
Chọn số nguyên ngẫu nhiên k \
Bản mã là *(γ, δ)*, với: \
*γ = x * β ^ k mod p*\
*δ = a^k mod p* \
Giải mã *(γ, δ)* theo công thức: *x = δ * (γ ^ -a) mod p*

### Chữ ký số

Bản rõ : x \
Chọn số nguyên ngẫu nhiên *k* \
Chữ ký số là *(γ, δ)*, với: \
*γ = α ^ k mod p* \
*δ = (x - a * r) * (k ^ -1 mod (p - 1))* 

Xác thực chữ ký *(γ, δ)* đúng khi: *α^x ≡ (β ^ γ)\* (γ ^ δ) (mod p)*

## 2. Hệ mật ECC và chữ ký số
(tham khảo trong docs: https://docs.google.com/document/d/1xPNIYEinPOMsGlE0hadb-afh46sNx1JhdPFv3o83a1U/edit?usp=sharing)


