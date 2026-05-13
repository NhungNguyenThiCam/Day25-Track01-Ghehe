# Prompt tham khảo 1 — Tìm sự cố thật từ thế giới ngoài

**Dùng khi**: nhóm cần tìm sự cố AI thật để neo brainstorm, tránh bịa rủi ro "cho có".
**Công cụ gợi ý**: Claude Deep Research, ChatGPT Deep Research, Perplexity Pro, Gemini Deep Research, hoặc tìm web thủ công.
**Lưu kết quả vào**: `worksheet/01-test-set-review/1-diverge.md` Phần A
**Thời gian**: 20–30 phút

---

## Trước khi vào prompt — 5 câu hỏi nhóm tự trả lời

Mục tiêu: **neo nhóm vào bối cảnh thật**. Tránh tìm case generic kiểu *"AI hallucinate"* — case đó có ở khắp nơi, không giúp ích test set track cụ thể của nhóm.

1. **Sản phẩm + AI đang làm gì cụ thể?** Vd: *"Chatbot tư vấn tuyển sinh, dùng LLM trả lời câu hỏi học sinh về ngành học và học bổng."*
2. **Ai dùng + dùng khi nào + trạng thái họ thế nào?** Vd: *"Học sinh cấp 3 + phụ huynh, dùng đêm 22:00, đang lo lắng cận deadline."*
3. **Rủi ro NẶNG nhất là gì?** Tài chính (mất tiền) / sai quyết định nghề nghiệp / lỡ deadline lớn / sức khoẻ tinh thần / pháp lý?
4. **Loại lỗi nào "đắt" nhất với sản phẩm?** Bịa data / trả lời quá tự tin / không escalate khi nên / leak privacy?
5. **Bối cảnh nào CHỈ track mình có** mà benchmark global không test? Vd VN-specific: học bổng dân tộc thiểu số, áp lực gia đình, hệ thống xét tuyển 2 khối.

> **Cảnh báo**: nếu nhóm trả lời câu 5 ngắn nhất, đó là dấu hiệu nhóm chưa hiểu sâu bối cảnh. **Phải fill 5 câu trước khi prompt** — không thì AI trả về case generic.

---

## Prompt tham khảo (paste sau `00-context.md`)

```text
Bạn là researcher chuyên về AI safety incidents. Dựa trên BỐI CẢNH SẢN PHẨM ở trên (00-context.md),
giúp nhóm tôi tìm các sự cố AI thật có liên quan để học và phòng tránh.

Yêu cầu tìm theo 4 hướng (4 lens):

LENS 1 — Cùng ngành (same industry):
- Sự cố AI trong [tên ngành: tuyển sinh / y tế / ngân hàng / ...] trong 5 năm qua
- Ưu tiên case có lawsuit, regulatory action, public apology

LENS 2 — Cùng kiểu lỗi (same failure mode):
- Sự cố ở ngành KHÁC nhưng cùng pattern (vd: AI bịa policy, AI thiên kiến, AI miss escalation)
- Ưu tiên case có root cause analysis công khai

LENS 3 — Cùng nhóm người dùng dễ tổn thương (similar vulnerable population):
- Người dùng có context tương tự (sinh viên cận deadline, bệnh nhân mất ngủ, người vay nợ)
- Ưu tiên case mà user vulnerability là nguyên nhân chính harm

LENS 4 — Đặc thù bối cảnh VN (Vietnam-specific):
- Sự cố tại VN hoặc với user VN
- Hoặc sự cố ở thị trường Đông Á có pattern văn hoá tương tự

Với MỖI sự cố, ghi:
- ID + Tổ chức / sản phẩm
- Ngày xảy ra
- Mô tả 2-3 câu
- Hậu quả định lượng (tiền, người bị ảnh hưởng, pháp lý)
- Vì sao liên quan đến bối cảnh nhóm tôi (1 câu)
- Nguồn primary (URL) + nguồn phụ (URL)
- Mức tin cậy: ✅ verified (≥2 nguồn primary) / ⚠️ partial (1 nguồn) / ❌ unverified

Yêu cầu CHẤT LƯỢNG nguồn:
- Ưu tiên primary: hồ sơ toà án (CanLII, CourtListener),
  official statement (company blog, gov report),
  tier-1 journalism (Reuters, NYT, BBC, WaPo, FT).
- KHÔNG dùng Medium, LinkedIn, Twitter làm primary source.
- Nếu chưa verify được, GHI RÕ "chưa kiểm chứng — cần fact-check".

Yêu cầu PHẢN BIỆN:
- Sau khi liệt kê, chọn ra 3 sự cố sát nhất với bối cảnh nhóm tôi.
- Với mỗi sự cố chọn, viết:
  - "Vì sao đây là priority case cho test set của tôi"
  - "Nếu chúng tôi KHÔNG học từ case này, sẽ vấp phải scenario nào trong sản phẩm?"
- Cuối cùng: liệt kê 1-2 sự cố mà bạn KHÔNG dám claim, vì nguồn yếu — để nhóm tự verify.
```

---

## Iterate — đẩy AI sâu hơn nếu output chưa đủ

### Khi AI trả case quá nổi tiếng

Nếu AI chỉ đưa Air Canada, Tay, GPT lawyer — case ai cũng biết. Đẩy thêm:

```text
3 case bạn vừa đưa quá nổi tiếng — đội đối thủ chắc chắn cũng dùng.

Tìm thêm 3 case ÍT NỔI BẬT hơn nhưng vẫn có nguồn verify, liên quan đến:
- Track [...] cụ thể của tôi
- Hệ thống pháp lý / giáo dục / y tế Việt Nam hoặc Đông Á
- Năm 2024-2025 (mới nhất)

Đặc biệt ưu tiên: Reddit threads có công khai verify, Hacker News discussions có source,
arxiv papers có case study, regulatory filings từ EU/UK/Canada/Australia.
```

### Khi muốn case adversarial (kẻ tấn công thật) thay vì user nhầm

```text
Trong các case bạn vừa đưa, case nào KẺ TẤN CÔNG (không phải user lành) lợi dụng?

Tách rõ:
- Case "user nhầm lẫn" (user không có ý xấu, AI vẫn fail)
- Case "user cố tình bẻ AI" (jailbreak, prompt injection, social engineering AI)

Với case "kẻ tấn công", mô tả:
- Ai (motive của họ)
- Cách họ exploit (technique cụ thể)
- AI lẽ ra nên phòng thủ thế nào
```

### Khi muốn nhìn case từ góc nạn nhân (counter-perspective)

```text
3 case bạn vừa đưa đa số nhìn từ góc COMPANY (Air Canada thua kiện, OpenAI rollback).

Đảo góc nhìn: kể lại 1-2 case từ góc NẠN NHÂN cụ thể.
- Họ là ai (background, profile)?
- Họ đã làm gì trước khi gặp AI (mức độ tin AI)?
- Sau khi AI fail, life họ thay đổi thế nào (financial, mental, legal)?
- Họ có recourse nào không? Có recover được không?

Mục đích: hiểu severity thật từ góc human cost, không chỉ company liability.
```

---

## Phản biện sau khi có output — 5 câu nhóm tự hỏi

Trước khi paste vào `1-diverge.md`, nhóm rà soát:

1. **Source check**: Mỗi case có URL primary không? Click URL có mở được không? Cross-check 2 nguồn cho case nghiêm trọng chưa?
2. **Relevance check**: Case này áp dụng vào track mình thế nào? Nếu không articulate được trong 1 câu → drop.
3. **Diversity check**: 3 case có cover 3-4 lens khác nhau không? Tránh 5 case đều là *"hallucination chatbot"*.
4. **Novelty check**: Case có quá nổi tiếng không? (Air Canada, Tay, GPT lawyer — ai cũng biết). Cần ít nhất **1 case ít phổ biến nhưng đắt**.
5. **Action check**: Sau khi đọc case, mình biết PHẢI test cái gì cụ thể trong sản phẩm chưa? Nếu vẫn mơ hồ → đào sâu thêm.

---

## Ví dụ tốt vs ví dụ chưa tốt

### ❌ Chưa tốt

> *"AI hallucinate. Vd: ChatGPT hallucinate court cases."*

Vấn đề: không cite source, generic, không liên quan track cụ thể, không actionable.

### ✅ Tốt

> **Case A1 — Air Canada chatbot bereavement fare lawsuit (11/2023)**
>
> - **Nguồn**: Moffatt v. Air Canada, 2024 BCCRT 149 — [CanLII](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html). Cross-check: [BBC Travel](https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know).
> - **Mô tả**: User hỏi chatbot Air Canada về policy giảm giá vé tang lễ. Chatbot bịa exception không tồn tại trong policy thật. User mua vé theo info AI, sau đó Air Canada từ chối refund.
> - **Hậu quả**: Tribunal Canada phán Air Canada thua, phải bồi thường + tiền lệ pháp lý *"công ty chịu trách nhiệm cho chatbot output, không thể disclaim"*.
> - **Liên quan track tôi (Admissions)**: cùng pattern — chatbot bịa policy. Học bổng / deadline / yêu cầu hồ sơ là policy. Nếu chatbot bịa, sinh viên action theo → trường có thể bị kiện.
> - **Test case rút ra**: *"User hỏi exception cho học bổng [X]"* → chatbot phải refuse + cite source chính thức + escalate counselor. Không bao giờ tự bịa exception.
> - **Mức tin cậy**: ✅ verified (court ruling + BBC cross-check).

Khác biệt: cite source primary, articulate relevance 1 câu, rút ra test case cụ thể action được.

---

## Anti-pattern khi prompt — tránh

| ❌ Đừng làm | ✅ Nên làm |
|---|---|
| Prompt ngắn, không paste context | Paste `00-context.md` đầy đủ, fill 5 câu self-prep trước |
| Tin AI cite blind | Click TỪNG URL, verify accessible + accurate |
| Stop sau 3 case đầu | Iterate 2-3 lần với các prompt push deeper |
| Chỉ chọn case nổi tiếng | Mix: 1 nổi tiếng + 2 ít phổ biến, đều có nguồn |
| Không articulate relevance | Mỗi case có 1 câu *"vì sao liên quan track mình"* |
| Drop case *"chưa kiểm chứng"* silent | Tag `[UNVERIFIED]` rõ, đừng giấu |
| 5 case cùng kiểu lỗi | Spread 3-4 lens (industry / failure mode / user / VN-specific) |

---

## Format save vào `1-diverge.md` Phần A

```markdown
## Phần A — Sự cố thật (Deep Research)

### Case A1 — [Tên ngắn, vd: Air Canada bereavement fare]
- **Ngày**: 11/2023 (incident) → 2/2024 (tribunal ruling)
- **Tổ chức**: Air Canada
- **Mô tả**: [2-3 câu]
- **Hậu quả**: [định lượng — pháp lý / tiền / scale]
- **Liên quan track tôi**: [1 câu]
- **Test case rút ra**: [câu cụ thể có thể test ngay]
- **Nguồn**: [URL primary] + [URL phụ]
- **Mức tin cậy**: ✅ / ⚠️ / ❌

### Case A2 — ...

### Case A3 — ...
```

---

## Câu hỏi mở rộng — nâng cao phản biện (optional, nhóm muốn đi sâu)

Nếu nhóm còn thời gian, dùng prompt sau để nhìn case **đa chiều**:

```text
Với 3 case priority bạn vừa chọn, giúp tôi đặt 3 câu hỏi PHẢN BIỆN:

1. Steelman case "AI làm đúng, lỗi do user/process/data" — biện hộ cho AI từ góc nào?
2. Nếu nhóm tôi CHỈ học bài học UX (vd thêm disclaimer), case này có tránh được không?
   Hay cần fix tầng sâu hơn (data, prompt, escalation)?
3. Trong 5 năm tới, nếu LLM technology cải thiện 10x, case này có còn xảy ra không?
   Nếu vẫn xảy ra → root cause không phải technology, là design / governance / business model.

Trả lời 3 câu này cho mỗi case, để nhóm tôi không stop ở surface-level analysis.
```

3 câu hỏi này giúp nhóm tránh **"AI is the problem"** narrative đơn giản hoá. Thực tế thường phức tạp hơn — đan xen design, business model, governance.
