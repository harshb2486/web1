from typing import Dict, List
import re


class EntityExtractor:
    def extract(self, message: str) -> Dict:
        entities = {}

        time_patterns = [
            (r'\b(last|past)\s+(week|month|year)\b', "timeframe"),
            (r'\b(this|current)\s+(week|month|year)\b', "timeframe"),
            (r'\b(today|yesterday|tomorrow)\b', "timeframe"),
        ]
        for pattern, entity_type in time_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities[entity_type] = match.group(0)

        name_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', message)
        if name_match:
            entities["name"] = name_match.group(1)

        number_match = re.search(r'\b(\d+(?:\.\d+)?)\s*(K|M|%|percent)?\b', message)
        if number_match:
            entities["number"] = number_match.group(0)

        return entities
