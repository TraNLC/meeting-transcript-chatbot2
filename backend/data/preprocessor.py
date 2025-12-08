"""Text preprocessing."""


class TranscriptPreprocessor:
    """Tiền xử lý transcript text."""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Làm sạch text.

        Args:
            text: Text cần làm sạch

        Returns:
            Text đã được làm sạch
        """
        # Remove multiple spaces
        text = " ".join(text.split())
        # Remove multiple newlines
        text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])
        return text.strip()
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 15000) -> str:
        """
        Cắt ngắn text nếu quá dài.

        Args:
            text: Text cần cắt
            max_length: Độ dài tối đa

        Returns:
            Text đã được cắt
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "\n\n[... Transcript đã được cắt ngắn ...]"
