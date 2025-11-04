from __future__ import annotations
import re
from typing import Optional, Tuple, Dict, Any

try:
    from underthesea import ner
except Exception:
    # Fallbacks if underthesea not available at lint-time
    def ner(_text: str):
        return []

from .time_parser import parse_vietnamese_time, parse_vietnamese_time_range
from datetime import datetime


class NLPPipeline:
    def __init__(self, *, relative_base: Optional[datetime] = None):
        self.relative_base = relative_base
        # Time patterns: nhận diện các mảnh thời gian rời rạc để ghép lại
        self.time_patterns = re.compile(
            r"(" 
            r"\b\d{1,2}(?:h|\s*giờ)(?:\s*\d{1,2}(?:p|\s*phút))?\b"  # 10h, 10 giờ 30 phút
            r"|\b\d{1,2}:\d{1,2}\b"                                   # 10:30
            r"|(?:ngày|ngay)\s*\d{1,2}\s*(?:tháng|thang)\s*\d{1,2}"   # ngày/ngay 6 tháng/thang 12
            r"|(?:hôm nay|hom nay|ngày mai|ngay mai|mai)"                 # hôm nay / hom nay / ngày mai / ngay mai / mai
            r"|(?:ngày mốt|ngay mot|mốt|mot|mai mốt|mai mot|ngày kia|ngay kia)" # ngày mốt / mai mốt / ngày kia
            r"|(?:sáng|sang)(?:\s+\w+)?|(?:chiều|chieu)(?:\s+\w+)?|(?:tối|toi)(?:\s+\w+)?"  # buổi
            r"|(?:cuối tuần|cuoi tuan)"                                   # cuối tuần / cuoi tuan
            r"|(?:thứ|thu)\s*\d(?:\s*(?:tuần|tuan) sau)?"               # thứ 2 tuần sau (diacriticless)
            r"|t\s*\d(?:\s*(?:tuần|tuan) sau)?"                         # t2..t7, tuan sau
            r"|cn(?:\s*(?:tuần|tuan) sau)?"                               # cn, cn tuần sau
            r"|(?:trong|sau)\s*\d{1,3}\s*(?:phút|phut|giờ|gio|ngày|ngay|tuần|tuan)"  # durations
            r"|\d{1,3}\s*(?:phút|phut|giờ|gio|ngày|ngay|tuần|tuan)\s*(?:nữa|nua)"    # X đơn vị nữa
            r"|(?:utc|gmt)\s*[+\-]?\d{1,2}(?::?\d{2})?"                # UTC+7, GMT+07:00
            r"|(?:múi|mui)\s*(?:giờ|gio)\s*(?:utc|gmt)?\s*[+\-]?\d{1,2}(?::?\d{2})?" # múi giờ +07:00 / mui gio
            r")",
            re.IGNORECASE,
        )
        # Location fallback: ở|o / tại|tai ... (tối đa một cụm, hỗ trợ không dấu)
        self.location_patterns = re.compile(r"\b(?:ở|o|tại|tai)\s+([\w\s\d./-]{1,50})", re.IGNORECASE)

        # Reminder keyword groups (có dấu và không dấu)
        verb = r"(?:nhắc(?:\s*nhở)?|nhac(?:\s*nho)?|báo\s*thức|bao\s*thuc|báo|bao|remind|notify)"
        pron = r"(?:\s*(?:tôi|toi|mình|minh|t))?"
        before = r"(?:\s*(?:trước|truoc|trc|sớm\s*hơn|som\s*hon))?"
        unit_min = r"(?:phút|phut|p|’|')"
        unit_hour = r"(?:giờ|gio|h|hr)"
        num = r"(\d{1,3})"
        # Forms: verb [pron] [before]? NUM UNIT [before]?  (covers: 'nhắc trước 10p' and 'nhắc 10p trước')
        self.reminder_min_regex1 = re.compile(fr"{verb}{pron}(?:{before}\s*)?{num}\s*{unit_min}(?:\s*(?:trước|truoc|trc))?\b", re.IGNORECASE)
        self.reminder_hour_regex1 = re.compile(fr"{verb}{pron}(?:{before}\s*)?{num}\s*{unit_hour}(?:\s*(?:trước|truoc|trc))?\b", re.IGNORECASE)
        # Forms: NUM UNIT [before] [verb] (e.g., '10p trước nhắc tôi')
        self.reminder_min_regex2 = re.compile(fr"\b{num}\s*{unit_min}{before}\s*(?:{verb})", re.IGNORECASE)
        self.reminder_hour_regex2 = re.compile(fr"\b{num}\s*{unit_hour}{before}\s*(?:{verb})", re.IGNORECASE)
        # Presence-only (no number): used to strip from text and optional boolean
        self.reminder_presence_regex = re.compile(fr"{verb}{pron}(?:\s*(?:trước|truoc|trc))?\b", re.IGNORECASE)

    def _extract_location_ner(self, text: str) -> Tuple[Optional[str], str]:
        """Sử dụng underthesea NER để ghép các token B-LOC/I-LOC thành một cụm địa điểm.
        Trả về (location, text_without_location)
        """
        try:
            entities = ner(text)
        except Exception:
            entities = []

        location_tokens = []
        capture = False
        for tok, tag in entities:
            if tag == 'B-LOC':
                if location_tokens:
                    break  # chỉ lấy cụm đầu tiên
                location_tokens = [tok]
                capture = True
            elif tag == 'I-LOC' and capture:
                location_tokens.append(tok)
            else:
                if capture:
                    break
        location = None
        if location_tokens:
            # underthesea tokenizes with underscores for spaces sometimes
            location = " ".join(t.replace('_', ' ') for t in location_tokens).strip()
            # Loại khỏi text (best-effort)
            text = re.sub(re.escape(location), "", text, flags=re.IGNORECASE).strip()
        return location, text

    def _extract_entities_regex(self, text: str) -> Dict[str, Any]:
        results: Dict[str, Any] = {
            "time_str": None,
            "location": None,
        }
        original_text = text
        # Time: ghép các mảnh liền kề lớn nhất thành một cụm
        matches = list(self.time_patterns.finditer(text))
        if matches:
            start = min(m.start() for m in matches)
            end = max(m.end() for m in matches)
            # Lưu lại tiền tố/hậu tố để fallback nếu event trống
            prefix = original_text[:start].strip(" ,.-")
            suffix = original_text[end:].strip(" ,.-")
            # Trích một đoạn bao quanh để giữ từ bổ trợ
            span = text[max(0, start-5):min(len(text), end+5)]
            span = re.sub(r"\b(vào|lúc|khoảng)\b", "", span, flags=re.IGNORECASE).strip()
            results['time_str'] = span
            # Xóa đoạn thời gian khỏi văn bản gốc
            text = (text[:start] + text[end:]).strip()
        # Location fallback
        l = self.location_patterns.search(text)
        if l and not results['location']:
            results['location'] = l.group(1).strip()
            text = text.replace(l.group(0), '').strip()
        # Remaining as event name
        results['event_name'] = re.sub(r"\b(vào|lúc|khoảng|nhắc tôi|nhắc|nhac toi|nhac|tại|ở)\b", "", text, flags=re.IGNORECASE)
        results['event_name'] = re.sub(r"\s{2,}", " ", results['event_name']).strip(' ,.-').strip()
        # Fallback: nếu event_name rỗng, thử lấy phần trước thời gian (ưu tiên) hoặc sau thời gian
        if not results['event_name'] and matches:
            # Loại bỏ từ nối khỏi prefix/suffix
            def _clean_side(s: str) -> str:
                s2 = re.sub(r"\b(vào|lúc|khoảng|tại|ở)\b", "", s, flags=re.IGNORECASE)
                s2 = re.sub(r"\s{2,}", " ", s2).strip(' ,.-').strip()
                return s2
            prefix_clean = _clean_side(prefix)
            suffix_clean = _clean_side(suffix)
            results['event_name'] = prefix_clean or suffix_clean
        return results

    def process(self, text: str) -> Dict[str, Any]:
        processed_text = text.lower() if text else ''
        # 1) Extract reminder minutes first, strip reminder phrases from text to avoid leaking into location
        reminder_minutes, text_wo_reminder, has_reminder_phrase = self._extract_reminder(processed_text)
        # 2) NER location on cleaned text then regex remainder
        loc_ner, rem_after_loc = self._extract_location_ner(text_wo_reminder)
        ex = self._extract_entities_regex(rem_after_loc)
        # Parse time
        start_dt, end_dt = parse_vietnamese_time_range(ex['time_str'], relative_base=self.relative_base)
        result = {
            'event': ex['event_name'],
            'start_time': start_dt.isoformat() if start_dt else None,
            'end_time': end_dt.isoformat() if end_dt else None,
            'location': self._clean_location_of_reminder(loc_ner or ex['location']),
            'reminder_minutes': reminder_minutes,
        }
        return result

    def _extract_reminder(self, text: str) -> Tuple[int, str, bool]:
        """Trích số phút nhắc nhở (nếu có) và loại bỏ mọi cụm từ liên quan 'nhắc tôi' khỏi text.
        Hỗ trợ cả có dấu/không dấu và các biến thể phổ biến.
        Trả về: (reminder_minutes, text_without_reminder, has_reminder_phrase)
        """
        minutes = 0
        has = False
        working = text
        # Try different forms, prioritize the first explicit number found
        for rx, factor in [
            (self.reminder_hour_regex1, 60),
            (self.reminder_min_regex1, 1),
            (self.reminder_hour_regex2, 60),
            (self.reminder_min_regex2, 1),
        ]:
            m = rx.search(working)
            if m:
                try:
                    val = int(m.group(1))
                    minutes = max(minutes, val * factor)
                except Exception:
                    pass
                has = True
                working = working.replace(m.group(0), ' ').strip()
        # If no number captured but reminder words exist, strip them
        if not has:
            if self.reminder_presence_regex.search(working):
                has = True
                working = self.reminder_presence_regex.sub(' ', working).strip()
        # Collapse multiple spaces
        working = re.sub(r"\s{2,}", " ", working)
        return minutes, working, has

    def _clean_location_of_reminder(self, loc: Optional[str]) -> Optional[str]:
        if not loc:
            return loc
        # Remove reminder keywords from location, both diacritic and non-diacritic
        loc2 = self.reminder_presence_regex.sub(' ', loc)
        loc2 = re.sub(r"\s{2,}", " ", loc2).strip(" ,.-").strip()
        return loc2 or None
