---
artifact: 2 — Hội tụ
bai-tap: 1 — Rà bộ kiểm thử
phase: Gộp tình huống + lọc trùng + chấm rủi ro
time: 10:05-10:30
input: 1-diverge.md của từng thành viên
nop-cuoi: Không — file trung gian
---

# 2 — Giai đoạn Hội tụ: gộp và lọc

Mục tiêu: nhóm đi từ 30-45 tình huống thô xuống còn 10-15 tình huống chắc, ít trùng, có mức ưu tiên rõ.

Lý do làm bước này: nếu chỉ chọn tình huống theo cảm giác, nhóm dễ giữ các tình huống nghe hay nhưng trùng nhau, hoặc bỏ sót tình huống nghiêm trọng. Giai đoạn này giúp nhóm chọn có lý do.

## Quy trình 25 phút

```text
5 phút  — Gộp toàn bộ tình huống của nhóm
10 phút — Lọc trùng theo kiểu lỗi
10 phút — Chấm điểm rủi ro
```

---

## Phần A — Gộp toàn bộ tình huống của nhóm

Mỗi thành viên đưa 15 tình huống từ `1-diverge.md` Phần C vào bảng dưới.

Ở bước này chưa lọc. Chỉ gộp lại để nhìn đủ toàn bộ ý tưởng.

| ID | Người nộp | Góc nhìn | Kiểu lỗi | Tình huống kiểm thử | Nguồn |
|---|---|---|---|---|---|
| C-A01 | Thành viên A | L1 | Bịa thông tin | | sự cố thật |
| C-A02 | Thành viên A | L2 | Chiều theo người dùng | | AI gợi ý |
| C-B01 | Thành viên B | | | | |
| C-C01 | Thành viên C | | | | |

Tổng số tình huống: ___

---

## Phần B — Lọc trùng theo kiểu lỗi

Dán `00-context.md`, bảng Phần A, và `prompts/03-convergent-analysis.md` vào AI để được gợi ý nhóm lỗi và trùng lặp.

Sau đó nhóm phải tự rà lại. AI chỉ hỗ trợ bản nháp.

Quy tắc lọc trùng:

- Cùng kiểu lỗi.
- Cùng cách kích hoạt lỗi.
- Cùng hành vi AI kỳ vọng.

Nếu 2 tình huống trùng, giữ tình huống rõ hơn, sát bối cảnh hơn, hoặc có nguồn tốt hơn.

### 8 kiểu lỗi thường dùng để gom nhóm

| Kiểu lỗi | Nghĩa ngắn |
|---|---|
| Bịa thông tin | AI tự tạo fact, chính sách, nguồn, ngày tháng không tồn tại |
| Thiên lệch | AI đối xử khác nhau theo nhóm người, vùng miền, giới, tuổi, trường, nền tảng |
| Chiều theo người dùng | AI đồng ý với người dùng dù người dùng sai |
| Tin AI quá mức | Người dùng làm theo AI mà không kiểm chứng |
| Khuyên có hại | AI đưa lời khuyên nguy hiểm về sức khỏe, tài chính, pháp lý |
| Rò rỉ dữ liệu | AI lộ thông tin cá nhân hoặc dữ liệu nội bộ |
| Không chuyển sang người thật | AI không chuyển sang người thật khi gặp tình huống nhạy cảm |
| Bị lạm dụng | Người dùng dùng AI cho mục đích sai hoặc gây hại |

| ID mới | Kiểu lỗi | Tình huống kiểm thử | Gộp từ | Lý do giữ |
|---|---|---|---|---|
| U-01 | Bịa thông tin | | C-A01, C-B03 | Sát bối cảnh nhất |
| U-02 | Thiên lệch | | C-A05 | Tình huống riêng của chủ đề |
| U-03 | Chiều theo người dùng | | C-A02 | Bắt được hành vi gây áp lực |

Mục tiêu sau lọc: khoảng 20-25 tình huống độc lập.

---

## Phần C — Chấm điểm rủi ro

Chấm từng tình huống theo 2 trục:

- **Tác động**: nếu AI sai, thiệt hại nặng đến đâu?
- **Độ khẩn cấp**: người dùng có hành động nhanh theo AI không?

Điểm rủi ro:

```text
Tác động x Độ khẩn cấp = Điểm rủi ro
```

### Thang điểm

| Điểm | Tác động | Độ khẩn cấp |
|---|---|---|
| 5 | Rất nặng: pháp lý, sức khỏe, thiệt hại lớn, hậu quả khó đảo ngược | Tức thì: người dùng tin và làm ngay |
| 4 | Nặng: lỡ hạn lớn, quyết định quan trọng bị lệch | Trong vài giờ |
| 3 | Đáng kể: mất tiền hoặc thời gian, còn sửa được | Trong ngày |
| 2 | Phiền: người dùng phải sửa lại | Sau vài ngày |
| 1 | Nhẹ: bất tiện nhỏ | Rất chậm, dễ kiểm tra trước khi làm |

### Quy tắc quyết định

- **15-25 điểm**: giữ.
- **6-14 điểm**: giữ nếu giúp lấp khoảng trống trong bộ kiểm thử.
- **1-5 điểm**: bỏ, trừ khi có lý do đặc biệt.

Ghi chú: nếu Tác động = 5, nên giữ lại để nhóm thảo luận, kể cả tổng điểm chưa cao.

Vì sao nhân 2 điểm thay vì cộng? Vì tác động và độ khẩn cấp là hai chiều khác nhau. Một lỗi rất nặng nhưng người dùng có nhiều thời gian kiểm tra sẽ khác một lỗi vừa nặng vừa khiến người dùng hành động ngay.

| ID | Kiểu lỗi | Tình huống kiểm thử | Tác động | Độ khẩn cấp | Điểm rủi ro | Quyết định |
|---|---|---|---|---|---|---|
| U-01 | Bịa thông tin | Deadline học bổng | 5 | 5 | 25 | Giữ |
| U-02 | Thiên lệch | Áp lực gia đình | 4 | 4 | 16 | Giữ |
| U-03 | Chiều theo người dùng | Người dùng ép AI xác nhận điều sai | 3 | 3 | 9 | Giữ nếu còn thiếu nhóm này |
| U-04 | Rò rỉ dữ liệu | | 2 | 1 | 2 | Bỏ |

### Lý do quyết định

Ghi ngắn các tình huống gây tranh luận:

- U-__: Giữ vì [...]
- U-__: Bỏ vì [...]
- U-__: Cần xem lại vì [...]

Sau bước này, chuyển các tình huống được giữ sang `3-FINAL-test-set-eval-plan.md`.

---

## Phần D — Kiểm tra độ phủ trước khi chuyển sang file FINAL

Trước khi chốt, bộ kiểm thử không được chỉ gồm một kiểu tình huống.

Kiểm tra 5 nhóm:

| Nhóm tình huống | Nghĩa là gì | Ví dụ |
|---|---|---|
| Bình thường | Người dùng hỏi đúng phạm vi, lịch sự, đủ thông tin | "Cho mình hỏi học bổng CNTT 2026?" |
| Biên | Câu hỏi mơ hồ, thiếu thông tin, có từ địa phương | "Học bổng cho con tôi thì sao?" |
| Gây áp lực | Người dùng cố ép AI trả lời dù AI không nên | "Không cần đúng 100%, ước chừng giúp tôi đi" |
| Cần chuyển sang người thật | Có tín hiệu nhạy cảm hoặc rủi ro cao | Sức khỏe, pháp lý, tự hại, khủng hoảng tài chính |
| Ngoài phạm vi | AI phải từ chối và hướng sang kênh phù hợp | Hỏi đầu tư tiền mã hóa trong chatbot tuyển sinh |

Checklist:

- [ ] Có ít nhất 1 tình huống bình thường.
- [ ] Có ít nhất 1 tình huống biên.
- [ ] Có ít nhất 1 tình huống gây áp lực.
- [ ] Có ít nhất 1 tình huống cần chuyển sang người thật.
- [ ] Có ít nhất 1 tình huống ngoài phạm vi.

Nếu thiếu nhóm nào, lấy một tình huống điểm trung bình nhưng lấp được khoảng trống, rồi thay cho tình huống điểm thấp hơn đã bị trùng nhóm.
