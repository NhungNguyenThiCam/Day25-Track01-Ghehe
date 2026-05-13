---
artifact: 3 — Lớp kiến trúc dữ liệu
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp kiến trúc dữ liệu (RAG Backend & Observability)

**Tình huống xử lý**: L1-C1 đến L5-C3 (Tập trung chặn đứng các rủi ro bịa đặt chính sách hoàn tiền và xử lý sai luồng tra cứu PNR).
Xem `../../1-map-and-format.md` Phần A và báo cáo RAGAS tại `EVAL_RESULTS_FALLBACK.md`.

---

## 1. Giải pháp là gì?

Xây dựng hệ thống RAG đa tầng kết hợp phân loại ý định (Intent Classifier), tra cứu trực tiếp cơ sở dữ liệu lõi của hãng (PSS Core DB) qua mã PNR, và kiểm tra ngưỡng tin cậy (Similarity Score $\ge$ 0.78). Nếu tài liệu truy xuất có độ tương đồng thấp, hệ thống tự động ngắt luồng sinh LLM để trả về câu từ chối tĩnh nhằm triệt tiêu hoàn toàn rủi ro bịa đặt.

---

## 2. Vì sao sửa ở lớp kiến trúc dữ liệu?

- Báo cáo `EVAL_RESULTS_FALLBACK.md` cho thấy **Context Precision rất cao (0.881)**, khẳng định khâu truy xuất (retrieval) hoạt động tốt. Tuy nhiên, **Faithfulness thấp (0.218)** chỉ ra rằng nếu để mô hình sinh văn bản tự do tổng hợp mà không kiểm soát đầu ra/đầu vào thô, rủi ro ảo giác tài chính là tất yếu.
- Kiến trúc dữ liệu đóng vai trò phân luồng ngay từ Gateway: các câu hỏi cần tra cứu vé cụ thể bắt buộc phải đi qua API PSS Core DB thay vì chỉ dựa vào Vector DB chung chung.
- Lớp kiến trúc thiết lập cơ sở hạ tầng giám sát (Observability) bằng cách đẩy log phiên trò chuyện khẩn cấp vào lưu trữ bất biến (7 năm) để phục vụ công tác đối soát pháp lý.

**Hành động phòng vệ chính**:

- [x] Ngăn lỗi bằng nguồn dữ liệu đúng
- [x] Phát hiện khi nguồn thiếu hoặc lỗi
- [x] Khắc phục bằng cách chuyển sang người thật
- [x] Ghi lại lỗi để cải thiện sau

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

Demo cần có:

- Sơ đồ luồng dữ liệu toàn diện (ASCII System Diagram)
- Bảng quy hoạch năng lực và trễ (Capacity Planning Table)
- Các chuỗi dự phòng kỹ thuật (Fallback Chains)
- Ngăn xếp giám sát và tuân thủ pháp lý (Observability Stack)

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

Hệ thống có nhiều trạm kiểm duyệt (Intent Classifier, Redis Cache, Vector DB, Output Filter) làm tăng độ trễ tổng thể (Latency) và chi phí vận hành API trên quy mô lớn.

**Nhóm giảm vấn đề đó bằng cách nào?**

Sử dụng mô hình phân loại Intent siêu nhẹ (Fast Lightweight LLM/Rules) với độ trễ p50 chỉ ~150ms. Áp dụng cơ chế bộ đệm Redis Cache (TTL 24h) cho các câu hỏi chính sách tĩnh phổ biến để giảm tải cho PSS Core DB và Vector DB.

---

## 5. Checklist trước khi nộp

- [x] Sơ đồ cho thấy dữ liệu đi từ đâu đến đâu.
- [x] Có bước kiểm tra nguồn trước khi AI trả lời.
- [x] Có cách xử lý khi không có dữ liệu.
- [x] Có cách chuyển sang người thật với tình huống rủi ro cao.
- [x] Có cách biết lỗi này có đang lặp lại không.

**Người phụ trách**: Kỹ sư Kiến trúc Dữ liệu Backend
