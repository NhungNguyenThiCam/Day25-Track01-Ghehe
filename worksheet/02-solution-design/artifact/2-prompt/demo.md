---
artifact: 2 — Demo chỉ dẫn AI
format: prompt tham khảo + ví dụ hỏi đáp
---

# demo.md — Demo chỉ dẫn AI

File này dùng để đặt bản prompt tham khảo và kết quả thử nhanh.

---

## 1. Prompt tham khảo

```text
Bạn là AI [vai trò] trong bối cảnh [tóm tắt từ 00-context.md].

Luật bắt buộc:
1. Không nêu ngày, số tiền, chính sách hoặc lời khuyên quan trọng nếu không có nguồn chính thức.
2. Nếu chưa có nguồn xác minh, nói rõ: "Mình chưa có thông tin được xác minh về [chủ đề]. Mình sẽ chuyển câu hỏi này cho người phụ trách."
3. Không xác nhận giả định của người dùng chỉ vì người dùng hỏi theo kiểu "có đúng không?".
4. Nếu câu hỏi vượt phạm vi AI nên xử lý, từ chối ngắn gọn và hướng người dùng đến người thật hoặc kênh phù hợp.

Cách nêu nguồn:
- Với thông tin quan trọng, phải ghi rõ nguồn.
- Nếu không có nguồn, không được đoán.
- Nếu nguồn có thể đã cũ, phải nói rõ cần kiểm tra lại.
```

---

## 2. Ví dụ kiểm tra

### Ví dụ 1 — Hỏi thông tin cần nguồn

**Người dùng**: "[Câu hỏi]"

**AI nên trả lời**: "[Câu trả lời mong muốn]"

### Ví dụ 2 — Người dùng đưa giả định sai

**Người dùng**: "[Câu hỏi]"

**AI nên trả lời**: "[Câu trả lời mong muốn]"

### Ví dụ 3 — Câu hỏi vượt phạm vi

**Người dùng**: "[Câu hỏi]"

**AI nên trả lời**: "[Câu trả lời mong muốn]"

---

## 3. Kết quả thử lại

Chọn vài tình huống từ Bài 1 và thử prompt này.

| Mã tình huống | Kỳ vọng | AI trả lời gì? | Đạt/Không đạt/Chưa rõ | Ghi chú |
|---|---|---|---|---|
| T-01 | | | | |
| T-02 | | | | |
| T-03 | | | | |

**Tỉ lệ đạt với tình huống rủi ro cao**: __/__

---

## 4. Chỉnh sau khi thử

- Điều gì AI vẫn làm sai?
- Cần thêm luật nào?
- Có luật nào làm AI từ chối quá nhiều không?
- Cần phối hợp thêm giao diện hoặc dữ liệu không?
