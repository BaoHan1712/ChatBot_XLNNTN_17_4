# analyzer.py
import re
from langdetect import detect
try:
    from underthesea import sentiment, word_tokenize
except ImportError:
    sentiment = None
    word_tokenize = None

class FeedbackAnalyzer:
    def __init__(self):
        # TODO 1: Stopwords mở rộng tiếng Việt
        self.stopwords = {
            # Từ chức năng
            "là", "của", "và", "các", "cho", "được", "với", "trong", "có", "này", "rất", 
            "thế", "nào", "cũng", "đã", "đang", "sẽ", "vì", "nên", "thì", "mà", "còn",
            # Thêm từ vựng phổ biến
            "cái", "tháng", "tuần", "ngày", "giờ", "phút", "giây", "lần", "cách", "bộ", "bộ",
            "tại", "từ", "về", "kiến", "trên", "dưới", "qua", "lại", "sau", "trước", "trong",
            "ngoài", "trung", "giữa", "bên", "cùng", "riêng", "toàn", "phần", "nửa", "hết",
            # Từ pháp
            "được", "bị", "hãy", "hơi", "chỉ", "bao", "tất", "đó", "đấy", "kỳ", "vậy",
            # Đại từ
            "tôi", "bạn", "ông", "bà", "anh", "chị", "em", "nó", "họ", "ta", "chúng",
            "mà", "ai", "gì", "nào", "cái", "chiếc", "những", "vài", "một", "hai", "ba"
        }

    def detect_lang(self, text):
        try:
            return detect(text)
        except:
            return "vi"

    def is_edge_case(self, text):
        clean = re.sub(r'[^\w\s]', '', text).strip()
        if len(clean.split()) < 2: return True
        return False

    def get_confidence(self, text, label):
        score = 0.65
        if len(text.split()) > 5: score += 0.1
        if "không" in text.lower() or "quá" in text.lower(): score += 0.1
        return min(score, 0.95)

    def _heuristic_sentiment(self, text):
        """Phương pháp dự đoán cảm xúc đơn giản khi model gặp lỗi"""
        text_lower = text.lower()
        
        # Từ khóa tích cực
        positive_words = {"tốt", "hay", "thích", "yêu", "tuyệt", "xuất sắc", "tuyệt vời", "hài lòng", "vui"}
        # Từ khóa tiêu cực
        negative_words = {"xấu", "ghét", "tồi", "tệ", "khó chịu", "buồn", "thất vọng", "không hài lòng"}
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"

    def process(self, text):  # Đảm bảo hàm này tên là process
        lang = self.detect_lang(text)
        if self.is_edge_case(text):
            return {"sentiment": "neutral", "keywords": [], "confidence": 0.5, "error": "Phản hồi quá ngắn."}

        label = "neutral"
        keywords = []
        
        if lang == 'vi':
            try:
                if sentiment:
                    label = sentiment(text) or "neutral"
                if word_tokenize:
                    tokens = word_tokenize(text)
                    keywords = [t for t in tokens if t.isalnum() and t.lower() not in self.stopwords]
            except Exception as e:
                # Fallback khi model lỗi
                label = self._heuristic_sentiment(text)
                keywords = [w for w in text.split() if len(w) > 2 and w.lower() not in self.stopwords][:5]
        else:
            # Fallback cho ngôn ngữ khác
            label = "neutral"
            keywords = text.split()[:5]

        return {
            "sentiment": label,
            "keywords": keywords,
            "confidence": self.get_confidence(text, label),
            "lang": lang
        }