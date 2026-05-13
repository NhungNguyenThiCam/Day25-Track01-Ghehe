---
artifact: 1 — Lớp giao diện
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp giao diện

**Tình huống xử lý**: T-__  
Xem `../../1-map-and-format.md` Phần A.

---

## 1. Giải pháp là gì?

[Viết 2-3 câu. Nói rõ màn hình sẽ thay đổi gì để giảm rủi ro.]

Ví dụ:

> Khi AI trả lời về hạn nộp học bổng, giao diện hiện nhãn “Đã kiểm tra từ nguồn chính thức” hoặc “Chưa có nguồn xác minh”. Nếu thiếu nguồn, màn hình hiện nút chuyển cho tư vấn viên.

---

## 2. Vì sao sửa ở lớp giao diện?

[Chọn 1-2 ý đúng với giải pháp của nhóm.]

- Người dùng dễ tin câu trả lời của AI quá mức.
- Rủi ro xảy ra ở khoảnh khắc người dùng đọc câu trả lời.
- Giao diện cần làm rõ: thông tin nào đã kiểm tra, thông tin nào chưa chắc.
- Nếu prompt hoặc dữ liệu vẫn sót lỗi, giao diện là lớp chặn cuối.

**Hành động phòng vệ chính**:

- [ ] Thông báo rõ giới hạn
- [ ] Phát hiện dấu hiệu thiếu nguồn
- [ ] Chuyển người thật khi cần
- [ ] Giúp người dùng kiểm tra lại nguồn

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

**Định dạng demo**:

- [ ] Phác thảo màn hình
- [ ] Luồng màn hình
- [ ] Bản HTML đơn giản
- [ ] Ảnh hoặc link prototype

**Thành phần cần có trong demo**:

- Trạng thái có nguồn xác minh
- Trạng thái chưa có nguồn xác minh
- Cách người dùng chuyển sang người thật
- Câu chữ cảnh báo ngắn, dễ hiểu

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

[Ví dụ: màn hình rối hơn, người dùng thấy bị làm phiền, thao tác chậm hơn.]

**Nhóm giảm vấn đề đó bằng cách nào?**

[Ví dụ: chỉ hiện cảnh báo khi câu trả lời có rủi ro cao; dùng nhãn ngắn; đưa chi tiết vào nút mở rộng.]

---

## 5. Checklist trước khi nộp

- [ ] Giải pháp gắn đúng với một rủi ro chính.
- [ ] Demo nhìn vào là hiểu vấn đề được chặn ở đâu.
- [ ] Có đủ trạng thái bình thường và trạng thái lỗi.
- [ ] Có cách chuyển sang người thật khi AI không nên tự xử lý.
- [ ] Câu chữ trong giao diện ngắn, không đổ hết trách nhiệm cho người dùng.

**Người phụ trách**: [Tên thành viên]
