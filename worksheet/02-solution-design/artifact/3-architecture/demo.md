---
artifact: 3 — Demo kiến trúc dữ liệu
format: sơ đồ xử lý + bảng thành phần
---

# demo.md — Demo kiến trúc dữ liệu

File này dùng để đặt sơ đồ và mô tả ngắn cách hệ thống giảm rủi ro.

---

## 1. Sơ đồ cách hệ thống xử lý

```text
[Đặt sơ đồ ở đây]

Ví dụ khung:

Người dùng hỏi
  -> Phân loại câu hỏi
  -> Có phải câu hỏi rủi ro cao không?
      -> Không: AI trả lời như bình thường
      -> Có: Tra nguồn chính thức
          -> Có dữ liệu: AI trả lời kèm nguồn
          -> Không có dữ liệu: Chuyển sang người thật
  -> Ghi lại để theo dõi lỗi
```

---

## 2. Thành phần chính

| Thành phần | Nhận gì? | Làm gì? | Trả ra gì? |
|---|---|---|---|
| Phân loại câu hỏi | Câu hỏi của người dùng | Xác định có rủi ro cao không | Trả lời thường / cần kiểm tra nguồn |
| Nguồn chính thức | Chủ đề cần kiểm tra | Tìm dữ liệu mới nhất | Thông tin + nguồn |
| Bộ xử lý khi thiếu nguồn | Kết quả không có dữ liệu | Không cho AI đoán | Yêu cầu chuyển sang người thật |
| Ghi lại lỗi | Câu hỏi + kết quả | Lưu lỗi để xem lại | Danh sách lỗi lặp lại |

---

## 3. Khi hệ thống gặp vấn đề

| Khi nào lỗi xảy ra? | Hệ thống làm gì? | Người dùng thấy gì? |
|---|---|---|
| Nguồn chính thức không có dữ liệu | | |
| Nguồn bị lỗi hoặc quá chậm | | |
| Câu hỏi vượt phạm vi AI | | |
| Lỗi này lặp lại nhiều lần | | |

---

## 4. Kiểm tra nhanh

- [ ] Sơ đồ không chỉ là “AI trả lời tốt hơn”, mà có bước kiểm tra cụ thể.
- [ ] Có cách xử lý khi thiếu dữ liệu.
- [ ] Có cách chuyển sang người thật.
- [ ] Có cách theo dõi để lần sau sửa tốt hơn.
