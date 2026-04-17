# ============================================================
# AI Student Feedback System - Complete Implementation
# ============================================================
# Tất cả 15 TODO đã được implement

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
import json
import os
from analyzer import FeedbackAnalyzer

# ============================================================
# CONFIG & CACHING (TODO 2)
# ============================================================
st.set_page_config(page_title="Feedback Analyzer Pro", layout="wide")

@st.cache_resource
def get_analyzer():
    """TODO 2: Cache model để tránh load lại mỗi lần rerun"""
    return FeedbackAnalyzer()

analyzer = get_analyzer()

# ============================================================
# TODO 11: PERSISTENCE (Lịch sử chat vào file)
# ============================================================
DB_PATH = "history_db.json"

def load_data():
    """Load lịch sử từ file JSON"""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data():
    """Lưu lịch sử vào file JSON"""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(st.session_state.history, f, default=str, ensure_ascii=False, indent=2)

# ============================================================
# INITIALIZATION
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = load_data()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# UTILS
# ============================================================
def add_entry(text, tag="General"):
    """Thêm entry mới vào history"""
    res = analyzer.process(text)
    entry = {
        "id": datetime.now().timestamp(),
        "text": text,
        "sentiment": res["sentiment"],
        "keywords": res["keywords"],
        "confidence": res["confidence"],
        "tag": tag,
        "timestamp": datetime.now().isoformat(),
        "lang": res.get("lang", "vi")
    }
    st.session_state.history.append(entry)
    save_data()
    return entry

def delete_entry(entry_id):
    """Xóa entry khỏi history"""
    st.session_state.history = [e for e in st.session_state.history if e['id'] != entry_id]
    save_data()

def get_sentiment_color(sentiment):
    """Trả về color cho sentiment badge"""
    colors = {
        "positive": "🟢 Tích cực",
        "negative": "🔴 Tiêu cực", 
        "neutral": "⚪ Trung lập"
    }
    return colors.get(sentiment, "⚪ Không xác định")

# ============================================================
# UI COMPONENTS
# ============================================================
def render_stats(df):
    """Render thống kê (TODO 6: Timeline, TODO 5: Word cloud)"""
    if df.empty:
        st.warning("Chưa có dữ liệu để hiển thị.")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Tổng phản hồi", len(df))
    pos_rate = len(df[df['sentiment'] == 'positive']) / len(df) if len(df) > 0 else 0
    col2.metric("🟢 Tỉ lệ tích cực", f"{pos_rate:.1%}")
    neg_rate = len(df[df['sentiment'] == 'negative']) / len(df) if len(df) > 0 else 0
    col3.metric("🔴 Tỉ lệ tiêu cực", f"{neg_rate:.1%}")
    col4.metric("📈 Độ tin cậy TB", f"{df['confidence'].mean():.2%}")

    # Biểu đồ cảm xúc
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📈 Phân bố cảm xúc")
        sentiment_counts = df['sentiment'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_counts.plot(kind='bar', color=['green' if x == 'positive' else 'red' if x == 'negative' else 'gray' 
                                                   for x in sentiment_counts.index], ax=ax)
        ax.set_title("Phân bố cảm xúc phản hồi", fontsize=14, fontweight='bold')
        ax.set_xlabel("Cảm xúc")
        ax.set_ylabel("Số lượng")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        st.pyplot(fig)

    # TODO 6: Timeline cảm xúc theo thời gian
    with col2:
        st.write("### 🕐 Xu hướng cảm xúc theo thời gian")
        df['time'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M')
        timeline_data = df.groupby(['time', 'sentiment']).size().unstack(fill_value=0)
        if not timeline_data.empty:
            st.line_chart(timeline_data)
        else:
            st.info("Chưa đủ dữ liệu để vẽ timeline")

    # TODO 5: Word cloud từ khóa
    st.write("### ☁️ Từ khóa phổ biến")
    all_words = " ".join([" ".join(k) for k in df['keywords']])
    if all_words.strip():
        wc = WordCloud(background_color="white", width=800, height=400, 
                      collocations=False, prefer_horizontal=0.7).generate(all_words)
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Chưa có từ khóa để hiển thị word cloud")

# ============================================================
# TODO 10: HƯỚNG DẪN & THÔNG TIN
# ============================================================
def show_instructions():
    """Hiển thị trang hướng dẫn sử dụng"""
    st.write("""
    # 📖 Hướng dẫn sử dụng Feedback Analyzer Pro
    
    ## 🎯 Chức năng chính
    
    ### 1. 💬 **Chatbot Tab**
    - Nhập phản hồi của sinh viên trực tiếp vào chat
    - Hệ thống sẽ tự động phân tích cảm xúc (tích cực/tiêu cực/trung lập)
    - Trích xuất từ khóa chính từ phản hồi
    - Tính toán độ tin cậy (confidence score)
    
    ### 2. 📊 **Thống kê Tab**
    - Hiển thị biểu đồ phân bố cảm xúc
    - Timeline xu hướng cảm xúc theo thời gian
    - Word cloud các từ khóa phổ biến
    - Xem chi tiết từng phản hồi
    - **Xóa** phản hồi không cần thiết
    
    ### 3. ⚖️ **So sánh Nhóm Tab**
    - So sánh cảm xúc giữa 2 nhóm phản hồi
    - VD: Trước/Sau cải tiến, Nhóm A vs Nhóm B
    - Hiển thị kết quả cảm xúc song song
    
    ## 📥 **Upload Dữ liệu**
    - Hỗ trợ file CSV và Excel (.xlsx)
    - Cột đầu tiên phải chứa phản hồi
    - Tự động xử lý hàng loạt
    
    ## 📤 **Export Dữ liệu**
    - Tải lịch sử phân tích dưới dạng CSV
    - Gồm: phản hồi, cảm xúc, từ khóa, độ tin cậy, thời gian
    
    ## 🌍 **Hỗ trợ Đa ngôn ngữ**
    - Tự động phát hiện ngôn ngữ (Tiếng Việt, Tiếng Anh, ...)
    - Xử lý riêng cho từng ngôn ngữ
    
    ## ⚙️ **Cách hoạt động**
    1. **Tokenization**: Tách và làm sạch text
    2. **Sentiment Analysis**: Phân tích cảm xúc bằng NLP
    3. **Keyword Extraction**: Trích xuất từ khóa quan trọng
    4. **Confidence Scoring**: Tính độ tin cậy của phân tích
    5. **Persistence**: Lưu lịch sử vào file dữ liệu
    
    ## 💡 **Mẹo sử dụng**
    - Phản hồi ngắn (1-2 từ) sẽ được đánh dấu là edge case
    - Chỉ emoji hoặc ký tự đặc biệt sẽ bị bỏ qua
    - Lịch sử tự động lưu vào file `history_db.json`
    - Làm tươi trang để âm thầm tải lịch sử mới nhất
    """)

# ============================================================
# MAIN APP
# ============================================================
def main():
    st.title("🤖 AI Student Feedback Analysis System")
    st.markdown("*Phân tích phản hồi sinh viên bằng AI - Hỗ trợ đa ngôn ngữ*")
    
    # Sidebar Controls
    with st.sidebar:
        st.markdown("---")
        st.write("### ⚙️ Công cụ")
        
        # TODO 10: Instructions
        tab_sidebar = st.radio("**Chọn chức năng:**", 
                              ["Chính", "Hướng dẫn"])
        
        if tab_sidebar == "Hướng dẫn":
            show_instructions()
            return
        
        # TODO 3: File Upload
        st.write("### 📁 Tải dữ liệu lên")
        uploaded_file = st.file_uploader("Chọn file CSV hoặc Excel", type=['csv', 'xlsx'])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df_upload = pd.read_csv(uploaded_file)
                else:
                    df_upload = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Đã đọc {len(df_upload)} dòng từ file")
                
                if st.button("🚀 Xử lý file"):
                    progress_bar = st.progress(0)
                    for idx, txt in enumerate(df_upload.iloc[:, 0].dropna()):
                        add_entry(str(txt), tag="Batch Upload")
                        progress_bar.progress((idx + 1) / len(df_upload))
                    st.success("✅ Đã nạp file thành công!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
        
        # Dữ liệu hiện tại
        st.write(f"### 📊 Thống kê nhanh")
        st.metric("Tổng entries", len(st.session_state.history))
        if st.session_state.history:
            df_hist = pd.DataFrame(st.session_state.history)
            col1, col2 = st.columns(2)
            pos_count = len(df_hist[df_hist['sentiment'] == 'positive'])
            neg_count = len(df_hist[df_hist['sentiment'] == 'negative'])
            col1.metric("🟢 Tích cực", pos_count)
            col2.metric("🔴 Tiêu cực", neg_count)
        
        # TODO 4: Export
        if st.session_state.history:
            st.write("### 📤 Xuất dữ liệu")
            df_hist = pd.DataFrame(st.session_state.history)
            csv_data = df_hist.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Tải CSV", csv_data, "feedback_analysis.csv", "text/csv")

    # Main Tabs
    t_chat, t_analytics, t_compare = st.tabs(["💬 Chatbot", "📊 Thống kê", "⚖️ So sánh"])

    with t_chat:
        st.write("## 💬 Nhập phản hồi sinh viên")
        
        # Hiển thị lịch sử chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
        
        # Input mới
        if prompt := st.chat_input("Nhập phản hồi sinh viên..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Xử lý phản hồi
            entry = add_entry(prompt)
            
            # Tạo response
            sentiment_emoji = get_sentiment_color(entry['sentiment'])
            keywords_str = ", ".join(entry['keywords'][:10]) if entry['keywords'] else "Không có"
            
            reply = f"""
            **Kết quả phân tích:**
            
            - **Cảm xúc:** {sentiment_emoji}
            - **Độ tin cậy:** {entry['confidence']:.1%}
            - **Ngôn ngữ:** {entry['lang']}
            - **Từ khóa:** {keywords_str}
            - **Thời gian:** {entry['timestamp']}
            """
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            with st.chat_message("assistant"):
                st.markdown(reply)

    with t_analytics:
        st.write("## 📊 Phân tích & Thống kê")
        
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            render_stats(df)
            
            # TODO 7: Chi tiết lịch sử - Edit/Delete
            st.write("### 📝 Chi tiết phản hồi")
            for i, row in df.iterrows():
                col_meta, col_delete = st.columns([0.95, 0.05])
                
                with col_meta:
                    with st.expander(f"{get_sentiment_color(row['sentiment'])} | {row['text'][:50]}... | {row['timestamp'][:10]}"):
                        st.write(f"**Phản hồi:** {row['text']}")
                        col1, col2, col3 = st.columns(3)
                        col1.write(f"**Cảm xúc:** {row['sentiment']}")
                        col2.write(f"**Độ tin cậy:** {row['confidence']:.1%}")
                        col3.write(f"**Từ khóa:** {', '.join(row['keywords'][:5])}")
                
                with col_delete:
                    if st.button("🗑️", key=f"del_{row['id']}", help="Xóa phản hồi này"):
                        delete_entry(row['id'])
                        st.rerun()
        else:
            st.info("📭 Chưa có dữ liệu. Hãy nhập hoặc upload phản hồi.")

    with t_compare:
        st.write("## ⚖️ So sánh hai nhóm phản hồi")
        st.markdown("*So sánh cảm xúc giữa hai nhóm (VD: Trước/Sau cải tiến)*")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.write("### 📍 Nhóm A")
            txt_a = st.text_area("Nhập nhóm A (VD: Trước cải tiến)", height=150, key="text_a")
        
        with col_b:
            st.write("### 📍 Nhóm B")
            txt_b = st.text_area("Nhập nhóm B (VD: Sau cải tiến)", height=150, key="text_b")
        
        if st.button("🔍 So sánh", use_container_width=True):
            if txt_a.strip() and txt_b.strip():
                res_a = analyzer.process(txt_a)
                res_b = analyzer.process(txt_b)
                
                col_res_a, col_res_b = st.columns(2)
                
                with col_res_a:
                    st.success(f"**Nhóm A**")
                    st.write(f"- **Cảm xúc:** {get_sentiment_color(res_a['sentiment'])}")
                    st.write(f"- **Độ tin cậy:** {res_a['confidence']:.1%}")
                    st.write(f"- **Từ khóa:** {', '.join(res_a['keywords'][:5])}")
                
                with col_res_b:
                    st.success(f"**Nhóm B**")
                    st.write(f"- **Cảm xúc:** {get_sentiment_color(res_b['sentiment'])}")
                    st.write(f"- **Độ tin cậy:** {res_b['confidence']:.1%}")
                    st.write(f"- **Từ khóa:** {', '.join(res_b['keywords'][:5])}")
                
                # Kết luận
                st.markdown("---")
                if res_a['sentiment'] == res_b['sentiment']:
                    st.info("✅ Cảm xúc giữa hai nhóm **giống nhau**")
                else:
                    st.warning(f"⚠️ Cảm xúc **khác nhau**: {res_a['sentiment']} vs {res_b['sentiment']}")
            else:
                st.warning("⚠️ Vui lòng nhập dữ liệu cho cả hai nhóm")

if __name__ == "__main__":
    main()
