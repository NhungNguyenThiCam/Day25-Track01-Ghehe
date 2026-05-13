---
artifact: 3 — Demo kiến trúc dữ liệu
format: ASCII System Architecture + Capacity Planning + Observability Stack
---

# demo.md — Demo kiến trúc dữ liệu (ASCII Data Architecture)

Bản thiết kế hệ thống dữ liệu backend và luồng xử lý RAG đa tầng nhằm triệt tiêu hoàn toàn rủi ro AI bịa đặt thông tin chính sách vé và bỏ sót các tình huống khẩn cấp.

---

## 1. Sơ đồ Kiến trúc Dữ liệu (ASCII System Diagram)

```text
                  ┌────────────────────────────────────────┐
                  │          USER (Web / App / Kiosk)      │
                  └───────────────────┬────────────────────┘
                                      │ HTTPS + Hashed UserID
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │  API GATEWAY (Cloudflare Workers / Kong Gateway) │
             │  - Rate limit: 20 requests / min / user          │
             │  - WAF & DDoS Shield                             │
             │  - Push async raw request log ──► [ DATADOG ]    │
             └────────────────────────┬─────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │  INTENT CLASSIFIER (Fast Lightweight LLM / Rule) │
             │  - Latency p50: ~150ms                           │
             │  - Phân loại: Normal / PNR-Required / Red-Flag   │
             └──────┬─────────────────┬──────────────────┬──────┘
                    │                 │                  │
         ┌──────────┴──────┐   ┌──────┴──────────┐   ┌───┴──────────────┐
         ▼                 ▼   ▼                 ▼   ▼                  ▼
     [ Normal ]     [ PNR-Required ]       [ Out-of-Scope ]    [ Red-Flag / Emergency ]
         │                 │                     │                      │
         │                 ▼                     ▼                      ▼
         │          ┌──────────────┐      ┌──────────────┐       ┌──────────────────────┐
         │          │ PSS CORE DB  │      │ STATIC REFUSE│       │ COUNSELOR ESCALATION │
         │          │ Tra cứu vé   │      │ Lịch sự ngắt │       │ - Cảnh báo giao diện │
         │          │ Timeout < 1s │      │ luồng RAG    │       │ - Line CSKH: 1800-xxx│
         │          └──────┬───────┘      └──────────────┘       │ - Báo động Y tế Sân  │
         │                 │                                     │   bay < 1 giây       │
         │                 ▼                                     └──────────┬───────────┘
         │          ┌──────────────┐                                        │
         │          │ REDIS CACHE  │◄────── Cache Hit (TTL 24h)             │
         │          │ TTL 24h      │                                        │
         │          └──────┬───────┘                                        │
         │                 │ Cache Miss                                     │
         ▼                 ▼                                                │
    ┌──────────────────────────────┐                                        │
    │ VECTOR DB (Pinecone / Milvus)│                                        │
    │ - Embedding Policy Matrix    │                                        │
    │ - Similarity Score >= 0.78   │                                        │
    └──────────────┬───────────────┘                                        │
                   │                                                        │
     Similarity < 0.78 (Low Confidence) ──► [ STATIC REFUSE: NO-SOURCE ]    │
                   │                                                        │
                   ▼                                                        │
    ┌──────────────────────────────────────────────────┐                    │
    │ LLM GENERATION SERVICE (Anthropic Claude 3.5)    │                    │
    │ - Inject RAG context nguyên văn                  │                    │
    │ - Cấm tuyệt đối hứa hẹn ngoại lệ                 │                    │
    │ - Tự động đính kèm liên kết trích dẫn (Citation) │                    │
    └──────────────────────┬───────────────────────────┘                    │
                           │                                                │
                           ▼                                                │
    ┌──────────────────────────────────────────────────┐                    │
    │ OUTPUT FILTER & COMPLIANCE LAYER                 │                    │
    │ - Strip PII (Che giấu số hộ chiếu, CCCD, SĐT)    │                    │
    │ - Gán nhãn tin cậy:                              │                    │
    │   • Score >= 0.85 ──► ✓ Đã kiểm chứng             │                    │
    │   • Score < 0.85  ──► ⚠ Cảnh báo / Ngắt luồng    │                    │
    └──────────────────────┬───────────────────────────┘                    │
                           │                                                │
             ┌─────────────┴─────────────┐                                  │
             ▼                           ▼                                  │
      [ Send to UI ]              [ OBSERVABILITY ]                         │
                                  - Datadog Log                             │
                                  - Prometheus Metric                       │
                                  - Kafka Audit Queue ◄─────────────────────┘
                                         │
                                         ▼
                                  [ MONITORING STACK ]
                                  • Grafana Dashboard
                                  • PagerDuty Alert (RAG Fail > 5%)
                                  • Legal Storage (Lưu trữ 7 năm)
```

---

## 2. Bảng Phân Tích Năng Lực Thành Phần (Capacity Planning Table)

| Thành phần (Component) | Độ trễ (Latency p50/p95) | Chi phí ước tính | Failure Mode (Mẫu sự cố) | Đường dẫn Fallback (Dự phòng) |
|---|---|---|---|---|
| **API Gateway** | 30ms / 80ms | $0.0001 / req | Bị tấn công DDoS | Tự động kích hoạt Cloudflare Rate-limiting. |
| **Intent Classifier** | 150ms / 300ms | $0.0001 / req | LLM API Timeout | Mặc định coi là truy vấn rủi ro cao (Conservative mode). |
| **Redis Cache** | 5ms / 15ms | Cố định hạ tầng | Cold Start / Miss | Bỏ qua Cache, gọi trực tiếp API tra cứu PSS DB. |
| **Primary PSS DB** | 250ms / 700ms | $0.005 / req | Quá tải truy vấn | Trả lời từ Redis Cache cũ kèm cảnh báo "Dữ liệu có thể chưa cập nhật". |
| **Vector DB** | 40ms / 120ms | $0.01 / 1K req | Corrupted Index | Kích hoạt luồng Static Refusal (Từ chối do thiếu nguồn). |
| **LLM Gen Service** | 900ms / 2.2s | $0.003 / req | Hết hạn mức Quota | Trả về thông báo khuôn mẫu: "Hệ thống đang bận, vui lòng gọi Hotline." |
| **Output Filter** | 10ms / 25ms | Gần như bằng 0 | Lọt dữ liệu PII | Hệ thống Backup Regex tự động thay thế số PII bằng chuỗi `[SECURE]`. |

**Tổng ngân sách độ trễ (Total Latency Budget)**: p50 ~1.38s · p95 ~3.44s (Hoàn toàn mượt mà cho trải nghiệm trò chuyện thời gian thực).

---

## 3. Các Đường Đi Dự Phòng Cốt Lõi (Fallback Chains)

1. **Fallback 1 (Khi PSS Core DB sập hoặc Timeout > 1s)**:
   - Hệ thống bỏ qua DB trực tiếp, chuyển sang đọc bảng quy định vé chung từ Redis Cache.
   - Giao diện người dùng hiển thị: *"Hệ thống lõi đang bảo trì. Thông tin bên dưới dựa trên quy định chung gần nhất."*
2. **Fallback 2 (Khi Vector DB không tìm thấy tài liệu có Similarity >= 0.78)**:
   - Ngắt luồng chuyển tiếp sang LLM Gen Service.
   - Trực tiếp trả về câu phản hồi tĩnh: *"Hệ thống chưa tìm thấy điều kiện cụ thể cho truy vấn của bạn. Vui lòng tham khảo trang Fare Rules hoặc gặp nhân viên CSKH."*
3. **Fallback 3 (Khi LLM Service sập hoặc cạn Quota)**:
   - Trả về tin nhắn tĩnh khẩn cấp để không làm treo giao diện người dùng.

---

## 4. Ngăn Xếp Giám Sát & Tuân Thủ (Observability Stack)

Hệ thống cung cấp khả năng quan sát toàn diện nhằm đảm bảo an toàn kỹ thuật và tuân thủ pháp lý:

### A. Metrics (Prometheus-compatible)
- `rag_hit_rate{status="hit|miss|low_sim"}`: Tỉ lệ RAG tìm thấy tài liệu liên quan.
- `llm_latency_seconds{quantile="p50|p95|p99"}`: Thời gian phản hồi của LLM.
- `refusal_rate{trigger="no_source|oos|jailbreak"}`: Tỉ lệ từ chối an toàn của bot.
- `escalation_rate{priority="medical_emergency|legal_threat"}`: Tỉ lệ chuyển đổi sang nhân viên trực ban.

### B. Structured Logs (Datadog JSON)
- Ghi log 100% các trường hợp bị từ chối và các ca khẩn cấp y tế.
- Dữ liệu bao gồm: `timestamp`, `hashed_user_id`, `classified_intent`, `similarity_score`, `retrieved_chunks_ids`.

### C. Cảnh báo tự động (PagerDuty Alerts)
- **Kích hoạt P1**: Tỉ lệ `rag_hit_rate` giảm dưới 70% trong khung giờ vàng (Peak-time).
- **Kích hoạt P2**: Tỉ lệ `escalation_rate` tăng đột biến gấp 3 lần mức cơ sở (Dấu hiệu khủng hoảng hoãn/hủy chuyến diện rộng).

### D. Tuân thủ Pháp lý (Legal Audit Trail)
- Để tuân thủ Luật Hàng không và bảo vệ quyền lợi pháp lý trong trường hợp xảy ra khiếu nại bồi thường, toàn bộ các phiên trò chuyện được gắn cờ `Red-Flag` sẽ được đẩy ngầm qua Kafka vào phân vùng **Lưu trữ Bất biến (Immutable Storage)** kéo dài trong **7 năm**.
- Tuân thủ Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân thông qua cơ chế xáo trộn (masking) tự động tại Output Filter.
