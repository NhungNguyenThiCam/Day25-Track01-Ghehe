---
artifact: 1 — Demo giao diện
format: ASCII UI Sketch / Luồng màn hình CSKH Hàng không
---

# demo.md — Demo giao diện (ASCII UI Sketch)

Bản phác thảo giao diện trò chuyện trên thiết bị di động (Mobile Chat UI) được thiết kế đặc thù nhằm minh bạch hóa nguồn trích dẫn (giải quyết Faithfulness thấp) và cung cấp lối thoát hiểm khẩn cấp (Emergency Hand-off) cho hành khách.

---

## 1. Phác thảo Màn hình Chính (ASCII UI Sketch)

```text
+---------------------------------------------------+
|  12:16  (i)           VNA ASSISTANT          [X]  |
+---------------------------------------------------+
|                                                   |
|  [Hành khách]                                     |
|  Người nhà tôi vừa mất gấp, chuyến bay cất cánh   |
|  trong 2 tiếng nữa. Vé Economy Super Lite có được |
|  linh động hoàn 100% tiền mặt không?              |
|                                         12:14     |
|                                                   |
|  [AI Assistant]                                   |
|  +---------------------------------------------+  |
|  | ✓ Đã kiểm chứng từ Fare Rules Matrix        |  |
|  +---------------------------------------------+  |
|  Xin chia buồn cùng gia đình bạn.                 |
|                                                   |
|  Theo quy định hiện hành, hạng vé Economy Super   |
|  Lite [1] không áp dụng hoàn vé tự nguyện [2].    |
|  Chính sách hỗ trợ vé tang chế chính thức [3] chỉ |
|  áp dụng giảm giá mua mới, không hỗ trợ hoàn tiền |
|  hồi tố đối với vé đã xuất.                       |
|                                                   |
|  +---------------------------------------------+  |
|  | 🔗 Nguồn trích dẫn gốc (Bấm để đối chiếu):  |  |
|  | [1] Bảng Điều kiện Hạng vé Eco Super Lite   |  |
|  | [2] Chính sách Hoàn/Hủy Tự nguyện (Mục 4.2) |  |
|  | [3] Quy định Hỗ trợ Nhân đạo & Tang chế     |  |
|  +---------------------------------------------+  |
|                                         12:15     |
|                                                   |
|  +---------------------------------------------+  |
|  | ⚠️ BẠN ĐANG TRONG TÌNH TRẠNG KHẨN CẤP?      |  |
|  | Nhấn nút bên dưới để kết nối ngay với Trưởng|  |
|  | ca trực CSKH hoặc Đội Y tế Sân bay (< 1s).  |  |
|  |                                             |  |
|  | [ 📞 KẾT NỐI NHÂN VIÊN TRỰC BAN / Y TẾ ]    |  |
|  +---------------------------------------------+  |
|                                                   |
+---------------------------------------------------+
|  Nhập tin nhắn...                       [ Gửi ]   |
+---------------------------------------------------+
```

---

## 2. Trạng thái cần minh họa

| Trạng thái | Người dùng thấy gì? | Người dùng làm gì tiếp? |
|---|---|---|
| **Có nguồn xác minh** | Nhãn xanh lá `✓ Đã kiểm chứng` và danh sách liên kết trích dẫn `[1]`, `[2]` đính kèm cuối câu trả lời. | Bấm vào liên kết để đọc nguyên văn văn bản pháp lý/quy định Fare Rules gốc nhằm tự xác thực. |
| **Chưa có nguồn / Low Sim** | Nhãn cam `⚠ Thông tin mang tính tham khảo` kèm thông báo bot chưa tìm thấy điều khoản cụ thể trong RAG. | Bấm nút chuyển tiếp câu hỏi sang cho nhân viên con người tra cứu trực tiếp trên PSS Core DB. |
| **AI không nên tự trả lời** | Ngắt luồng trả lời tự động, hiển thị câu từ chối chuẩn mực và khung thông tin liên hệ chính thức. | Gọi trực tiếp Hotline 1800-xxx hoặc điền form yêu cầu hỗ trợ ngoại lệ. |
| **Cần chuyển sang người thật** | Khung dải băng đỏ khẩn cấp `⚠️ BẠN ĐANG TRONG TÌNH TRẠNG KHẨN CẤP?` và nút gọi nhanh trực ban/y tế. | Bấm nút để được ưu tiên nối máy hoặc điều phối xe cấp cứu mặt đất ngay lập tức. |

---

## 3. Ghi chú cho từng thành phần

- **Nhãn tin cậy (Trust Badge)**: Nằm ngay đầu bong bóng chat của AI. Đổi màu tự động: Xanh lá (Score $\ge$ 0.85), Cam (Score < 0.85). Giúp người dùng định hình mức độ tin cậy ngay trước khi đọc nội dung.
- **Khung trích dẫn (Citations Box)**: Nằm liền kề dưới nội dung trả lời. Liệt kê rõ ràng các số thứ tự tương ứng với hyperlink trích xuất từ dữ liệu RAG (khắc phục điểm mù Faithfulness thấp khi văn bản bị diễn đạt lại).
- **Khung thoát hiểm (Escalation Banner)**: Xuất hiện tự động ở đáy màn hình chat khi hệ thống phát hiện từ khóa rủi ro cao (`mất`, `bầu`, `ra máu`, `kiện`, `quản lý thị trường`). Kích hoạt gọi điện hoặc mở kênh chat ưu tiên không qua hàng đợi.

---

## 4. Kiểm tra nhanh

- [x] Nhìn vào demo là hiểu rủi ro đang được chặn ở đâu.
- [x] Có trạng thái khi AI không có đủ thông tin.
- [x] Có cách chuyển sang người thật.
- [x] Câu chữ đủ ngắn để đặt trên màn hình thật.
