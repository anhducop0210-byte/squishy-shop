# Squishy Store — Web Trưng Bày 32 Sản Phẩm Squishy

## 1. Link Web Đã Publish (GitHub Pages)
- **Trang Khách Hàng:** https://anhducop0210-byte.github.io/squishy-shop/
- **Trang Quản Trị Giá:** https://anhducop0210-byte.github.io/squishy-shop/admin.html *(Mã PIN mặc định: `0580`)*
- **Liên hệ / Zalo:** `0374860580` (`https://zalo.me/0374860580`)

## 2. Cấu Trúc Dự Án
```text
squishy-shop/
├── index.html          # Giao diện Khách hàng (xem sản phẩm, lọc, tìm kiếm, nhắn Zalo)
├── admin.html          # Giao diện Quản trị (đăng nhập PIN, nhập giá, đổi trạng thái, tải products.json)
├── data/
│   └── products.json   # Dữ liệu 32 sản phẩm, giá, danh mục, SĐT/Zalo, PIN quản trị
├── images/
│   └── product_01.jpg ... product_32.jpg  # 32 ảnh sản phẩm đã xóa sạch chữ gốc
├── server.py           # Backend Flask chạy local (lưu trực tiếp vào data/products.json & upload ảnh)
└── START_WEB.bat       # Nhấp đúp để mở web local trên Windows
```

## 3. Cách Chạy Local & Cập Nhật Giá Lên Web
1. Chạy `START_WEB.bat` (hoặc `python server.py`), mở `http://localhost:5000/admin` (PIN: `0580`).
2. Nhập giá cho 32 sản phẩm rồi bấm **Lưu thay đổi**.
3. Để đẩy giá mới lên link GitHub Pages công khai:
   ```bash
   git add data/products.json
   git commit -m "Update product prices"
   git push
   ```

---

## 4. PROMPT DÀNH CHO CLAUDE — YÊU CẦU THIẾT KẾ LẠI UI/UX & VISUAL DESIGN

> **Gửi Claude:** Hãy đọc toàn bộ repository này (`index.html`, `admin.html`, `data/products.json`, `images/product_01.jpg` → `product_32.jpg`) và **thiết kế lại hoàn toàn UI/UX và Visual Design** cho cả trang Khách Hàng (`index.html`) lẫn trang Quản Trị (`admin.html`) theo đúng các yêu cầu sau:

### Yêu cầu thiết kế (Bắt buộc)
1. **Chống lỗi font Tiếng Việt tuyệt đối:**
   - Sử dụng font hỗ trợ đầy đủ dấu Tiếng Việt 100% (ưu tiên `Be Vietnam Pro`, `Plus Jakarta Sans`, hoặc `Inter` kèm `subset=vietnamese`), kiểm tra kỹ các dấu nặng/hỏi/ngã/mũ ở cả chữ thường lẫn chữ hoa và các weight đậm (`600`, `700`, `800`).
2. **Phong cách thiết kế thật, tinh tế — KHÔNG "nhìn như AI tạo":**
   - Tuyệt đối **tránh** các màu gradient cầu vồng/hồng-tím sến, tránh nhồi nhét emoji (`🧸🔥✨💬`) vào tiêu đề hay nút bấm, tránh đổ bóng màu loè loẹt và bố cục rập khuôn kiểu landing page AI.
   - Hướng tới thẩm mỹ **boutique / lifestyle thương hiệu thật** (tham khảo Pop Mart, Miniso Japan, Muji, hoặc các shop đồ chơi/phụ kiện Hàn–Nhật trên Shopify):
     - Khoảng trắng (whitespace) hợp lý, lưới sản phẩm cân đối, ảnh sản phẩm là nhân vật chính.
     - Bảng màu tiết chế (nền sáng sạch, 1 màu chữ chính có độ tương phản cao, 1 màu nhấn tinh tế, màu xanh Zalo `#0068FF` chỉ dùng có chủ đích cho CTA Zalo).
     - Dùng icon SVG mảnh, đồng bộ (Lucide / Heroicons style) thay cho emoji.
     - Trải nghiệm mobile-first mượt mà (khách hàng chủ yếu mở link từ Zalo/Facebook trên điện thoại).
3. **Giữ nguyên 100% chức năng & phân quyền:**
   - **Trang Khách Hàng (`index.html`):**
     - Hiển thị đầy đủ 32 sản phẩm từ `data/products.json` (và tự ưu tiên `/api/products` nếu đang chạy local Flask).
     - Tìm kiếm nhanh, lọc theo 6 danh mục, sắp xếp theo giá/tên.
     - Modal xem chi tiết sản phẩm (ảnh lớn, tên, giá, ghi chú, nút đặt qua Zalo tự copy tên sản phẩm + mở `https://zalo.me/0374860580`, nút gọi `tel:0374860580`).
     - Không để lộ nút sửa giá hay tính năng quản trị ở trang khách.
   - **Trang Quản Trị (`admin.html`):**
     - Bắt buộc đăng nhập bằng mã PIN (mặc định `0580`, khớp với `data/products.json` và `/api/admin/login`).
     - Bảng nhập giá nhanh gọn, thân thiện cả trên desktop lẫn mobile, hỗ trợ lưu trực tiếp qua Flask API khi chạy local và lưu `localStorage` + tải file `products.json` khi chạy trên GitHub Pages.
4. **Thông tin liên hệ cố định:**
   - Số điện thoại & Zalo: **`0374860580`** (`https://zalo.me/0374860580`).
5. **Tương thích GitHub Pages:**
   - Giữ kiến trúc static thuần (HTML/CSS/JS) tại root (`index.html`, `admin.html`) sử dụng đường dẫn tương đối (`./data/products.json`, `./images/product_XX.jpg`) để sau khi `git push` là hoạt động ngay trên GitHub Pages mà không cần bước build phức tạp.
