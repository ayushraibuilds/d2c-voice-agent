"""
Unit tests for lang_detect.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lang_detect import detect, LangResult


class TestDetect:
    def test_empty_string_defaults_to_english(self):
        result = detect("")
        assert result.lang_code == "en"
        assert result.method == "default"

    def test_whitespace_only_defaults_to_english(self):
        result = detect("   ")
        assert result.lang_code == "en"
        assert result.method == "default"

    def test_english_message(self):
        result = detect("Where is my order? I haven't received it yet.")
        assert result.lang_code == "en"
        assert result.confidence > 0

    def test_devanagari_script_detected_as_hindi(self):
        result = detect("मेरा ऑर्डर कहाँ है?")
        assert result.lang_code == "hi"
        assert result.method == "script"
        assert result.confidence >= 0.9

    def test_hinglish_keyword_detection(self):
        # Contains "mera order" and "kahan" — should hit keyword heuristic
        result = detect("mera order kahan hai? abhi tak nahi aaya")
        assert result.lang_code == "hi"
        assert result.method == "keyword"
        assert result.confidence >= 0.9

    def test_tamil_script_detection(self):
        result = detect("என் ஆர்டர் எங்கே?")
        assert result.lang_code == "ta"
        assert result.method == "script"

    def test_telugu_script_detection(self):
        result = detect("నా ఆర్డర్ ఎక్కడ ఉంది?")
        assert result.lang_code == "te"
        assert result.method == "script"

    def test_kannada_script_detection(self):
        result = detect("ನನ್ನ ಆರ್ಡರ್ ಎಲ್ಲಿದೆ?")
        assert result.lang_code == "kn"
        assert result.method == "script"

    def test_bengali_script_detection(self):
        result = detect("আমার অর্ডার কোথায়?")
        assert result.lang_code == "bn"
        assert result.method == "script"

    def test_result_is_lang_result_instance(self):
        result = detect("Hello!")
        assert isinstance(result, LangResult)
        assert hasattr(result, "lang_code")
        assert hasattr(result, "confidence")
        assert hasattr(result, "method")

    def test_single_hinglish_keyword_not_enough(self):
        # Only one keyword present, fallback to langdetect/default
        result = detect("refund please")
        # Should NOT be keyword-detected since only 1 keyword match
        assert result.method != "keyword"

    def test_confidence_range(self):
        result = detect("मुझे रिफंड चाहिए")
        assert 0.0 <= result.confidence <= 1.0
