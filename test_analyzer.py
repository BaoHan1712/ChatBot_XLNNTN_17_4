"""
Unit Tests cho FeedbackAnalyzer
TODO 14: Thêm unit test cho hàm analyze_feedback
"""

import unittest
from analyzer import FeedbackAnalyzer


class TestFeedbackAnalyzer(unittest.TestCase):
    """Test cases cho FeedbackAnalyzer class"""
    
    def setUp(self):
        """Setup trước mỗi test"""
        self.analyzer = FeedbackAnalyzer()
    
    # ==================== TEST INITIALIZATION ====================
    def test_analyzer_init(self):
        """Test khởi tạo FeedbackAnalyzer"""
        self.assertIsNotNone(self.analyzer.stopwords)
        self.assertTrue(len(self.analyzer.stopwords) > 0)
        print("✅ Test init: PASSED")
    
    def test_stopwords_content(self):
        """Test danh sách stopwords có chứa các từ cơ bản"""
        expected_words = ["là", "của", "và", "các", "cho"]
        for word in expected_words:
            self.assertIn(word, self.analyzer.stopwords)
        print("✅ Test stopwords: PASSED")
    
    # ==================== TEST LANGUAGE DETECTION ====================
    def test_detect_lang_vietnamese(self):
        """Test phát hiện tiếng Việt"""
        text = "Phản hồi này rất tốt"
        lang = self.analyzer.detect_lang(text)
        self.assertEqual(lang, "vi")
        print("✅ Test detect Vietnamese: PASSED")
    
    def test_detect_lang_english(self):
        """Test phát hiện tiếng Anh"""
        text = "This is an excellent feedback"
        lang = self.analyzer.detect_lang(text)
        self.assertEqual(lang, "en")
        print("✅ Test detect English: PASSED")
    
    def test_detect_lang_fallback(self):
        """Test fallback về VI khi lỗi"""
        text = "123 @#$ !@#"
        lang = self.analyzer.detect_lang(text)
        self.assertEqual(lang, "vi")
        print("✅ Test detect fallback: PASSED")
    
    # ==================== TEST EDGE CASES ====================
    def test_edge_case_too_short(self):
        """Test phát hiện phản hồi quá ngắn (1-2 từ)"""
        text = "Tốt"
        is_edge = self.analyzer.is_edge_case(text)
        self.assertTrue(is_edge)
        print("✅ Test edge case (too short): PASSED")
    
    def test_edge_case_only_special_chars(self):
        """Test phát hiện phản hồi chỉ có ký tự đặc biệt"""
        text = "!@#$%^&*()"
        is_edge = self.analyzer.is_edge_case(text)
        self.assertTrue(is_edge)
        print("✅ Test edge case (special chars): PASSED")
    
    def test_edge_case_only_emoji(self):
        """Test phát hiện phản hồi chỉ có emoji"""
        text = "😀😃😄"
        is_edge = self.analyzer.is_edge_case(text)
        self.assertTrue(is_edge)
        print("✅ Test edge case (emoji only): PASSED")
    
    def test_not_edge_case_normal_text(self):
        """Test văn bản bình thường không phải edge case"""
        text = "Phản hồi này rất hay và hữu ích cho tôi"
        is_edge = self.analyzer.is_edge_case(text)
        self.assertFalse(is_edge)
        print("✅ Test normal text: PASSED")
    
    # ==================== TEST CONFIDENCE SCORING ====================
    def test_confidence_short_text(self):
        """Test confidence score cho phản hồi ngắn"""
        score = self.analyzer.get_confidence("Tốt", "positive")
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 0.95)
        print("✅ Test confidence (short): PASSED")
    
    def test_confidence_long_text(self):
        """Test confidence score cho phản hồi dài"""
        long_text = "Phản hồi này rất tốt và tuyệt vời. Tôi rất hài lòng với dịch vụ này"
        score1 = self.analyzer.get_confidence(long_text, "positive")
        short_text = "Tốt"
        score2 = self.analyzer.get_confidence(short_text, "positive")
        self.assertGreater(score1, score2)
        print("✅ Test confidence (long > short): PASSED")
    
    def test_confidence_with_negation(self):
        """Test confidence score thay đổi với từ phủ định"""
        text_neg = "Phản hồi này không tốt và quá tệ"
        score_neg = self.analyzer.get_confidence(text_neg, "negative")
        text_normal = "Phản hồi này tốt"
        score_normal = self.analyzer.get_confidence(text_normal, "neutral")
        self.assertGreater(score_neg, score_normal)
        print("✅ Test confidence (negative boost): PASSED")
    
    # ==================== TEST SENTIMENT ANALYSIS ====================
    def test_heuristic_sentiment_positive(self):
        """Test phát hiện cảm xúc tích cực"""
        text = "Phản hồi này rất tốt, tôi yêu dịch vụ này"
        sentiment = self.analyzer._heuristic_sentiment(text)
        self.assertEqual(sentiment, "positive")
        print("✅ Test heuristic sentiment (positive): PASSED")
    
    def test_heuristic_sentiment_negative(self):
        """Test phát hiện cảm xúc tiêu cực"""
        text = "Phản hồi này rất xấu, tôi ghét dịch vụ này"
        sentiment = self.analyzer._heuristic_sentiment(text)
        self.assertEqual(sentiment, "negative")
        print("✅ Test heuristic sentiment (negative): PASSED")
    
    def test_heuristic_sentiment_neutral(self):
        """Test phát hiện cảm xúc trung lập"""
        text = "Phản hồi này bình thường"
        sentiment = self.analyzer._heuristic_sentiment(text)
        self.assertEqual(sentiment, "neutral")
        print("✅ Test heuristic sentiment (neutral): PASSED")
    
    # ==================== TEST PROCESS METHOD ====================
    def test_process_output_structure(self):
        """Test kết quả process có đủ trường"""
        text = "Phản hồi này rất tốt"
        result = self.analyzer.process(text)
        
        # Kiểm tra các trường bắt buộc
        self.assertIn("sentiment", result)
        self.assertIn("keywords", result)
        self.assertIn("confidence", result)
        self.assertIn("lang", result)
        print("✅ Test process output structure: PASSED")
    
    def test_process_vietnamese_feedback(self):
        """Test xử lý phản hồi tiếng Việt"""
        text = "Khóa học này rất tốt, tôi học được rất nhiều"
        result = self.analyzer.process(text)
        
        self.assertIsNotNone(result["sentiment"])
        self.assertGreater(len(result["keywords"]), 0)
        self.assertGreater(result["confidence"], 0)
        self.assertEqual(result["lang"], "vi")
        print("✅ Test process Vietnamese: PASSED")
    
    def test_process_english_feedback(self):
        """Test xử lý phản hồi tiếng Anh"""
        text = "This course is excellent and very helpful"
        result = self.analyzer.process(text)
        
        self.assertIsNotNone(result["sentiment"])
        self.assertGreater(result["confidence"], 0)
        self.assertEqual(result["lang"], "en")
        print("✅ Test process English: PASSED")
    
    def test_process_edge_case_handling(self):
        """Test xử lý edge case trong process"""
        text = "Hi"
        result = self.analyzer.process(text)
        
        self.assertEqual(result["sentiment"], "neutral")
        self.assertEqual(result["confidence"], 0.5)
        self.assertIn("error", result)
        print("✅ Test process edge case: PASSED")
    
    # ==================== TEST KEYWORD EXTRACTION ====================
    def test_keywords_not_stopwords(self):
        """Test từ khóa trích xuất không chứa stopwords"""
        text = "Phản hồi này rất tốt và hay"
        result = self.analyzer.process(text)
        keywords = result["keywords"]
        
        # Kiểm tra stopwords không có trong keywords
        for keyword in keywords:
            self.assertNotIn(keyword.lower(), self.analyzer.stopwords)
        print("✅ Test keywords exclude stopwords: PASSED")
    
    def test_keywords_extraction(self):
        """Test trích xuất từ khóa"""
        text = "Khóa học lập trình Python rất tuyệt vời"
        result = self.analyzer.process(text)
        
        self.assertGreater(len(result["keywords"]), 0)
        print("✅ Test keywords extraction: PASSED")
    
    # ==================== TEST EDGE CASES & ERROR HANDLING ====================
    def test_empty_string(self):
        """Test xử lý chuỗi rỗng"""
        result = self.analyzer.process("")
        self.assertEqual(result["sentiment"], "neutral")
        print("✅ Test empty string: PASSED")
    
    def test_very_long_text(self):
        """Test xử lý text rất dài"""
        text = "Phản hồi " * 1000
        result = self.analyzer.process(text)
        self.assertIsNotNone(result["sentiment"])
        print("✅ Test very long text: PASSED")
    
    def test_special_characters_handling(self):
        """Test xử lý ký tự đặc biệt"""
        text = "Phản hồi này: tốt! (rất hay) @#$"
        result = self.analyzer.process(text)
        self.assertIsNotNone(result["sentiment"])
        print("✅ Test special characters: PASSED")
    
    def test_unicode_handling(self):
        """Test xử lý Unicode"""
        text = "Phản hồi: Tốt! 🎉 Tuyệt vời! ⭐"
        result = self.analyzer.process(text)
        self.assertIsNotNone(result["sentiment"])
        print("✅ Test Unicode handling: PASSED")


class TestAnalyzerIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        self.analyzer = FeedbackAnalyzer()
    
    def test_multiple_feedbacks_sequence(self):
        """Test xử lý nhiều phản hồi liên tiếp"""
        feedbacks = [
            "Khóa học này rất tốt",
            "Thực sự không thích",
            "Bình thường thôi",
            "Tuyệt vời lắm!",
            "Tệ quá"
        ]
        
        results = []
        for feedback in feedbacks:
            result = self.analyzer.process(feedback)
            results.append(result)
            self.assertIsNotNone(result["sentiment"])
        
        self.assertEqual(len(results), len(feedbacks))
        print("✅ Test multiple feedbacks: PASSED")
    
    def test_consistency(self):
        """Test kết quả nhất quán khi gọi lại"""
        text = "Phản hồi tuyệt vời"
        result1 = self.analyzer.process(text)
        result2 = self.analyzer.process(text)
        
        self.assertEqual(result1["sentiment"], result2["sentiment"])
        self.assertEqual(result1["confidence"], result2["confidence"])
        print("✅ Test consistency: PASSED")


def run_tests():
    """Chạy tất cả tests"""
    print("\n" + "="*60)
    print("RUNNING FEEDBACK ANALYZER UNIT TESTS")
    print("="*60 + "\n")
    
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm tất cả tests
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzerIntegration))
    
    # Chạy tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
