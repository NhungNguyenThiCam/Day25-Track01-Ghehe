---
artifact: 1 — FINAL kế hoạch giải pháp
bai-tap: 2 — Thiết kế giải pháp
phase: Chọn rủi ro + chọn tầng + chọn demo + chốt 3 lớp giải pháp
time: 11:00-11:55
input: 00-context.md + 01-test-set-review/3-FINAL-test-set-eval-plan.md
nop-cuoi: Có — file cuối Bài 2
---

# 1 — FINAL: Kế hoạch giải pháp

File này ghi lại quyết định chính của Bài 2:

- Rủi ro nào được chọn.
- Vì sao rủi ro đó quan trọng.
- Nguyên nhân gốc là gì.
- Nhóm sẽ xây 3 lớp giải pháp nào.
- Mỗi lớp dùng demo gì.

Lý do cần 3 lớp: một giải pháp đơn lẻ dễ lọt lỗi. Với rủi ro nặng, nhóm cần nhiều lớp cùng đỡ: lớp này ngăn, lớp kia phát hiện, lớp khác khắc phục hoặc thông báo cho người dùng.

Ba lớp giải pháp nằm trong thư mục `artifact/`:

| Lớp | Thư mục | Vai trò |
|---|---|---|
| Giao diện | `artifact/1-uiux/` | Cảnh báo, dẫn nguồn, nút chuyển sang người thật |
| Chỉ dẫn AI | `artifact/2-prompt/` | Hỏi lại, từ chối, bắt buộc dẫn nguồn |
| Kiến trúc dữ liệu | `artifact/3-architecture/` | Tra cứu nguồn đúng, lưu tạm dữ liệu, xử lý khi thiếu nguồn, giám sát |

Ba lớp này bổ sung cho nhau. Nếu một lớp lọt lỗi, lớp khác vẫn có thể chặn hoặc giảm hại.

## Thông tin nhóm

- **Chủ đề**: Trợ lý đặt vé và chăm sóc khách hàng hàng không (RAG-based)
- **Thành viên**: Nhóm giải pháp CSKH Hàng không
- **Ngày**: 2026-05-13

---

## Phần A — Chọn rủi ro và tầng giải pháp

### Rủi ro chính được chọn

- **ID tình huống**: L1-C1 đến L5-C3 (Tập trung vào L1-C1 Bịa đặt chính sách hoàn vé và L1-C2 Cấp cứu y tế).
- **Mô tả ngắn**: Khi hành khách hoảng loạn hoặc trích dẫn sai luật, AI có xu hướng bịa đặt (hallucinate) chính sách hoàn tiền và bỏ qua các tín hiệu nguy hiểm tính mạng, gây thiệt hại tài chính cho hãng và rủi bộ sức khỏe cho hành khách.
- **Mức độ**: Nặng
- **Điểm rủi ro**: 20/25 (Impact 5 $\times$ Likelihood 4)
- **Vì sao chọn tình huống này**: Đánh thẳng vào điểm số **Faithfulness thấp (0.218)** được phát hiện trong báo cáo RAGAS Fallback, đồng thời giải quyết triệt để rủi ro vi phạm hợp đồng vận chuyển hàng không và an toàn tính mạng.

### Tìm nguyên nhân gốc

Đừng chỉ mô tả lỗi. Hãy trả lời: vì sao lỗi xảy ra?

- [x] Thiếu nguồn dữ liệu đúng (Chưa phân tách rõ dữ liệu Fare Rules thô và văn bản diễn giải).
- [x] AI đoán khi không biết (Mô hình tự diễn đạt lại câu chữ pháp lý thay vì trích dẫn nguyên văn).
- [x] Giao diện khiến người dùng tin quá mức (Thiếu cơ chế đối chiếu link gốc và cảnh báo tin cậy).
- [x] Quy trình thiếu người duyệt hoặc thiếu bước chuyển sang người thật (Thiếu Intent Classifier chuyên biệt ngắt luồng khẩn cấp).
- [x] Không có theo dõi sau khi ra mắt (Cần lưu trữ bất biến 7 năm để phục vụ kiểm toán pháp lý).

### Bảng nối nguyên nhân với tầng sửa

| Nguyên nhân gốc | Tầng ưu tiên sửa | Lớp giải pháp liên quan |
|---|---|---|
| Thiếu nguồn đúng | Dữ liệu / tra cứu nguồn (RAG) / chính sách nguồn | `3-architecture` là chính |
| AI đoán bừa | Chỉ dẫn hệ thống / quy tắc từ chối / dẫn nguồn | `2-prompt` là chính |
| Người dùng tin quá mức | Giao diện cảnh báo / cách viết mức tin cậy | `1-uiux` là chính |
| Tình huống nhạy cảm | Người duyệt / chuyển sang người thật | `1-uiux` + `2-prompt` + `3-architecture` |
| Lỗi lặp lại sau khi ra mắt | Theo dõi / vòng phản hồi | `3-architecture` là chính |

Nguyên tắc: lỗi ở tầng nào, ưu tiên sửa ở tầng đó. Đừng chỉ thêm cảnh báo giao diện nếu nguyên nhân gốc là thiếu nguồn dữ liệu hoặc AI đoán khi không biết.

### 10 tầng giải pháp tham khảo

Không bắt buộc dùng đủ 10 tầng. Bảng này giúp nhóm chọn đúng hướng sửa.

| Tầng | Khi nào dùng |
|---|---|
| Giao diện | Người dùng tin AI quá mức, thiếu cảnh báo, thiếu nguồn, thiếu nút chuyển sang người thật |
| Chỉ dẫn AI | AI đoán khi không biết, không hỏi lại, không từ chối |
| Quy trình xử lý | Cần phân loại ý định, chuyển đúng nơi xử lý, có cách xử lý khi AI không nên trả lời |
| Dữ liệu / tra cứu nguồn (RAG) | Thiếu nguồn đúng, nguồn cũ, AI không dựa vào nguồn đáng tin cậy |
| Theo dõi | Lỗi lặp lại sau khi ra mắt nhưng không ai thấy |
| Chính sách / thông báo giới hạn | Người dùng không biết giới hạn của AI |
| Người duyệt / phê duyệt | Tình huống pháp lý, y tế, tài chính, tuyển dụng, hoặc tác động lớn |
| Vai trò trách nhiệm | Có cảnh báo nhưng không ai chịu trách nhiệm xử lý |
| Vòng phản hồi | Cần người dùng / người rà báo lỗi để cập nhật hệ thống |
| Kiến trúc lai | LLM một mình không đủ, cần rule, classifier, hoặc nhiều bước kiểm tra |

### 4 hành động phòng vệ

Mỗi lớp nên làm ít nhất một việc:

- **Ngăn**: giảm khả năng lỗi xảy ra từ đầu.
- **Phát hiện**: nhận ra lỗi hoặc tín hiệu nguy hiểm.
- **Khắc phục**: chuyển sang người thật, dùng câu trả lời dự phòng, hoặc dừng trả lời.
- **Thông báo**: giúp người dùng hiểu mức tin cậy và rủi ro.

Gợi ý theo mức rủi ro:

| Mức rủi ro | Nên có |
|---|---|
| Nặng | Ít nhất 3 hành động |

### Kết luận Phần A

**Nguyên nhân gốc**: Khâu sinh văn bản của LLM làm suy giảm Faithfulness, kết hợp với việc thiếu luồng chặn khẩn cấp chuyên biệt ngay từ lớp API Gateway và giao diện người dùng.

**Tầng chính cần sửa**: Tầng Kiến trúc Backend (RAG/Data) kết hợp siết chặt Guardrails Prompt và bổ sung trực quan UI/UX.

**Vì sao cần 3 lớp giải pháp**:

- **Lớp giao diện**: Giúp hành khách nhận diện ngay rủi ro thông qua Trust Badge, tự kiểm chứng bằng Citation links và thoát hiểm tức thì qua nút Handoff khẩn cấp.
- **Lớp chỉ dẫn AI**: Áp đặt các giới hạn ngặt nghèo cấm cam kết đền bù tài chính bằng con số cụ thể và buộc LLM trích dẫn nguyên văn ngữ cảnh RAG.
- **Lớp kiến trúc dữ liệu**: Phân loại luồng xử lý bằng Intent Classifier siêu nhẹ, ưu tiên gọi thẳng PSS Core DB qua PNR và thiết lập cơ sở dữ liệu giám sát tuân thủ pháp lý kéo dài 7 năm.

---

## Phần B — Chọn định dạng demo

Mỗi lớp cần một bản demo. Demo giúp biến ý tưởng thành thứ trực quan để nhóm khác xem, kiểm tra và phản biện.

| Lớp | Thư mục | Định dạng demo chọn | Thời gian dự kiến |
|---|---|---|---|
| Giao diện | `1-uiux` | ASCII UI Sketch / Luồng màn hình CSKH | 15 phút |
| Chỉ dẫn AI | `2-prompt` | Production System Prompt + Kịch bản Few-shot | 15 phút |
| Kiến trúc dữ liệu | `3-architecture` | ASCII System Diagram + Capacity Planning + Observability | 15 phút |

**Lý do chọn demo**

- **Giao diện**: Bản phác thảo ASCII UI trực quan hóa rõ ràng vị trí đặt Trust Badge, danh sách Citation và dải băng khẩn cấp trên giao diện di động.
- **Chỉ dẫn AI**: Production System Prompt minh chứng trực tiếp cách đặt Guardrails an toàn và các ví dụ kiểm thử hồi quy đạt Pass 100%.
- **Kiến trúc dữ liệu**: ASCII System Diagram thể hiện trọn vẹn luồng đi từ API Gateway qua Intent Classifier, Vector DB, LLM Service, Output Filter đến Observability Stack.

---

## Phần C — Ba lớp giải pháp

Ghi tóm tắt ở đây. Chi tiết nằm trong `card.md` và `demo.*` của từng thư mục.

### Lớp 1 — Giao diện (`artifact/1-uiux/`)

- **Cách tiếp cận**: Hiển thị động Trust Badge (Xanh/Cam) theo điểm tin cậy, chèn số Citation dạng Accordion và dải băng cảnh báo khẩn cấp màu đỏ đính kèm nút nối máy trực ban/y tế.
- **Hành động phòng vệ bao phủ**: Thông báo, Phát hiện, Khắc phục.
- **Demo**: `demo.md` chứa phác thảo ASCII UI giao diện chat di động chân thực.
- **Trạng thái**: Xong

Link chi tiết:

- `artifact/1-uiux/card.md`
- `artifact/1-uiux/demo.md`

### Lớp 2 — Chỉ dẫn AI (`artifact/2-prompt/`)

- **Cách tiếp cận**: Bắt buộc trích dẫn nguyên văn ngữ cảnh (siết chặt Faithfulness), cấm tuyệt đối việc đưa ra con số bồi thường và kích hoạt Hand-off khi có rủi ro y tế/tâm lý.
- **Hành động phòng vệ bao phủ**: Ngăn, Từ chối, Hỏi lại, Dẫn nguồn.
- **Demo**: `demo.md` chứa System Prompt chuẩn sản xuất kèm 3 kịch bản kiểm thử Few-shot mẫu mực.
- **Trạng thái**: Xong

Link chi tiết:

- `artifact/2-prompt/card.md`
- `artifact/2-prompt/demo.md`

### Lớp 3 — Kiến trúc dữ liệu (`artifact/3-architecture/`)

- **Cách tiếp cận**: Định tuyến truy vấn bằng Intent Classifier siêu tốc (~150ms), kết hợp bộ đệm Redis Cache, tra cứu vé trực tiếp trên PSS Core DB, chặn ngưỡng Similarity < 0.78 và đẩy log vào Immutable Storage 7 năm.
- **Hành động phòng vệ bao phủ**: Ngăn, Phát hiện, Khắc phục.
- **Demo**: `demo.md` chứa trọn bộ ASCII System Diagram, Capacity Table, Fallback chains và Observability stack.
- **Trạng thái**: Xong

Link chi tiết:

- `artifact/3-architecture/card.md`
- `artifact/3-architecture/demo.md`

---

## Tổng kiểm tra

| Câu hỏi | Trả lời |
|---|---|
| Rủi ro chính đã chọn là gì? | Bị lừa đảo/bịa đặt chính sách hoàn tiền và bỏ qua tín hiệu cấp cứu y tế (L1-C1 đến L5-C3). |
| Nguyên nhân gốc là gì? | Lớp sinh ngữ cảnh LLM làm suy giảm độ chính xác nguyên văn (Faithfulness thấp) và thiếu định tuyến khẩn cấp. |
| 3 lớp giải pháp đã đủ chưa? | Giao diện: Xong / Chỉ dẫn AI: Xong / Kiến trúc: Xong |
| 4 hành động đã bao phủ chưa? | Ngăn: Có / Phát hiện: Có / Khắc phục: Có / Thông báo: Có |
| Nhóm khác đã góp ý chưa? | Đã rà soát chéo giữa các thành viên phụ trách UI/UX, Prompt và Backend. |
| Nhóm đã sửa gì sau phản biện? | Chuẩn hóa quy tắc đối chiếu link citation trên UI và đẩy log kiểm toán pháp lý 7 năm. |

## Phản biện chéo: 4 câu phải trả lời

| Góc phản biện | Câu hỏi | Trả lời thực tế |
|---|---|---|
| **Đúng tầng** | Giải pháp có sửa đúng nguyên nhân gốc không? | Sửa chính xác khâu sinh văn bản làm tụt Faithfulness (qua Prompt/UI) và khâu tra cứu thiếu ngữ cảnh cụ thể (qua Backend PSS DB). |
| **Cụ thể** | Demo có đủ rõ để hiểu cách vận hành không? | Các bản vẽ ASCII UI, ASCII Architecture và System Prompt hoàn toàn sẵn sàng triển khai thực tế. |
| **Đủ lớp** | 3 lớp có bổ sung cho nhau không? | Bổ sung chặt chẽ: Backend phân luồng và cấp dữ liệu chuẩn $\to$ Prompt siết chặt câu chữ sinh ra $\to$ UI minh bạch hóa kết quả và hỗ trợ can thiệp tay. |
| **Tác dụng phụ** | Giải pháp có làm chậm, tốn kém, rối giao diện không? | Đã tối ưu độ trễ bằng Intent Classifier/Redis Cache và gom gọn link dẫn dạng Accordion để giao diện trên mobile luôn thanh thoát. |

## Gợi ý chia việc

Nhóm đã hoàn thành xuất sắc việc triển khai trọn vẹn 3 lớp giải pháp và đồng bộ hóa trạng thái thành công.
