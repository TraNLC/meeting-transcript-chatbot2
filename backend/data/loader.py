"""Transcript file loader."""

from pathlib import Path
from typing import Union
import docx


class TranscriptLoader:
    """Load transcript từ nhiều định dạng file."""

    SUPPORTED_FORMATS = [".txt", ".docx"]

    @staticmethod
    def load_file(file_path: Union[str, Path]) -> str:
        """
        Load transcript từ file.

        Args:
            file_path: Đường dẫn đến file transcript

        Returns:
            Nội dung transcript dạng text

        Raises:
            FileNotFoundError: Nếu file không tồn tại
            ValueError: Nếu định dạng file không được hỗ trợ
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        if file_path.suffix not in TranscriptLoader.SUPPORTED_FORMATS:
            raise ValueError(
                f"Định dạng file không được hỗ trợ: {file_path.suffix}. "
                f"Hỗ trợ: {', '.join(TranscriptLoader.SUPPORTED_FORMATS)}"
            )

        if file_path.suffix == ".txt":
            return TranscriptLoader._load_txt(file_path)
        elif file_path.suffix == ".docx":
            return TranscriptLoader._load_docx(file_path)

    @staticmethod
    def _load_txt(file_path: Path) -> str:
        """Load file TXT."""
        with open(file_path, "r", encoding="utf-8-sig") as f:
            return f.read()

    @staticmethod
    def _load_docx(file_path: Path) -> str:
        """Load file DOCX."""
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
