---
artifact: 3 — Lớp kiến trúc dữ liệu
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp kiến trúc dữ liệu

**Tình huống xử lý**: T-__  
Xem `../../1-map-and-format.md` Phần A.

---

## 1. Giải pháp là gì?

[Viết 2-3 câu. Nói rõ hệ thống cần thêm nguồn dữ liệu, bước kiểm tra, cách chuyển câu hỏi hoặc cách ghi lại lỗi nào.]

Ví dụ:

> Với câu hỏi về học bổng, hệ thống phải tra nguồn tuyển sinh chính thức trước khi AI trả lời. Nếu nguồn không có dữ liệu hoặc bị lỗi, AI không được đoán mà chuyển câu hỏi cho tư vấn viên.

---

## 2. Vì sao sửa ở lớp kiến trúc dữ liệu?

[Chọn 1-2 ý đúng với giải pháp của nhóm.]

- Nguyên nhân chính là thiếu nguồn đúng hoặc nguồn cũ.
- AI đang phải tự nhớ thông tin thay vì đọc từ nguồn đáng tin cậy.
- Cần kiểm tra dữ liệu trước khi câu trả lời được tạo ra.
- Cần ghi lại lỗi để nhóm biết lỗi nào lặp lại nhiều.

**Hành động phòng vệ chính**:

- [ ] Ngăn lỗi bằng nguồn dữ liệu đúng
- [ ] Phát hiện khi nguồn thiếu hoặc lỗi
- [ ] Khắc phục bằng cách chuyển sang người thật
- [ ] Ghi lại lỗi để cải thiện sau

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

Demo cần có:

- Sơ đồ cách dữ liệu đi qua hệ thống
- Nguồn dữ liệu chính thức
- Bước kiểm tra trước khi AI trả lời
- Cách xử lý khi nguồn thiếu, lỗi hoặc quá cũ
- Cách ghi lại hoặc theo dõi lỗi

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

[Ví dụ: trả lời chậm hơn, phụ thuộc vào nguồn dữ liệu, tốn công duy trì, hệ thống phức tạp hơn.]

**Nhóm giảm vấn đề đó bằng cách nào?**

[Ví dụ: lưu tạm dữ liệu phổ biến, có thông báo khi nguồn lỗi, đặt người phụ trách cập nhật nguồn, giới hạn chỉ áp dụng với câu hỏi rủi ro cao.]

---

## 5. Checklist trước khi nộp

- [ ] Sơ đồ cho thấy dữ liệu đi từ đâu đến đâu.
- [ ] Có bước kiểm tra nguồn trước khi AI trả lời.
- [ ] Có cách xử lý khi không có dữ liệu.
- [ ] Có cách chuyển sang người thật với tình huống rủi ro cao.
- [ ] Có cách biết lỗi này có đang lặp lại không.

**Người phụ trách**: [Tên thành viên]
