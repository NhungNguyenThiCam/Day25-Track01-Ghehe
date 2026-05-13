---
artifact: 2 — Lớp chỉ dẫn AI
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp chỉ dẫn AI (System Prompt & Guardrails)

**Tình huống xử lý**: L1-C1 (Mồi nhử tang chế), L1-C2 (Cấp cứu y tế), L1-C3 (Nghị định 92/2021) và các tấn công thao túng tâm lý (L2-C3).
Xem `../../1-map-and-format.md` Phần A và báo cáo RAGAS tại `EVAL_RESULTS_FALLBACK.md`.

---

## 1. Giải pháp là gì?

Thiết lập System Prompt đa tầng áp đặt các giới hạn nghiêm ngặt (Guardrails) cho mô hình sinh văn bản: tuyệt đối không hứa hẹn bồi thường tài chính bằng con số cụ thể, bắt buộc trích dẫn nguyên văn văn bản RAG kèm citation link (giải quyết triệt để vấn đề Faithfulness thấp), và tự động chuyển sang quy trình từ chối an toàn hoặc báo động y tế khi phát hiện rủi ro tính mạng.

---

## 2. Vì sao sửa ở lớp chỉ dẫn AI?

- Mô hình LLM mặc định có xu hướng chiều lòng người dùng (sycophancy) khi bị đặt vào bối cảnh áp lực hoặc thương hại.
- Chỉ số **Faithfulness thấp (0.218)** từ kết quả RAGAS chứng minh rằng nếu để LLM tự do diễn đạt lại tài liệu chính sách, rủi ro sai lệch hoặc bịa đặt (hallucination) điều kiện hoàn vé là cực kỳ cao. Prompt buộc phải siết chặt quy tắc "Chỉ trả lời chính xác những gì có trong ngữ cảnh được cung cấp".
- Lớp prompt cho phép triển khai nhanh chóng các kịch bản mẫu (few-shot examples) hướng dẫn bot cách thấu cảm mà không hứa hẹn phá vỡ chính sách hãng.

**Hành động phòng vệ chính**:

- [x] Ngăn câu trả lời sai ngay từ đầu
- [x] Bắt buộc nêu nguồn khi nói về thông tin quan trọng
- [x] Từ chối trả lời khi thiếu căn cứ
- [x] Chuyển người thật khi vượt phạm vi

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

Demo cần có:

- Luật chính cho AI (System Instructions)
- Mẫu câu khi thiếu nguồn (Static Refusal Templates)
- Mẫu câu khi cần chuyển sang người thật (Emergency Handoff Templates)
- Các ví dụ hỏi đáp kiểm thử (Few-shot testing)
- Kết quả đối chiếu với danh sách tình huống rủi ro cao

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

Mô hình có thể trở nên quá thận trọng (over-refusal), từ chối trả lời ngay cả những câu hỏi thông thường về giá vé hoặc điều kiện hành lý đơn giản nếu câu hỏi hơi thiếu ngữ cảnh, dẫn đến trải nghiệm giao tiếp máy móc, thiếu tự nhiên.

**Nhóm giảm vấn đề đó bằng cách nào?**

Cung cấp cho LLM hướng dẫn phân tầng rõ ràng: trả lời đầy đủ, thấu cảm với các câu hỏi tra cứu thông thường; chỉ kích hoạt từ chối cứng (hard refusal) khi truy vấn yêu cầu cam kết ngoại lệ hoàn tiền hoặc can thiệp y tế/pháp lý.

---

## 5. Checklist trước khi nộp

- [x] Luật viết đủ cụ thể để AI làm theo.
- [x] Có mẫu câu khi AI không có đủ thông tin.
- [x] Có ví dụ cho tình huống dễ sai.
- [x] Có thử lại bằng tình huống trong Bài 1.
- [x] Không dùng prompt như cách duy nhất nếu lỗi nằm ở dữ liệu hoặc quy trình.

**Người phụ trách**: Nhóm Kỹ sư Prompt & Guardrails
