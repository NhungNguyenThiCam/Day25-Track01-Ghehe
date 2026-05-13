---
artifact: 1 — Lớp giao diện
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp giao diện (Cảnh báo Nguồn & Nút Khẩn cấp)

**Tình huống xử lý**: L1-C1 đến L5-C3 (Đặc biệt tập trung vào L1-C1 Bịa đặt chính sách hoàn vé và L1-C2 Cấp cứu y tế).
Xem `../../1-map-and-format.md` Phần A và kết quả đánh giá tại `EVAL_RESULTS_FALLBACK.md`.

---

## 1. Giải pháp là gì?

Giao diện tích hợp hệ thống nhãn xác thực động dựa trên điểm tin cậy (Confidence Score) và trích xuất nguyên văn liên kết nguồn (Citations) từ bảng Fare Rules/Nghị định 92. Khi phát hiện các từ khóa nhạy cảm về y tế hoặc khi bot từ chối do thiếu nguồn tin cậy, màn hình lập tức hiển thị dải băng cảnh báo màu đỏ kèm nút bấm gọi nhanh "Kết nối Quầy CSKH / Đội Y tế Sân bay" trong vòng 1 giây.

---

## 2. Vì sao sửa ở lớp giao diện?

- Người dùng đang chịu áp lực cao (trễ chuyến, tang chế, thai sản) dễ tin câu trả lời của AI quá mức hoặc hoảng loạn nếu bot trả lời vòng vo.
- Kết quả `EVAL_RESULTS_FALLBACK.md` cho thấy **Faithfulness thấp (0.218)** dù **Context Precision cao (0.881)**, nghĩa là AI lấy đúng tài liệu nhưng diễn đạt dễ gây hiểu lầm. Giao diện buộc phải hiển thị link trích dẫn gốc để hành khách tự đối chiếu.
- Giao diện là lớp chặn cuối cùng trực quan nhất để điều hướng người dùng sang luồng hỗ trợ con người (Human-in-the-loop) khi hệ thống sinh ngữ cảnh rủi ro.

**Hành động phòng vệ chính**:

- [x] Thông báo rõ giới hạn
- [x] Phát hiện dấu hiệu thiếu nguồn
- [x] Chuyển người thật khi cần
- [x] Giúp người dùng kiểm tra lại nguồn

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

**Định dạng demo**:

- [x] Phác thảo màn hình (ASCII UI Sketch)
- [x] Luồng màn hình
- [ ] Bản HTML đơn giản
- [ ] Ảnh hoặc link prototype

**Thành phần cần có trong demo**:

- Trạng thái có nguồn xác minh (Verified Badge + Hyperlinks)
- Trạng thái chưa có nguồn/Low Confidence (Warning Badge)
- Cách người dùng chuyển sang người thật (Emergency Escalation Button)
- Câu chữ cảnh báo ngắn, dễ hiểu, thấu cảm

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

Màn hình hiển thị quá nhiều liên kết trích dẫn và nhãn dán có thể khiến giao diện chat trên điện thoại trở nên chật chội, làm người dùng lười đọc hoặc cảm thấy hệ thống thiếu thân thiện.

**Nhóm giảm vấn đề đó bằng cách nào?**

Chỉ hiển thị nhãn cảnh báo nổi bật đối với các câu hỏi nhạy cảm liên quan đến tài chính (hoàn tiền, phí đổi) và an ninh/y tế. Các liên kết trích dẫn được gộp gọn dưới dạng chú thích dạng số `[1]`, `[2]` có thể bấm để mở rộng (Accordion view).

---

## 5. Checklist trước khi nộp

- [x] Giải pháp gắn đúng với một rủi ro chính.
- [x] Demo nhìn vào là hiểu vấn đề được chặn ở đâu.
- [x] Có đủ trạng thái bình thường và trạng thái lỗi.
- [x] Có cách chuyển sang người thật khi AI không nên tự xử lý.
- [x] Câu chữ trong giao diện ngắn, không đổ hết trách nhiệm cho người dùng.

**Người phụ trách**: Nhóm giải pháp CSKH Hàng không
