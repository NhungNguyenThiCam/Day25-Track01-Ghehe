# Prompt tham khảo 5a — Phác thảo giao diện bằng ASCII

**Dùng khi**: nhóm muốn demo Pack 1 UI/UX bằng khung chữ — nhanh, không cần design tool.
**Công cụ gợi ý**: Claude Sonnet/Opus, ChatGPT-4o (ASCII tốt nhất với model lớn).
**Lưu kết quả vào**: `worksheet/02-solution-design/artifact/1-uiux/demo.md`
**Thời gian**: 10–15 phút

---

## Trước khi vào prompt — 5 câu hỏi nhóm tự trả lời

ASCII sketch tốt = sketch có **state machine rõ**. Đừng vẽ 1 màn "happy path" rồi xong — UX defense in depth thể hiện ở **các trạng thái khác nhau**:

1. **Default state**: AI có data, trả lời được, user lành. Màn hình hiển thị gì?
2. **Uncertain state**: AI không chắc, confidence thấp. Cảnh báo hiện như thế nào? Nguồn được surface ra sao?
3. **No-data state**: AI không có nguồn để trả lời. Refuse message + escalation path?
4. **Pressure-trap state**: User ép AI bằng narrative ("Em nghe nói X..."). UI hiển thị gì để user không bị anchor vào narrative?
5. **Error / Escalation state**: User hỏi red-flag (tự tử, bạo lực). UI chuyển sang counselor channel thế nào?

> **Cảnh báo**: nếu nhóm chỉ vẽ 1 state (default) → demo không cho thấy Defense in Depth. Vẽ ÍT NHẤT 3 states (default + uncertain + no-data).

---

## Prompt chính (paste sau `00-context.md` + Pack 1 card.md)

```text
Bạn là UX designer chuyên về AI safety patterns. Dựa trên BỐI CẢNH SẢN PHẨM và PACK 1 UI/UX SOLUTION CARD ở trên,
phác thảo demo ASCII cho 3-4 states khác nhau.

YÊU CẦU 3-4 STATES CỤ THỂ:

State 1 — DEFAULT (AI có data, confidence cao):
- AI trả lời đầy đủ
- Badge "Verified từ [source]" hoặc confidence indicator cao
- Nút "Mở văn bản gốc" / "Source" rõ
- Nút escalate vẫn có (nhưng không prominent)

State 2 — UNCERTAIN (AI có data nhưng confidence trung bình):
- AI trả lời nhưng wording cautious ("Theo thông tin năm trước...")
- Badge "Partial verification" hoặc confidence indicator vừa
- Nút "Mở văn bản gốc" + nút "Verify với counselor" cùng prominent
- Disclaimer wording rõ uncertainty

State 3 — NO DATA / REFUSE:
- AI không trả lời (refuse explicit, không bịa)
- Wording: "Tôi chưa có thông tin được xác minh về [topic]"
- Escalation path prominent (1 click → counselor / hotline)
- Suggested next step (vd "Bạn có thể check tại [URL]")

State 4 — ESCALATION / RED-FLAG (optional, cho case nhạy cảm):
- User mention red-flag (tự tử, bạo lực, harm)
- AI refuse + show hotline immediately
- Background color change (vd subtle red border)
- Không có "try again" — chuyển counselor

VỚI MỖI STATE, ghi:

```
╔═══════════════ State [N] ═══════════════╗
║ [ASCII layout: 30-40 chars wide]         ║
║                                          ║
║ - User message visible at top            ║
║ - AI response in middle                  ║
║ - Badges/confidence indicators           ║
║ - Action buttons at bottom               ║
║ - Annotations bên ngoài giải thích       ║
╚══════════════════════════════════════════╝
```

Sau mỗi state, ghi 2-3 annotations:
- Component nào quan trọng nhất cho state này
- Affordance nào (button / link) phải prominent
- Edge case: nếu user ignore badge, hệ thống có safeguard gì?

YÊU CẦU PHẢN BIỆN:
- Sau 3-4 states, đánh dấu state nào DIFFICULT to verify trong demo (vd cần animation, cần A/B test với user thật).
- Đề xuất 2-3 user research questions để verify design (vd "User có nhìn thấy badge không? Click rate vào 'Verify với counselor'?").
```

---

## Iterate — đẩy AI sâu hơn nếu output chưa đủ

### Khi sketch chỉ có 1 state default

```text
Sketch hiện tại chỉ vẽ default state — không cho thấy Defense in Depth.

Vẽ thêm 2 states critical:
1. State NO-DATA: AI refuse explicit, escalate prominent. UI khác gì so với default?
2. State PRESSURE-TRAP: user nói "Em nghe nói deadline 30/3, đúng không?" — UI hiển thị gì để user không bị anchor vào narrative sai?

Mỗi state PHẢI khác visually (color, layout, wording) để user nhận thức.
```

### Khi badge/disclosure thiếu accessibility

```text
Sketch hiện tại có badge "Verified" visual. Nhưng:

1. Screen reader user không "thấy" badge — cần ARIA label gì?
2. Colorblind user không phân biệt badge xanh/đỏ — cần icon + text fallback?
3. User non-native VN không hiểu "Verified" — wording đơn giản hơn (vd "Đã kiểm tra")?

Re-sketch với 3 accessibility considerations trên. Show wording cuối cùng cho mỗi badge state.
```

### Khi muốn user testing trong design

```text
Sketch demo có vẻ OK trên giấy, nhưng demo cần verify với user thật.

Đề xuất 3 user testing scenarios:
1. Scenario A: user vội (cận deadline). Họ có notice badge không?
2. Scenario B: user pressure-trap ("Em nghe nói..."). Họ có tin AI hay verify?
3. Scenario C: user red-flag (depression). Họ có click escalation không?

Mỗi scenario, ghi:
- Recruit profile (ai test)
- Task (làm gì trong app)
- Metric (đo cái gì — click rate, time-to-decision, post-task survey)
- Pass criteria (acceptable threshold)
```

---

## Phản biện sau khi có output — 5 câu nhóm tự hỏi

Trước khi save vào `demo.md`:

1. **State coverage**: Có 3-4 states không? Hay chỉ 1 default + 1 "error"?
2. **Affordance clarity**: Mỗi state, action nào prominent nhất? Có conflict không (vd 2 button cùng prominent gây phân tâm)?
3. **Defense layered**: UX có catch user error / pressure-trap không? Hay chỉ display thông tin?
4. **Accessibility**: Screen reader, colorblind, non-native VN — có handle không?
5. **Testable**: Demo này có thể user test được không? Hay chỉ là "đẹp on paper"?

---

## Ví dụ tốt vs ví dụ chưa tốt

### ❌ Chưa tốt — chỉ 1 state, không annotation

```
╔══ AI response ══╗
║ Deadline: 15/04 ║
║ Verified ✓      ║
╚═════════════════╝
```

Vấn đề: chỉ 1 state, không có pressure-trap handling, không có refuse path, không có escalation.

### ✅ Tốt — 3 states + annotations

```
State 1 — DEFAULT (AI có data + confidence cao)
╔══════ AI Response ══════╗
║ Hạn HB CNTT: 15/04/2026 ║
║                          ║
║ ✓ Verified từ            ║
║   admissions.edu         ║
║ ────────────────────     ║
║ [Mở văn bản gốc]         ║
║ [Verify với counselor]   ║
╚══════════════════════════╝

Annotations:
- Badge "Verified" với link inline tới source (không phải mở tab mới — distraction)
- Nút "Verify counselor" vẫn có dù confidence cao — Defense in Depth
- Tiếng Việt thuần, không "Source"/"Verify"

State 2 — UNCERTAIN (data partial, confidence vừa)
╔══════ AI Response ══════╗
║ Hạn HB CNTT theo dữ liệu║
║ 2025: 15/04             ║
║                          ║
║ ⚠ Chưa cập nhật 2026     ║
║ ──────────────────────  ║
║ ⚠ KIỂM TRA TRANG CHÍNH  ║
║   THỨC TRƯỚC KHI NỘP    ║
║                          ║
║ [Mở admissions.edu]      ║
║ [Verify với counselor]   ║
╚══════════════════════════╝

Annotations:
- Wording "theo dữ liệu 2025" — explicit về age of data
- Warning ⚠ prominent với uppercase
- 2 actions cùng prominent (user chọn)

State 3 — NO DATA / REFUSE
╔══════ AI Response ══════╗
║ Tôi chưa có thông tin    ║
║ được xác minh về deadline║
║ học bổng CNTT 2026.      ║
║                          ║
║ Bạn có thể check tại:    ║
║ → admissions.edu/cntt    ║
║                          ║
║ Hoặc chat với counselor: ║
║ [Chat ngay] [Đặt lịch]   ║
╚══════════════════════════╝

Annotations:
- AI explicit refuse — không bịa
- Suggested next step concrete (URL + counselor)
- 2 escalation options (chat ngay vs đặt lịch — fit user urgency)
```

Khác biệt: 3 states distinct, annotations giải thích design intent, accessibility considerations.

---

## Anti-pattern khi prompt — tránh

| ❌ Đừng làm | ✅ Nên làm |
|---|---|
| Sketch 1 state default | Sketch ≥ 3 states: default + uncertain + no-data |
| Badge generic "AI có thể sai" | Specific badge: "Verified từ [source]" / "Partial verification" / "Chưa xác minh" |
| Wording English ("Verify", "Source") | Thuần Việt: "Kiểm tra với người thật", "Mở văn bản gốc" |
| Đặt 5 button cùng prominent | 1-2 button prominent, còn lại secondary |
| Skip annotations | Mỗi state có 2-3 annotation giải thích design intent |
| Demo "đẹp on paper", không testable | Demo kèm 3 user testing scenarios |

---

## Format save vào `demo.md`

```markdown
# Pack 1 — UX/UI Demo (Track [N])

## State 1 — DEFAULT

[ASCII sketch]

**Annotations**:
- ...
- ...

## State 2 — UNCERTAIN

[ASCII sketch]

**Annotations**:
- ...
- ...

## State 3 — NO DATA / REFUSE

[ASCII sketch]

**Annotations**:
- ...
- ...

## (Optional) State 4 — ESCALATION RED-FLAG

[ASCII sketch + special handling]

## User testing plan

| Scenario | User profile | Task | Pass criteria |
|---|---|---|---|
| A — Pressure-trap | User vội, cận deadline | Hỏi AI deadline | Notice badge → click verify |
| B — No data | User hỏi info AI không có | ... | Click escalation < 30s |
| C — Red-flag | User mention depression | ... | Reach counselor < 1 click |
```

---

## Câu hỏi mở rộng phản biện (optional)

```text
Sketch 3 states của tôi. Giúp tôi phản biện:

1. **Bypass test**: User cố tình ignore badge "Verified" — Pack 2 (Prompt) + Pack 3 (Architecture) có catch không?
2. **Cognitive load**: 3 states có làm UI quá phức tạp không? User mới có nhận diện được state mình đang ở?
3. **Cultural fit**: Wording tiếng Việt có natural không? Có phải dịch word-by-word từ English UX patterns?

Đặc biệt câu 3: review wording, suggest phrasing thuần Việt + natural.
```
