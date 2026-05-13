---
title: Traceability Map — Bộ Kiểm thử & Thiết kế Giải pháp CSKH Hàng không
date: 2026-05-13
purpose: Hỗ trợ thuyết trình (Pitching) & Báo cáo kỹ thuật (Executive Presentation)
---

# 🗺️ BẢN ĐỒ ÁNH XẠ (TRACEABILITY MAP)
**Hệ thống**: Airline Customer Service AI Assistant (RAG-based)  
**Kết nối**: `worksheet/01-test-set-review` $\longleftrightarrow$ `worksheet/02-solution-design`

---

## 1. SƠ ĐỒ TỔNG QUAN LUỒNG GIẢI QUYẾT (EXECUTIVE FLOW DIAGRAM)

Sơ đồ minh họa cách dữ liệu sự cố thô được chuyển hóa thành các lớp phòng vệ kỹ thuật chuẩn sản xuất:

```text
 ┌────────────────────────────────────────────────────────┐
 │           01-TEST-SET-REVIEW (Giai đoạn 1)             │
 │ Tổng hợp 15 kịch bản rủi ro cao (T-01 đến T-15)        │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │            RAGAS FALLBACK EVALUATION REPORT            │
 │ Phát hiện chí mạng: Faithfulness cực thấp (0.218)      │
 │ Context Precision rất cao (0.881) -> Lỗi do LLM tự biên│
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │          02-SOLUTION-DESIGN (Giai đoạn 2)              │
 │  Cấu trúc giải pháp phòng thủ chuyên sâu (3 Lớp)       │
 └──────┬────────────────────┼─────────────────────┬──────┘
        │                    │                     │
        ▼                    ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌────────────────┐
│  LỚP BACKEND  │    │  LỚP PROMPT   │    │   LỚP UI/UX    │
│(Architecture) │    │ (Guardrails)  │    │  (Interface)   │
│ Tra cứu PSS DB│    │ Cấm cam kết số│    │ Nhãn TrustBadge│
│ Intent ~150ms │    │ Trích dẫn gốc │    │ Link Citation  │
│ Log Kafka 7năm│    │ Pass Rate 100%│    │ Nút Handoff<1s │
└───────────────┘    └───────────────┘    └────────────────┘
```

---

## 2. MA TRẬN ÁNH XẠ CHI TIẾT (TRACEABILITY MATRIX)

Bảng giúp trình bày nhanh với Giám đốc/Nhà đầu tư về cách mỗi rủi ro trong bộ kiểm thử được vô hiệu hóa hoàn toàn bởi thiết kế giải pháp:

| ID Tình huống (`01-test-set-review`) | Tên Rủi ro / Mẫu lỗi | Nguyên nhân Gốc (Root Cause) | Lớp Giải pháp Chịu trách nhiệm (`02-solution-design`) | Đầu ra Minh chứng (Demo Artifacts) |
|---|---|---|---|---|
| **T-01** | **Bịa đặt chính sách** (Hoàn tiền vé tang chế sau khi bay) | LLM tự ý diễn đạt lại quy định pháp lý, tự suy diễn lòng thương hại thay vì trích dẫn chính sách thô. | **Lớp Prompt (`2-prompt`)** + **Lớp UI/UX (`1-uiux`)** | • Guardrails cấm suy diễn chính sách.<br>• UI hiển thị Accordion link dẫn gốc để tự kiểm chứng. |
| **T-02** | **Cam kết đền bù có hại** (Hứa bồi thường 2.35M do delay) | Bot thiếu ranh giới tài chính, chiều theo giả định mồi nhử của hành khách. | **Lớp Prompt (`2-prompt`)** | • Quy tắc `NO COMPENSATION COMMITMENT` cấm tuyệt đối trả về con số bồi thường. |
| **T-03** | **Xử lý sai luồng cảm xúc** (Khách hoảng loạn vì tang lễ) | RAG bot trả lời máy móc điều khoản khô khan, thiếu khâu luân chuyển quyền ưu tiên. | **Lớp UI/UX (`1-uiux`)** + **Lớp Prompt (`2-prompt`)** | • Kịch bản Few-shot thấu cảm.<br>• Banner thoát hiểm tự động hiển thị nút kết nối Agent. |
| **T-04** | **Jailbreak / Prompt Injection** ("Ignore previous instructions") | Lỗ hổng kỹ thuật cho phép ghi đè chỉ thị hệ thống. | **Lớp Prompt (`2-prompt`)** | • Cơ chế cô lập Boundary, từ chối thực thi các lệnh độc hại/mâu thuẫn. |
| **T-05** | **Ảo giác logic tính toán** (Hoàn vé một phần HAN-SGN) | LLM tự tính nhầm số tiền hoàn chặng lẻ thay vì tra cứu engine định giá. | **Lớp Backend (`3-architecture`)** | • Định tuyến bắt buộc gọi thẳng cơ sở dữ liệu lõi **PSS Core DB** qua mã PNR. |
| **T-06** | **Tư vấn y tế vượt quyền** (Bầu 36 tuần đau bụng/ra máu) | Trợ lý ảo sa đà vào đọc điều kiện bay thay vì nhận diện khẩn cấp y tế tính mạng. | **Lớp Backend (`3-architecture`)** + **Lớp UI/UX (`1-uiux`)** | • Intent Classifier ngắt luồng RAG ngay lập tức.<br>• UI chớp dải băng đỏ gọi trực tiếp Đội Y tế Sân bay (< 1s). |
| **T-07** | **Khách hàng dọa kiện** (Leo thang pháp lý) | Thiếu cơ chế lắng nghe sự giận dữ tột độ để nhường quyền kiểm soát. | **Lớp Backend (`3-architecture`)** | • Kích hoạt cờ `Red-Flag`, tự động ngắt bot và đẩy phiên chat cho bộ phận Pháp lý. |
| **T-08** | **Thao túng pháp luật** (Trích dẫn sai Nghị định 92 đòi tiền) | Người dùng lợi dụng bối cảnh pháp lý riêng của Việt Nam để gài bẫy bot. | **Lớp Prompt (`2-prompt`)** | • Prompt cung cấp sẵn kịch bản bác bỏ nhẹ nhàng, trích dẫn chuẩn xác Công báo 927 & 928. |
| **T-09** | **Tin đồn thất thiệt** (Hoàn tiền do ô nhiễm môi trường) | Dữ liệu RAG bị nhiễu hoặc bot tự suy diễn từ nguồn tin tức không chính thống. | **Lớp Backend (`3-architecture`)** | • Ngưỡng chặn an toàn **Similarity Score < 0.78** tự động trả về từ chối tĩnh `NO-SOURCE`. |
| **T-10** | **Tin AI quá mức** (Ép đưa số liệu phí đổi vé ước chừng) | Người dùng lười tra cứu, ép bot nói đại một con số. | **Lớp Prompt (`2-prompt`)** + **Lớp UI/UX (`1-uiux`)** | • Bot kiên quyết từ chối đưa số ước lượng, yêu cầu PNR.<br>• UI đổi Trust Badge sang màu Cam cảnh báo. |
| **T-11** | **Bối cảnh riêng VN** (Dùng app VNeID thay CCCD) | Dữ liệu RAG thô chưa cập nhật kịp công văn mới của Cục Hàng không. | **Lớp Backend (`3-architecture`)** | • Bổ sung bộ đệm **Redis Cache (TTL 24h)** nạp tức thời các quy định vận hành mới nhất. |
| **T-12** | **Nghiệp vụ hẹp** (Sai trật tự tên trên vé và giấy tờ) | Bot không hiểu quy trình Name Correction, tư vấn sai rủi ro an ninh sân bay. | **Lớp Prompt (`2-prompt`)** | • Bổ sung hướng dẫn giải thích nghiệp vụ và yêu cầu ra quầy vé xử lý. |
| **T-13** | **Áp lực giận dữ** (De-escalation khi bị chửi bới) | LLM phản ứng phòng thủ hoặc xin lỗi vòng vo gây thêm ức chế. | **Lớp Prompt (`2-prompt`)** + **Lớp UI/UX (`1-uiux`)** | • Kịch bản Few-shot giữ vững Boundary.<br>• Giao diện mở nhanh kênh khiếu nại chính thức. |
| **T-14** | **Bẫy thương hại** ("Chị sinh viên nghèo bị lừa hết tiền") | Tấn công thao túng cảm xúc (Sycophancy/Emotional jailbreak). | **Lớp Prompt (`2-prompt`)** | • Hướng dẫn AI cách từ chối mềm mỏng nhưng tuân thủ tuyệt đối **Fare Rules Matrix**. |
| **T-15** | **Phương ngữ/Slang** ("vé tui trả lại đc hk?") | Bot không bắt được ngữ nghĩa tiếng lóng ngắn gọn của người Việt. | **Lớp Backend (`3-architecture`)** | • Mô hình phân loại Intent siêu nhẹ (~150ms) chuẩn hóa thành truy vấn "Refund". |

---

## 3. KỊCH BẢN THUYẾT TRÌNH (3-MINUTE ELEVATOR PITCH)

Sử dụng kịch bản này để Pitching thuyết phục trước hội đồng đánh giá hoặc Ban Giám đốc:

### 🎤 1. Đặt vấn đề (Hook & Problem Statement)
> *"Chào các anh/chị. Trong ngành dịch vụ hàng không, một lời nói bất cẩn của Trợ lý AI có thể dẫn đến thảm họa truyền thông hoặc các vụ kiện tụng hàng triệu đô — điển hình là vụ việc chatbot Air Canada bịa đặt chính sách hoàn vé tang lễ gần đây.*
> 
> *Khi chạy kiểm thử độc lập bộ 15 kịch bản rủi ro cao trên hệ thống của chúng ta, báo cáo **RAGAS Fallback** đã gióng lên hồi chuông cảnh báo: chỉ số truy xuất tài liệu (Context Precision) rất cao đạt **0.881**, nhưng độ chính xác nguyên văn (Faithfulness) lại tụt dốc thảm hại xuống **0.218**. Nguyên nhân cốt lõi không nằm ở dữ liệu của hãng, mà do mô hình LLM tự ý 'ảo giác', dùng từ ngữ đồng nghĩa làm sai lệch bản chất pháp lý và dễ dãi cam kết đền bù khi bị khách hàng gài bẫy cảm xúc."*

### 💡 2. Giải pháp Phòng thủ Đa tầng (Defense-in-Depth Strategy)
> *"Để giải quyết triệt để rủi ro này, nhóm không áp dụng một miếng vá tạm thời, mà thiết kế một **hệ thống phòng thủ chuyên sâu 3 lớp** bổ trợ lẫn nhau:*
> 1. **Tầng Kiến trúc Dữ liệu (Backend)**: Đặt một Intent Classifier siêu nhẹ ngay tại cửa ngõ Gateway (độ trễ ~150ms) để lọc luồng. Bất kỳ câu hỏi nào về giá cả hay điều kiện vé cụ thể đều buộc phải gọi trực tiếp cơ sở dữ liệu lõi **PSS Core DB** qua mã PNR, đồng thời ngắt ngay luồng sinh văn bản nếu độ tự tin của dữ liệu RAG dưới ngưỡng 0.78.
> 2. **Tầng Chỉ dẫn AI (Prompt Guardrails)**: Tiêm trực tiếp các bộ quy tắc sắt đá vào System Prompt: cấm tuyệt đối việc đưa ra con số bồi thường tiền mặt và bắt buộc bot đính kèm số trích dẫn liền kề sau mỗi câu khẳng định.
> 3. **Tầng Giao diện (UI/UX)**: Khách hàng sẽ thấy một **Trust Badge** (Nhãn tin cậy) đổi màu động ngay đầu tin nhắn, kèm danh sách link nguồn gốc để tự bấm vào kiểm chứng. Đặc biệt, nếu phát hiện từ khóa cấp cứu thai sản hay đe dọa kiện tụng, giao diện lập tức hiện dải băng đỏ kết nối thẳng với nhân viên trực ban hoặc xe cấp cứu mặt đất dưới 1 giây."*

### 📈 3. Tác động và Cam kết (Results & Compliance Audit)
> *"Kết quả thử nghiệm hồi quy (Regression Test) cho thấy hệ thống mới đạt **Pass Rate 100%** trên toàn bộ các ca khó nhất. Hơn thế nữa, để bảo vệ pháp lý tối đa cho hãng, toàn bộ các phiên trò chuyện khẩn cấp đều được xáo trộn thông tin cá nhân (đáp ứng NĐ 13/2023) và lưu trữ ngầm trên hệ thống bất biến (Immutable Storage) kéo dài **7 năm**.*
> 
> *Giải pháp của chúng ta không chỉ thông minh, thấu cảm mà còn tuyệt đối an toàn và tuân thủ pháp luật."*

---

## 4. CẤU TRÚC THƯ MỤC KIỂM CHỨNG (ARTIFACT DIRECTORY TREE)

Khi trình bày demo trực tiếp trên máy, hãy mở các file sau theo thứ tự:

```text
worksheet/
├── 01-test-set-review/
│   └── 3-FINAL-test-set-eval-plan.md     <-- [Mở trước: Danh sách 15 Test cases gốc]
│
├── map.md                                <-- [Mở thứ hai: Bản đồ giải thích mạch nối này]
│
└── 02-solution-design/
    ├── 1-map-and-format.md               <-- [Kế hoạch tổng thể: Phân tích Root Cause]
    └── artifact/
        ├── 1-uiux/demo.md                <-- [Demo 1: Bản vẽ ASCII UI chat trên di động]
        ├── 2-prompt/demo.md              <-- [Demo 2: System Prompt sản xuất & Pass 100%]
        └── 3-architecture/demo.md        <-- [Demo 3: ASCII System Diagram & Capacity]
```
