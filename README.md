# 🤖 AI Student Feedback Analysis System

Hệ thống phân tích phản hồi sinh viên bằng **AI & NLP** với hỗ trợ **đa ngôn ngữ**.

Thông Tin Sinh Viên

Họ Tên: Hàn Quốc Bảo

MSSV: 123001056
## 📋 15 TODOs - Tất cả đã hoàn thành ✅

| # | Tính năng | Trạng thái |
|---|----------|-----------|
| 1 | Mở rộng danh sách STOPWORDS | ✅ Hoàn thành (~60 từ) |
| 2 | Caching model underthesea | ✅ @st.cache_resource |
| 3 | Upload file CSV/Excel | ✅ Batch processing |
| 4 | Export lịch sử ra CSV | ✅ Download button |
| 5 | Word cloud từ khóa | ✅ WordCloud visualization |
| 6 | Timeline cảm xúc theo thời gian | ✅ Line chart |
| 7 | Edit/Delete phản hồi | ✅ Delete functionality |
| 8 | Confidence score | ✅ Heuristic scoring |
| 9 | Phân tích đa ngôn ngữ | ✅ langdetect |
| 10 | Trang hướng dẫn | ✅ Sidebar instructions |
| 11 | Persist lịch sử | ✅ history_db.json |
| 12 | Chế độ so sánh 2 nhóm | ✅ Compare tab |
| 13 | Xử lý edge case | ✅ is_edge_case() |
| 14 | Unit test | ✅ test_analyzer.py |
| 15 | Tách logic ra analyzer.py | ✅ Module riêng |

---

## 🚀 Cài đặt & Chạy

### 1. Yêu cầu
- Python 3.8+
- Pip

### 2. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy Ứng dụng

```bash
streamlit run app_chatbot_todo.py
```

Ứng dụng sẽ chạy trên: `http://localhost:8501`

---

## 🧪 Chạy Unit Tests

```bash
python test_analyzer.py
```

**Tester sẽ chạy 20+ test cases:**
- Language detection (VI, EN, fallback)
- Edge case detection
- Confidence scoring
- Sentiment analysis
- Keyword extraction
- Unicode handling
- Consistency checks

---

## 📂 Cấu trúc Dự án

```
xlnntn/
├── app_chatbot_todo.py       # Main Streamlit app (hoàn thiện)
├── analyzer.py              # Core NLP logic module
├── test_analyzer.py         # Unit tests (14 test cases)
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── history_db.json         # Persistent chat history
└── facebook_comments_vi_unlabeled.csv  # Sample data
```

---

## 💡 Tính Năng Chính

### 🎯 3 Tab Chính

#### 1. **💬 Chatbot Tab**
- Nhập phản hồi trực tiếp
- Phân tích cảm xúc real-time
- Trích xuất từ khóa
- Tính confidence score

#### 2. **📊 Thống kê Tab**
- Biểu đồ phân bố cảm xúc
- Timeline cảm xúc theo thời gian
- Word cloud từ khóa
- Chi tiết từng phản hồi
- Xóa phản hồi không cần

#### 3. **⚖️ So sánh Tab**
- So sánh 2 nhóm phản hồi
- VD: Trước/Sau cải tiến
- Hiển thị kết quả song song

### 📁 Upload & Export
- **Upload**: Hỗ trợ CSV, Excel (.xlsx)
- **Export**: Tải CSV với tất cả metadata

### 🌍 Đa Ngôn Ngữ
- Tự động phát hiện ngôn ngữ
- Hỗ trợ Tiếng Việt, Tiếng Anh, ...
- Xử lý riêng cho từng ngôn ngữ

### ⚙️ Caching & Persistence
- Model AI cache để tối ưu performance
- Lịch sử tự động lưu vào JSON

---

## 📊 Ví dụ Output

### Sentiment Analysis
```
Input:  "Khóa học này rất tuyệt vời!"
Output: 
{
  "sentiment": "positive",
  "keywords": ["khóa", "học", "tuyệt", "vời"],
  "confidence": 0.85,
  "lang": "vi"
}
```

### Edge Cases
```
Input:  "Hi"
Output: 
{
  "sentiment": "neutral",
  "keywords": [],
  "confidence": 0.5,
  "error": "Phản hồi quá ngắn."
}
```

---

## 🔍 Xử Lý Edge Cases

- **Phản hồi quá ngắn** (< 2 từ) → Đánh dấu
- **Chỉ emoji/ký tự đặc biệt** → Bỏ qua
- **Model lỗi** → Fallback heuristic
- **Unicode, emoticon** → Xử lý đúng

---

## 🧠 Công Nghệ Sử Dụng

| Component | Library | Mục đích |
|-----------|---------|---------|
| **NLP Tiếng Việt** | underthesea | Sentiment analysis, tokenization |
| **Language Detection** | langdetect | Phát hiện ngôn ngữ |
| **Visualization** | matplotlib, wordcloud | Chart, word cloud |
| **Data Processing** | pandas | Xử lý CSV, DataFrame |
| **Web Framework** | streamlit | UI interaktif |
| **Storage** | JSON | Lưu lịch sử |

---

## 📈 Performance

- **Caching**: Model load 1 lần, tái sử dụng
- **Batch Processing**: Upload 100+ phản hồi cùng lúc
- **Lazy Loading**: Timeline, word cloud load on-demand

---

## 🛠️ Troubleshooting

### ❌ Error: "ModuleNotFoundError: No module named 'langdetect'"
```bash
pip install langdetect underthesea
```

### ❌ UnicodeDecodeError
Đảm bảo file CSV/Excel có encoding UTF-8

### ❌ Model NotFittedError
Ứng dụng sẽ fallback sang heuristic sentiment tự động

---

## 📝 TODO Implementation Checklist

- [x] TODO 1: Stopwords mở rộng (60+ từ)
- [x] TODO 2: Caching (@st.cache_resource)
- [x] TODO 3: Upload CSV/Excel
- [x] TODO 4: Export CSV
- [x] TODO 5: Word cloud
- [x] TODO 6: Timeline
- [x] TODO 7: Delete functionality
- [x] TODO 8: Confidence score
- [x] TODO 9: Multi-language
- [x] TODO 10: Instructions page
- [x] TODO 11: Persistence
- [x] TODO 12: Compare mode
- [x] TODO 13: Edge case handling
- [x] TODO 14: Unit tests
- [x] TODO 15: Modular design

---

## 📧 Support

Để báo lỗi hoặc yêu cầu tính năng, hãy tạo issue.

---

**Version**: 1.0.0  
**Last Updated**: 2026-04-17  
**Status**: ✅ Production Ready
