# Prompt tham khảo 4 — 3 hướng giải pháp Defense in Depth

**Dùng khi**: nhóm đã chọn ca tệ nhất từ Bài 1, cần brainstorm 3 hướng giải pháp khác layer (UX / Prompt / Architecture).
**Công cụ gợi ý**: Claude Sonnet/Opus, ChatGPT-4o, Gemini 1.5 Pro.
**Lưu kết quả vào**: `worksheet/02-solution-design/1-map-and-format.md` Phần C
**Thời gian**: 15–20 phút

---

## Trước khi vào prompt — 5 câu hỏi nhóm tự trả lời

3 hướng giải pháp **không phải** 3 lời giải khác nhau cho cùng vấn đề. Là **3 tầng phòng vệ độc lập cộng dồn** (Defense in Depth). Cách brainstorm bị 4 anti-pattern thường gặp:

1. **3 packs đều là UX patch** (vì designer dễ nghĩ tới UX)
2. **3 packs phụ thuộc nhau** (Pack 2 cần Pack 1 hoạt động → không độc lập)
3. **Chỉ cover Disclose, miss Prevent/Catch/Recover** (banner *"AI có thể sai"* không fix root cause)
4. **Side effect không multi-stakeholder** (chỉ nghĩ developer, miss user/legal/ops)

Trước khi prompt AI, nhóm tự reflect:

1. **Root cause của ca tệ nhất ở tầng nào?** Data (thiếu nguồn) / Model (AI đoán bừa) / UX (user tin quá mức) / Process (thiếu escalation) / Monitoring (lỗi lặp sau launch)?
2. **4 verbs nào bộ giải pháp PHẢI cover?** Prevent (chặn) / Catch (phát hiện) / Recover (khắc phục) / Disclose (báo user)?
3. **Severity = bao nhiêu?** Score ≥ 15 → cần ≥ 3 layers stack. Score 6-14 → 2 layers đủ. Score < 6 → 1 layer.
4. **3 packs phải độc lập** — nếu 1 pack fail, 2 pack khác vẫn cover. Pack nào của nhóm phụ thuộc pack khác?
5. **Audience cuối cùng là ai?** Designer (build UX) / Backend dev (build prompt + RAG) / PM (own process)? Format mỗi pack phải khớp audience.

---

## Prompt chính (paste sau ca tệ nhất + Risk Score)

```text
Bạn là senior AI product architect. Dựa trên CA TỆ NHẤT dưới đây (đã chọn từ Bài 1) và bối cảnh sản phẩm,
giúp nhóm tôi brainstorm 3 hướng giải pháp theo Defense in Depth.

CA TỆ NHẤT:
[paste case từ 3-FINAL-test-set-eval-plan.md]
- User prompt: "[...]"
- Expected AI failure: [...]
- Impact: [1-5] · Urgency: [1-5] · Score: [...]
- Root cause hypothesis: [thiếu nguồn / AI đoán bừa / user tin quá mức / case nhạy cảm]

NGUYÊN TẮC THIẾT KẾ:
- Failure ở layer nào → fix ở layer đó. Đừng patch UX cho lỗi gốc Data.
- Mỗi solution cover ≥ 1 verb (Prevent / Catch / Recover / Disclose).
- High severity (Score ≥ 15) = stack ≥ 3 verbs.
- 3 packs PHẢI độc lập — 1 pack fail, 2 pack khác vẫn cover.

YÊU CẦU 3 HƯỚNG GIẢI PHÁP:

PACK 1 — UX/UI Solution (Layer 3):
- Mục tiêu: user trust mis-calibration. Cần Disclose + Catch user error.
- Khi nào dùng: root cause = "user tin AI quá mức" hoặc cần đảm bảo user thấy uncertainty.
- Components cần có:
  - Disclosure: badge / wording / confidence indicator
  - Source attribution: link nguồn, "Verified by [X]"
  - Escalation affordance: nút "Verify với người thật" / "Mở văn bản gốc"
  - Loading + error states: skeleton, error message rõ
- Output: card.md + demo (sketch / Excalidraw / vibe-code / HTML)

PACK 2 — Prompt Engineering Solution (Layer 2):
- Mục tiêu: model defaulting to confident guess. Cần Prevent + Refuse.
- Khi nào dùng: root cause = "AI đoán bừa" hoặc cần enforce refuse-when-unknown.
- Components cần có:
  - Refuse rule explicit: "Never state X without Y"
  - Cite-ground requirement: "Mọi response về [topic] PHẢI cite URL"
  - Few-shot examples: 3 cases cover refuse / cite / escalate
  - OOS handling: red-flag topics → escalate (mental health, medical, legal)
- Output: card.md + demo.md (system prompt text + 3 few-shot)

PACK 3 — Architecture / RAG Solution (Layer 1):
- Mục tiêu: thiếu nguồn data đúng. Cần Prevent (Ground).
- Khi nào dùng: root cause = "thiếu nguồn" hoặc model dùng data outdated.
- Components cần có:
  - Data source chính: RAG hit official policy / database
  - Cache strategy: TTL hợp lý (1h, 1 day)
  - Fallback path: API timeout / null → refuse + escalate
  - Monitoring + audit log: log mọi query để detect drift post-launch
- Output: card.md + demo.md (ASCII / Mermaid diagram + component spec)

VỚI MỖI PACK, GHI:
1. **Solution summary** (1 đoạn): pack làm gì cụ thể
2. **Layer + Why fits**: tại sao layer này match root cause
3. **Concrete artifact**: components cụ thể (3-5 bullet) + format demo
4. **Side effect + mitigation** (multi-stakeholder):
   - User: trade-off UX (cluttered? friction? confused?)
   - Operations: latency, cost, scalability
   - Legal / compliance: data privacy, accessibility
   - Engineering: complexity, maintenance burden
5. **Verbs covered**: Prevent ✓ / Catch ✓ / Recover ✓ / Disclose ✓
6. **Failure mode của solution**: solution này fail trong tình huống nào? (Tránh false confidence)

PHẢN BIỆN với chính output:
- 3 packs có thực sự độc lập không? Nếu Pack 2 cần Pack 1 hoạt động → flag.
- 3 packs cộng dồn cover ĐỦ 4 verbs chưa? Nếu thiếu Recover → đề xuất Pack 4 hoặc thêm vào Pack 1.
- Side effect nào CHƯA addressed multi-stakeholder?

ĐỀ XUẤT THỨ TỰ BUILD:
Nhóm chỉ có 35' build 3 packs PARALLEL. Đề xuất pack nào BUILD TRƯỚC (chia thành viên A), pack nào BUILD SAU (thành viên B + C). Justify thứ tự (vd: Pack 3 Architecture cần làm trước để Pack 1 UX biết data source nào available).
```

---

## Iterate — đẩy AI sâu hơn nếu output chưa đủ

### Khi 3 packs đều là UX patch (anti-pattern)

```text
3 packs bạn vừa đưa đều thiên về UX (badge, warning, disclosure). Đây là anti-pattern Defense in Depth — chỉ cover Disclose, miss Prevent/Catch/Recover.

Re-design với constraint:
- Pack 1: PHẢI là UX/UI (Layer 3) — Disclose primary
- Pack 2: PHẢI là Prompt Engineering (Layer 2) — Prevent/Refuse primary
- Pack 3: PHẢI là Architecture/RAG (Layer 1) — Prevent/Ground primary

3 packs MUST khác layer. Không bao giờ 2 packs cùng UX hoặc cùng Prompt.

Re-suggest 3 packs với constraint mới.
```

### Khi solution chỉ cover Disclose, miss Recover

```text
Trong 3 packs, không có pack nào cover RECOVER verb (xử lý khi failure xảy ra).
3 packs cover: Prevent (Pack 2, 3) + Disclose (Pack 1) + Catch (Pack 3 monitoring).
THIẾU Recover.

Recover example trong context [track]:
- Easy escalation to counselor (1 click)
- Undo button / refund flow
- Human-in-loop trigger khi AI confidence < 0.7
- Fallback message "Tôi không chắc, đang chuyển bạn tới [counselor / hotline / human agent]"

Đề xuất:
A) Thêm Recover component vào 1 trong 3 packs hiện tại (vd thêm escalate button vào Pack 1)
B) Tạo Pack 4 dedicated cho Approval Flow (Layer 7)

Recommend nhóm tôi nên đi hướng A hay B + lý do.
```

### Khi side effect không multi-stakeholder

```text
Side effect của Pack 1 hiện tại chỉ nói: "Badge có thể bị ignore".
Đây là góc nhìn USER. Còn thiếu:

1. **Operations**: badge thêm 200ms latency / query. Scalability impact?
2. **Engineering**: maintenance burden khi update policy source — ai own?
3. **Legal**: badge "Verified" có create implicit warranty không? Nếu badge sai → liability?
4. **Customer support**: badge mới → CS team có training cập nhật? Volume hỏi tăng không?
5. **Accessibility**: badge có ARIA label cho screen reader user không?
6. **Internationalization**: nếu sản phẩm scale ra ASEAN, badge text Vietnamese hardcoded?

Re-write side effects của Pack 1 với 6 góc nhìn trên. Mitigation cụ thể cho mỗi.
```

---

## Phản biện sau khi có output — 5 câu nhóm tự hỏi

Trước khi save vào `1-map-and-format.md`:

1. **Layer-correct check**: Mỗi pack có **layer-correct** không? Pack 1 = UX, Pack 2 = Prompt, Pack 3 = Architecture. KHÔNG mix.
2. **Independence check**: 3 packs có **độc lập** không? Nếu 1 fail, 2 pack khác vẫn cover. Test: tắt giả lập Pack 2 → Pack 1 + 3 còn handle case không?
3. **4 verbs coverage**: Prevent / Catch / Recover / Disclose — ≥ 1 verb / pack, tổng cộng cover **cả 4** trong 3 packs?
4. **Side effect honesty**: Có "free lunch solution" nào không (không có downside)? Suspect — re-think.
5. **Failure mode của solution**: Mỗi pack fail trong tình huống nào? Pack nào fail catastrophic, pack nào fail graceful?

---

## Ví dụ tốt vs ví dụ chưa tốt

### ❌ Chưa tốt — 3 packs đều UX

> Pack 1: Badge "Verified". Pack 2: Warning popup. Pack 3: Disclosure footer.

Vấn đề: 3 packs cùng layer UX, cùng verb Disclose. Defense in Depth không có vì cùng failure mode = cùng failure cause.

### ✅ Tốt — 3 layers khác nhau, cover 4 verbs

> **Pack 1 (UX, Layer 3)**: Badge "Verified từ admissions.edu" + nút "Mở văn bản gốc" + nút "Chat counselor". → Disclose + Recover.
>
> **Pack 2 (Prompt, Layer 2)**: System prompt explicit "Never state deadline without citing source URL. If no source → respond 'Tôi chưa có thông tin xác minh, đang chuyển counselor'". + 3 few-shot examples cho Refuse / Cite / Escalate. → Prevent + Refuse.
>
> **Pack 3 (Architecture, Layer 1)**: RAG service query admissions API mỗi response chứa keyword "deadline / scholarship". Cache 1 day. Fallback: API null → AI refuse + escalate counselor (SLA 4h). Monitoring: log mọi query + alert nếu cite source 404. → Prevent (Ground) + Catch (Monitor).
>
> **4 verbs cộng dồn**: ✓ Prevent (Pack 2 + 3) · ✓ Catch (Pack 3) · ✓ Recover (Pack 1 escalate) · ✓ Disclose (Pack 1 badge)
>
> **Independence test**: Pack 2 fail (drift system prompt) → Pack 3 RAG vẫn ground. Pack 3 fail (API down) → Pack 2 prompt vẫn enforce refuse + Pack 1 UX vẫn show "data not available". Pack 1 fail (user ignore badge) → Pack 2 + 3 vẫn prevent at backend. **3 packs thực sự độc lập**.

Khác biệt: layer-correct, verb-complete, side effect multi-stakeholder, independence verified.

---

## Anti-pattern khi prompt — tránh

| ❌ Đừng làm | ✅ Nên làm |
|---|---|
| Brainstorm "3 solutions" không constraint | Constraint: Pack 1 UX / Pack 2 Prompt / Pack 3 Architecture |
| Chỉ nghĩ Disclose ("thêm warning") | Force cover 4 verbs: Prevent + Catch + Recover + Disclose |
| 3 packs phụ thuộc nhau | Independence test: 1 pack fail, 2 pack khác vẫn cover |
| Side effect 1 chiều (chỉ user perspective) | 6 góc nhìn: user / ops / eng / legal / CS / accessibility |
| Format demo theo sở thích nhóm | Format theo audience: designer / dev / PM |
| Pack nào cũng cover mọi failure mode | Mỗi pack focus 1 strength, 3 packs combined → cover all |

---

## Format save vào `1-map-and-format.md`

```markdown
## Phần A — Map failure → tầng giải pháp

**Ca tệ nhất chọn**: [Case ID + tên]
- User prompt: "[...]"
- Impact: [1-5] · Urgency: [1-5] · Score: [...]
- Root cause: [hypothesis]
- Primary layer: [Data / Prompt / UX / Process / Monitoring]

## Phần B — Pick format mỗi pack

| Pack | Layer | Format chọn | Lý do |
|---|---|---|---|
| 1-uiux | Layer 3 | Sketch / Excalidraw / vibe-code | [...] |
| 2-prompt | Layer 2 | Markdown spec (system prompt + few-shot) | [...] |
| 3-architecture | Layer 1 | ASCII / Mermaid | [...] |

## Phần C — 3 Solution Picks

### Pack 1 — UX/UI
- **Solution summary**: ...
- **Verbs covered**: Disclose + (Recover)
- **Components**: ...
- **Side effect**: [multi-stakeholder]
- **Failure mode của solution**: ...

### Pack 2 — Prompt Engineering
[same structure]

### Pack 3 — Architecture / RAG
[same structure]

### Independence check
- Pack 2 fail → Pack [...] còn cover
- Pack 3 fail → Pack [...] còn cover
- Pack 1 fail → Pack [...] còn cover

### Verbs coverage matrix
| Verb | Pack 1 | Pack 2 | Pack 3 |
|---|---|---|---|
| Prevent | | ✓ | ✓ |
| Catch | | | ✓ |
| Recover | ✓ | | |
| Disclose | ✓ | | |

→ Build 3 packs PARALLEL → save vào `artifact/{1-uiux, 2-prompt, 3-architecture}/`
```

---

## Câu hỏi mở rộng phản biện (optional, đi sâu)

Nếu nhóm còn thời gian, prompt AI để stress-test 3 packs:

```text
3 packs giải pháp của tôi (paste). Giúp tôi phản biện 3 câu:

1. **Cost-benefit reality**: 3 packs cần effort bao nhiêu (dev hours / quarters)?
   Nếu công ty chỉ approve 1 pack → priority order là gì?
   Justify dựa trên Risk Reduction / Pack (effort vs impact).

2. **Counterfactual**: Nếu sản phẩm này đã có 2 năm production data,
   pack nào sẽ KHÔNG cần (đã handle bằng instinct), pack nào sẽ ESSENTIAL (lesson learned)?

3. **Adversarial review**: Kẻ tấn công sau khi đọc 3 packs này, sẽ bypass thế nào?
   Vd: bypass Pack 1 (ignore badge), bypass Pack 2 (jailbreak prompt), bypass Pack 3 (cache poisoning).
   Defense in Depth dùng tại đây: cần ≥ 2 layers fail đồng thời mới bypass full.
   Verify scenario: nếu attacker bypass được 1 layer, 2 layer còn lại có catch không?
```
