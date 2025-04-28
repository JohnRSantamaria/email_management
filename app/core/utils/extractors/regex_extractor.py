import re
from typing import Dict, List
from app.core.utils.validators.number_validator import NumberValidator


class RegexExtractor:
    def __init__(self):
        self.patterns = {
            "nif": r"(?i)(?:^|\\n|\s)N\.?\s*I\.?\s*F\.?\s+([^\s|\\]+)",
            "cif": r"(?i)(?:^|\\n|\s)C\.?\s*I\.?\s*F\.?\s+([^\s|\\|,]+)",
            "vat": r"(?i)(?:^|\\n|\s)V\.?\s*A\.?\s*T(?:\s*No:?)?(?:\s*ID:?)?\.?\s+([^\s|\\]+)",
            "cf": r"(?i)(?:^|\\n|\s)C\.?\s*F(?:\s*No:?)?(?:\s*ID:?)?\.?\s+([^\s|\\]+)",
            "es": r"(?i)(?:^|\\n|\s)E\.?\s*S(?:\s*No:?)?(?:\s*ID:?)?\.?([^\s|\\]+)",
            "b": r"(?:^|\\n|\s)(B(?:\s)?(?=[A-Z0-9]*\d)[A-Z0-9]+)",  # No permite alfabeticos.
        }

    def extract_with_pattern(self, text: str, pattern_key: str) -> List[str]:
        """Extracts matches based on a named regex pattern."""
        regex = re.compile(self.patterns[pattern_key])
        matches = regex.findall(text)
        return [m for m in matches if NumberValidator.contains_number(m)]

    def extract_all_patterns(self, text: str) -> Dict[str, List[str]]:
        """Extracts all matches for all patterns."""
        results = set()
        for _, pattern in self.patterns.items():
            regex = re.compile(pattern)
            matches = regex.findall(text)
            valid_matches = [m for m in matches if NumberValidator.contains_number(m)]
            results.update(valid_matches)

        return list(results)
