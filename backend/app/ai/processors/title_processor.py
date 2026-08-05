import re
from typing import List, Dict
from app.ai.processors.base import BaseProcessor

POWER_WORDS = {
    "ultimate", "secret", "exploded", "shocking", "unbelievable",
    "incredible", "amazing", "revolutionary", "breakthrough", "insane",
    "epic", "massive", "huge", "crazy", "insane", "genius", "master",
    "pro", "expert", "advanced", "beginner", "complete", "full",
    "everything", "definitive", "essential", "must", "need", "best",
    "worst", "top", "perfect", "free", "new", "easy", "fast",
}


class TitleProcessor(BaseProcessor):
    async def process(self, signals: List[Dict]) -> List[Dict]:
        for signal in signals:
            title = signal.get("title", "")
            signal["title_analysis"] = self._analyze_title(title)
        return signals

    def _analyze_title(self, title: str) -> Dict:
        words = title.split()
        word_count = len(words)
        has_question = "?" in title
        has_number = bool(re.search(r'\d+', title))
        has_caps = any(w.isupper() and len(w) > 1 for w in words)
        power_word_count = sum(1 for w in words if w.lower() in POWER_WORDS)

        sentiment = 0.0
        if has_question:
            sentiment += 0.1
        if power_word_count > 0:
            sentiment += 0.2
        if has_number:
            sentiment += 0.1
        if has_caps:
            sentiment += 0.05

        return {
            "word_count": word_count,
            "has_question": has_question,
            "has_number": has_number,
            "has_caps": has_caps,
            "power_words": power_word_count,
            "sentiment": min(sentiment, 1.0),
        }
