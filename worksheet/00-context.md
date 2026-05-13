---
title: 00 — Bối cảnh sản phẩm của nhóm
section: Day 25 — dùng lại cho mọi cuộc trò chuyện với AI
format: Nhóm
time: Điền 5 phút đầu buổi
---

# 00-context.md — Bối cảnh sản phẩm của nhóm

Điền file này một lần ở đầu buổi. Sau đó, mỗi lần dùng AI, hãy đưa toàn bộ nội dung file này vào đầu cuộc trò chuyện.

Lý do: AI không tự nhớ bối cảnh giữa các cuộc trò chuyện. Nếu mỗi lần đưa bối cảnh khác nhau, câu trả lời cũng sẽ lệch.

---

## 1. Sản phẩm

- **Tên sản phẩm / bot**: Airline Customer Service AI Assistant (RAG-based)
- **Sản phẩm giúp ai làm gì**: Hỗ trợ hành khách tra cứu thông tin hành lý, chính sách giá vé (Fare Rules), quy định đổi/hoàn vé và các yêu cầu hỗ trợ đặc biệt.
- **Người dùng gặp sản phẩm ở đâu**: Website chính thức và ứng dụng di động (App) của hãng hàng không.
- **Giai đoạn hiện tại**: Chuẩn bị ra mắt (Pre-launch safety evaluation).

---

## 2. Phạm vi

**AI được làm gì**

- Truy xuất và trả lời thông tin dựa trên bảng điều kiện giá vé (Fare Rules Matrix) và chính sách hành lý chính thức.
- Hướng dẫn quy trình thực hiện đổi vé hoặc hoàn vé trên hệ thống tự phục vụ.
- Cung cấp các đường link dẫn đến tài liệu chính sách và Fare Conditions của hãng.

**AI không được làm gì**

- Không được cam kết số tiền bồi thường hoặc số tiền hoàn lại cụ thể bằng con số.
- Không được tự ý thực hiện các giao dịch tài chính (thanh toán/hoàn tiền) mà không có sự phê duyệt của nhân viên.
- Không được hứa hẹn các ngoại lệ chính sách nằm ngoài dữ liệu nguồn (RAG).

**Vì sao có giới hạn này**

Tránh rủi ro pháp lý và trách nhiệm bồi thường thiệt hại tài chính cho hãng (tương tự tiền lệ vụ Moffatt v. Air Canada 2024). Đảm bảo tuân thủ nghĩa vụ cung cấp thông tin chính xác theo Nghị định 92/2021/NĐ-CP của Chính phủ Việt Nam.

---

## 3. Người dùng

- **Là ai**: Hành khách quốc tế và nội địa, đa dạng độ tuổi và trình độ công nghệ, đang sử dụng dịch vụ của hãng.
- **Họ hỏi AI khi nào**: Khi chuyến bay bị delay/hủy, sát giờ bay, hoặc vào khung giờ đêm (22h-4h) khi tổng đài hotline thường xuyên quá tải.
- **Họ cần quyết định gì sau khi hỏi AI**: Quyết định có thực hiện hủy vé, đổi chuyến bay hoặc mua thêm dịch vụ bổ trợ ngay lập tức hay không.
- **Khi nào họ dễ bị tổn thương / dễ hiểu sai**: Khi đang ở trạng thái stress cao do sự cố chuyến bay, vội vã cần thông tin tài chính chính xác để ra quyết định nhanh.
- **Họ thường tin AI đến mức nào**: Tin tưởng rất cao vì AI nằm trên kênh Official của hãng, người dùng thường coi lời chatbot là "phát ngôn cuối cùng".

---

## 4. Bối cảnh ngành

- **Sự cố tương tự đã từng xảy ra**: Vụ kiện Air Canada (2024) hãng phải bồi thường thiệt hại do chatbot bịa đặt chính sách hỗ trợ tang chế sai sự thật.
- **Quy định hoặc ràng buộc liên quan**: Nghị định 92/2021/NĐ-CP về kinh doanh hàng không; Luật bảo vệ quyền lợi người tiêu dùng.
- **Nguồn chính thức nên ưu tiên**: Fare Rules Matrix, Vietnam Airlines Fare Conditions, chính sách hành lý của hãng.

---

## 5. Ghi chú thêm

Hệ thống sử dụng kiến trúc RAG. Trọng tâm kiểm thử là ngăn chặn lỗi Hallucination (bịa đặt chính sách) về việc hoàn tiền cho các hạng vé giá rẻ (như Economy Super Lite) vốn thường không được hoàn trả.

---

## Cách dùng

```text
1. Mở công cụ AI phù hợp với bước đang làm.
2. Đưa toàn bộ nội dung file này vào đầu cuộc trò chuyện.
3. Chọn prompt tham khảo từ thư mục ../prompts/ và chỉnh lại nếu cần.
4. Đọc lại bản nháp AI tạo ra.
5. Sửa lại cho đúng bối cảnh nhóm.
6. Lưu kết quả vào đúng file trong worksheet/.
```

Ghi chú: nội dung trong `[...]` là chỗ cần điền. Sau khi điền xong, xóa dấu ngoặc nếu không cần giữ.
