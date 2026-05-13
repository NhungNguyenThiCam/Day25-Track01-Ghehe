---
artifact: 2 — Lớp chỉ dẫn AI
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp chỉ dẫn AI

**Tình huống xử lý**: T-__  
Xem `../../1-map-and-format.md` Phần A.

---

## 1. Giải pháp là gì?

[Viết 2-3 câu. Nói rõ nhóm sẽ thêm luật, giới hạn hoặc ví dụ mẫu nào để AI trả lời an toàn hơn.]

Ví dụ:

> Khi người dùng hỏi ngày, số tiền hoặc chính sách tuyển sinh, AI chỉ được trả lời nếu có nguồn chính thức. Nếu thiếu nguồn, AI phải nói rõ là chưa xác minh được và chuyển cho tư vấn viên.

---

## 2. Vì sao sửa ở lớp chỉ dẫn AI?

[Chọn 1-2 ý đúng với giải pháp của nhóm.]

- AI đang trả lời quá tự tin khi thiếu nguồn.
- AI đang chiều theo giả định sai của người dùng.
- AI cần luật rõ: khi nào trả lời, khi nào từ chối, khi nào chuyển sang người thật.
- Có thể sửa nhanh bằng prompt trước khi thay đổi hệ thống lớn hơn.

**Hành động phòng vệ chính**:

- [ ] Ngăn câu trả lời sai ngay từ đầu
- [ ] Bắt buộc nêu nguồn khi nói về thông tin quan trọng
- [ ] Từ chối trả lời khi thiếu căn cứ
- [ ] Chuyển người thật khi vượt phạm vi

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

Demo cần có:

- Luật chính cho AI
- Mẫu câu khi thiếu nguồn
- Mẫu câu khi cần chuyển sang người thật
- 2-3 ví dụ hỏi đáp để kiểm tra luật
- Kết quả thử lại với vài tình huống từ Bài 1

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

[Ví dụ: AI từ chối quá nhiều, câu trả lời cứng, trải nghiệm chậm hơn vì phải kiểm tra nguồn.]

**Nhóm giảm vấn đề đó bằng cách nào?**

[Ví dụ: chỉ bắt buộc nguồn với thông tin rủi ro cao; tách từ chối mềm và từ chối cứng; kiểm tra lại bằng bộ tình huống.]

---

## 5. Checklist trước khi nộp

- [ ] Luật viết đủ cụ thể để AI làm theo.
- [ ] Có mẫu câu khi AI không có đủ thông tin.
- [ ] Có ví dụ cho tình huống dễ sai.
- [ ] Có thử lại bằng tình huống trong Bài 1.
- [ ] Không dùng prompt như cách duy nhất nếu lỗi nằm ở dữ liệu hoặc quy trình.

**Người phụ trách**: [Tên thành viên]
