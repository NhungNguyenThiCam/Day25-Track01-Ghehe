# Prompt tham khảo 5e — Phác thảo kiến trúc dữ liệu bằng ASCII

**Dùng khi**: nhóm muốn demo Pack 3 (Architecture / RAG) bằng sơ đồ chữ — show data flow + fallback paths.
**Công cụ gợi ý**: Claude Sonnet/Opus, ChatGPT-4o.
**Lưu kết quả vào**: `worksheet/02-solution-design/artifact/3-architecture/demo.md`
**Thời gian**: 10–15 phút

---

## Trước khi vào prompt — 5 câu hỏi nhóm tự trả lời

Architecture diagram tốt = diagram show **data sources + fallback paths + observability**, không phải chỉ "RAG retrieve thông tin":

1. **Data sources**: AI lấy data từ đâu? Primary (admissions.edu API) / Secondary (Wikipedia) / Cached (Redis) / Embedded (vector DB)?
2. **Retrieval path**: Data flow đi qua bao nhiêu hops? Latency mỗi hop? Cost mỗi hop?
3. **Cache strategy**: TTL bao lâu? Invalidation khi nào? Stale data handling?
4. **Fallback paths**: API down, cache miss, embedding fail — system làm gì?
5. **Observability**: Monitoring metrics? Logs? Alerts? Audit trail cho compliance?

> **Cảnh báo**: nếu diagram chỉ "User → AI → Response", thiếu data layer → không thực sự là Architecture solution. Cần show ≥ 4 components + data flows.

---

## Prompt chính (paste sau `00-context.md` + Pack 3 card.md)

```text
Bạn là backend architect chuyên về RAG systems + AI safety. Dựa trên BỐI CẢNH và PACK 3 ARCHITECTURE/RAG card,
phác thảo sơ đồ ASCII show data flow + fallback paths + observability hooks.

YÊU CẦU SƠ ĐỒ:

1. ≥ 4 components:
   - User-facing API (chatbot endpoint)
   - Intent classifier (LLM hoặc rule-based)
   - RAG service (embedding + vector DB + retriever)
   - LLM service (OpenAI / Anthropic / Gemini)
   - Cache layer (Redis / in-memory)
   - Monitoring service (logs + metrics + alerts)

2. ≥ 3 data sources:
   - Primary: official API (admissions.edu) hoặc database
   - Secondary: vector DB indexed
   - Cache: Redis với TTL

3. ≥ 2 fallback paths:
   - Primary API down → cache fallback
   - Cache miss + API timeout → refuse with explicit message
   - LLM quota exhausted → static template response

4. ≥ 3 observability hooks:
   - Query log (input + intent + rag_hits + response)
   - Metric: rag_hit_rate, refuse_rate, escalation_count
   - Alert: rag_failure > 5% in 5min window

VÍ DỤ STRUCTURE:

```
                  ┌─────────────────────────┐
                  │      USER (Web/App)     │
                  └────────────┬────────────┘
                               │ HTTPS
                               ▼
            ┌──────────────────────────────────────┐
            │  CHATBOT API (gateway)               │
            │  - Rate limit: 10 req/min/user      │
            │  - Auth: token check                 │
            └──────────────────┬───────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────────┐
            │  INTENT CLASSIFIER (LLM-based)       │
            │  - Latency: ~200ms                   │
            │  - Output: in-scope/OOS/red-flag    │
            └──────────────────┬───────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
        in-scope            OOS               red-flag
            │                  │                  │
            ▼                  ▼                  ▼
   ┌─────────────┐      ┌───────────┐      ┌──────────────┐
   │RAG SERVICE  │      │REFUSE OOS │      │COUNSELOR     │
   │             │      └───────────┘      │CHANNEL       │
   │  ┌────────┐ │                          │              │
   │  │CACHE   │ │                          │+ hotline UI  │
   │  │Redis   │ │                          └──────────────┘
   │  │TTL 1d  │ │
   │  └───┬────┘ │
   │      │ miss │
   │      ▼      │
   │  ┌────────┐ │  fallback if API down
   │  │API     │ │  ────────────────────► [REFUSE no-source
   │  │admissi-│ │                          + suggest URL]
   │  │ons.edu │ │
   │  │ timeout│ │
   │  │ < 2s   │ │
   │  └───┬────┘ │
   │      │ hit  │
   │      ▼      │
   │  ┌────────┐ │
   │  │VECTOR  │ │
   │  │DB      │ │
   │  │embed + │ │
   │  │similar-│ │
   │  │ity > 75│ │
   │  └───┬────┘ │
   └──────┼──────┘
          │
          ▼
   ┌─────────────────────────────┐
   │ LLM SERVICE                 │
   │ + cite source explicit       │
   │ + confidence score (RAGAS)   │
   │ + fallback: cached template  │
   │   if quota exhausted         │
   └──────────────┬───────────────┘
                  │
                  ▼
   ┌─────────────────────────────┐
   │ OUTPUT FILTER                │
   │ - Strip PII                  │
   │ - Add badge based confidence │
   │ - Add citation links         │
   └──────────────┬───────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   [Send to UI]      [LOGS + METRICS]
                     - query, intent
                     - rag_hit_rate
                     - confidence_score
                     - response_latency
                          │
                          ▼
                     [MONITORING]
                     - Dashboard
                     - Alert: rag_fail > 5%
                     - Alert: confidence
                       trend down
```

VỚI MỖI COMPONENT, ghi:
- **Input/Output**: data flow vào/ra
- **Latency**: p50, p95
- **Cost**: per request hoặc per 1K requests
- **Failure mode**: component fail thì gì xảy ra
- **Fallback**: nếu fail, fallback đi đâu

YÊU CẦU PHẢN BIỆN:
- Đánh dấu 2 components là single-point-of-failure (SPOF)
- Đề xuất 2 metrics critical cho SLO (Service Level Objective)
```

---

## Iterate — đẩy AI sâu hơn

### Khi diagram thiếu fallback paths

```text
Architecture hiện tại không có fallback. Production sẽ break khi:
- admissions.edu API down (peak time, vendor incident)
- LLM API quota exhausted (cost spike, throttling)
- Cache miss + Redis cold start
- Vector DB index corrupted

Re-draw với fallback chain:
1. Primary path: Redis cache → admissions.edu API → vector DB → LLM
2. Fallback 1: Cache hit (stale acceptable) → serve cached + warn user "Data có thể cũ"
3. Fallback 2: API timeout > 2s → refuse + suggest URL
4. Fallback 3: LLM quota → static template "Đang quá tải, vui lòng thử lại sau"

Mỗi fallback có observability hook (log + metric + alert threshold).
```

### Khi observability sparse

```text
Diagram hiện tại có 1 monitoring node generic. Production cần observability rich:

1. **Metrics** (Prometheus-compatible):
   - `rag_request_total{status="hit|miss|timeout"}`
   - `llm_request_duration_seconds{percentile="p50|p95|p99"}`
   - `refuse_rate{reason="oos|no_source|red_flag"}`
   - `escalation_rate{type="red_flag|low_confidence"}`

2. **Logs** (structured JSON):
   - Per request: query, intent, sources, confidence, refuse_reason
   - Sampling: 10% normal, 100% refuses, 100% escalations

3. **Alerts**:
   - rag_miss_rate > 10% trong 5 phút
   - llm_latency p99 > 5s
   - refuse_rate > 30% (có thể model regression)
   - escalation_rate spike > 3x baseline

4. **Audit trail** (compliance):
   - All red-flag escalations logged 7 years (legal requirement)
   - PII handling per NĐ 13/2023

Re-draw với observability stack.
```

### Khi muốn architecture handle scale (1M users)

```text
Diagram hiện tại OK cho 1K users. Production scale 1M users cần:

1. **Load balancing**: chatbot API có N instances behind load balancer
2. **Database read replicas**: admissions.edu API hit replica, không master
3. **Vector DB sharding**: index quá lớn → shard by department/year
4. **Async escalation**: red-flag không block — queue + worker pool
5. **Circuit breaker**: nếu downstream fail > threshold, short-circuit để protect

Re-draw architecture với scale-out considerations + show capacity planning.
```

---

## Phản biện sau output — 5 câu nhóm tự hỏi

1. **Component count**: ≥ 4 components, ≥ 3 data sources?
2. **Fallback explicit**: ≥ 2 fallback paths với trigger condition rõ?
3. **Observability**: ≥ 3 hooks (logs + metrics + alerts)?
4. **SPOF identified**: Có component nào single-point-of-failure không? Mitigation?
5. **Latency budget**: Tổng latency p50 < 2s, p95 < 5s? User experience acceptable?

---

## Ví dụ tốt vs chưa tốt

### ❌ Chưa tốt — chỉ "User → AI"

```
User → AI → Response
```

Vấn đề: 0 data layer, 0 fallback, 0 observability.

### ✅ Tốt — full architecture với fallback + observability

```
┌──────────────────────────────────────────────────────┐
│                  USER LAYER                          │
│  Web/Mobile chatbot UI                               │
└──────────────────────┬───────────────────────────────┘
                       │ HTTPS + auth token
                       ▼
┌──────────────────────────────────────────────────────┐
│           API GATEWAY (Cloudflare Workers)           │
│  - Rate limit 10/min/user                            │
│  - DDoS protection                                   │
│  - Request log → Datadog                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│         INTENT CLASSIFIER (mini LLM)                 │
│  Latency p50: 200ms · p95: 400ms                     │
│  Cost: $0.0001/req                                   │
└────┬──────────────┬──────────────┬───────────────────┘
     │              │              │
     │ in-scope     │ OOS          │ red-flag
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐   ┌─────────────┐
│RAG SERVE │  │REFUSE OOS│   │COUNSELOR    │
│          │  │          │   │CHANNEL      │
│┌────────┐│  │Log: oos  │   │+ hotline    │
││Cache   ││  │count     │   │1800-599-920 │
││Redis   ││  └──────────┘   │+ SLA 5 min  │
││TTL 1d  ││                 │+ Log:       │
│└───┬────┘│                 │ red_flag++  │
│    │miss │                 └─────────────┘
│    ▼    │
│┌────────┐│ ──── API down/timeout ────►┌──────────────┐
││API     ││                            │REFUSE        │
││admissi-││                            │NO-SOURCE     │
││ons.edu ││                            │+ suggest URL │
││ <2s    ││                            │+ Log:        │
│└───┬────┘│                            │ refuse_no_src│
│    │hit  │                            └──────────────┘
│    ▼    │
│┌────────┐│
││VECTOR  ││ ──── similarity < 0.75 ────►(REFUSE NO-SOURCE)
││DB      ││
││Pinecone││
│└───┬────┘│
└────┼─────┘
     │
     ▼
┌──────────────────────────────────────────────────────┐
│              LLM SERVICE (Anthropic)                 │
│  Latency p50: 1s · p95: 2.5s                         │
│  Cost: $0.003/req                                    │
│  + System prompt: refuse rules + cite                │
│  + Few-shot examples                                 │
│  + Confidence score (RAGAS faithfulness)             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│               OUTPUT FILTER                          │
│  - Strip PII (regex + classifier)                    │
│  - Add badge based on confidence:                    │
│    ≥ 0.8 → ✓ Verified                                │
│    0.6-0.8 → ⚠ Partial                               │
│    < 0.6 → block, refuse                             │
│  - Add citation hyperlinks                           │
└──────────────────────┬───────────────────────────────┘
                       │
       ┌───────────────┼─────────────────┐
       ▼               ▼                 ▼
   [Send UI]    [LOGS Datadog]      [METRICS Prom]
                 query, intent,       rag_hit_rate
                 confidence,          llm_latency_p99
                 sources,             refuse_rate
                 user_id_hashed       escalation_rate
                       │                    │
                       └────────┬───────────┘
                                ▼
                         [DASHBOARD + ALERT]
                         - rag_miss > 10%/5min
                         - llm_p99 > 5s
                         - refuse_rate > 30%
                         - escalation 3x baseline
```

**Component table**:
| Component | Latency p50/p95 | Cost/req | Failure mode | Fallback |
|---|---|---|---|---|
| API Gateway | 50ms / 100ms | $0.0001 | DDoS attack | Cloudflare ratelimit |
| Intent Classifier | 200ms / 400ms | $0.0001 | LLM API down | Default conservative (treat as red-flag) |
| Cache (Redis) | 5ms / 20ms | negligible | Cold start | Skip, hit API |
| admissions.edu API | 300ms / 800ms | API quota | Timeout > 2s | Refuse no-source |
| Vector DB | 50ms / 150ms | $0.01/1K req | Index corruption | Rebuild from cache |
| LLM Service | 1s / 2.5s | $0.003 | Quota exhausted | Static template |
| Output Filter | 10ms / 30ms | negligible | PII regex miss | Backup classifier |

**Total latency**: p50 ~1.6s · p95 ~3.9s · acceptable cho chat experience.

**SPOF analysis**:
- admissions.edu API: HIGH SPOF → mitigation: read replica + 24h cache TTL
- LLM Service: MEDIUM SPOF → mitigation: multi-vendor fallback (Anthropic → OpenAI)

Khác biệt: 7 components, 3 fallback paths, observability stack, SPOF analysis, capacity numbers.

---

## Anti-pattern khi prompt — tránh

| ❌ Đừng làm | ✅ Nên làm |
|---|---|
| Diagram "User → AI" | ≥ 4 components + ≥ 3 data sources |
| Skip cache layer | Show cache strategy (TTL, invalidation) |
| 0 fallback paths | ≥ 2 fallback với trigger condition |
| Generic "monitoring" node | Specific: metrics + logs + alerts với threshold |
| Skip latency numbers | Mỗi component có p50/p95 latency + cost |
| Skip SPOF analysis | Identify SPOF + propose mitigation |

---

## Format save vào `demo.md`

````markdown
# Pack 3 — Architecture Demo (ASCII)

## System diagram

[paste ASCII diagram]

## Component table

| Component | Latency | Cost | Failure mode | Fallback |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Data flow paths

### Primary path (happy)
1. User → API Gateway → Intent → RAG cache hit → LLM → Filter → UI
2. Total latency: ~1.6s

### Fallback paths
1. RAG cache miss → API hit → vector DB → LLM
2. API timeout → refuse no-source + suggest URL
3. LLM quota → static template

## Observability stack

- **Metrics** (Prometheus): rag_hit_rate, llm_latency_p99, refuse_rate, escalation_rate
- **Logs** (Datadog): structured JSON per request
- **Alerts** (PagerDuty): 4 critical alerts

## SPOF mitigation

| Component | SPOF risk | Mitigation |
|---|---|---|
| admissions.edu API | HIGH | Read replica + 24h cache |
| LLM Service | MEDIUM | Multi-vendor fallback |

## SLO targets

- Availability: 99.9%
- Latency p95: < 5s
- rag_hit_rate: > 80%
````

---

## Câu hỏi mở rộng phản biện (optional)

```text
Architecture diagram của tôi. Giúp tôi phản biện:

1. **Cost reality**: $0.003/LLM req. 1M users × 5 queries/user/day = 5M queries/day = $15K/day = $5.4M/year.
   Realistic budget? Optimize gì để giảm 50% cost?
2. **Latency vs accuracy tradeoff**: RAG cache TTL 1 day → data có thể stale 24h.
   Acceptable cho admissions deadline (thay đổi rare)? Hay cần shorter TTL?
3. **Vendor lock-in**: phụ thuộc Pinecone (vector DB) + Anthropic (LLM) + Cloudflare (gateway).
   Migration plan nếu vendor down hoặc tăng giá 10x?
```
