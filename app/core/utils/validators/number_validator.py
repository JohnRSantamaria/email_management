class NumberValidator:
    @staticmethod
    def contains_number(text: str) -> bool:
        """Verify if the code has at least one number."""
        return any(c.isdigit() for c in text)
