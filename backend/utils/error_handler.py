"""Error handling utilities with user-friendly messages.

Provides consistent error handling and user-friendly error messages.
"""

from typing import Tuple, Optional, Dict, Any
from functools import wraps
import traceback
from .logger import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base application error with user-friendly message."""
    
    def __init__(self, message: str, user_message: str = None, details: dict = None):
        """Initialize error.
        
        Args:
            message: Technical error message for logging
            user_message: User-friendly message for display
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.user_message = user_message or message
        self.details = details or {}


class FileValidationError(AppError):
    """File validation error."""
    pass


class APIError(AppError):
    """API call error."""
    pass


class ProcessingError(AppError):
    """Processing error."""
    pass


class StorageError(AppError):
    """Storage/database error."""
    pass


def get_user_friendly_message(error: Exception, language: str = "vi") -> str:
    """Convert exception to user-friendly message.
    
    Args:
        error: Exception to convert
        language: Language for message (vi/en)
        
    Returns:
        User-friendly error message
    """
    messages = {
        "vi": {
            "FileNotFoundError": "❌ Không tìm thấy file. Vui lòng kiểm tra lại.",
            "PermissionError": "❌ Không có quyền truy cập file. Kiểm tra quyền đọc/ghi.",
            "ValueError": "❌ Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.",
            "ConnectionError": "❌ Lỗi kết nối. Kiểm tra internet và thử lại.",
            "TimeoutError": "❌ Quá thời gian chờ. Vui lòng thử lại.",
            "KeyError": "❌ Thiếu thông tin cần thiết. Vui lòng kiểm tra lại.",
            "TypeError": "❌ Lỗi kiểu dữ liệu. Vui lòng kiểm tra định dạng.",
            "ImportError": "❌ Thiếu thư viện cần thiết. Chạy: pip install -r requirements.txt",
            "default": "❌ Đã xảy ra lỗi. Vui lòng thử lại hoặc liên hệ hỗ trợ."
        },
        "en": {
            "FileNotFoundError": "❌ File not found. Please check the file path.",
            "PermissionError": "❌ Permission denied. Check file permissions.",
            "ValueError": "❌ Invalid data. Please check your input.",
            "ConnectionError": "❌ Connection error. Check internet and retry.",
            "TimeoutError": "❌ Request timeout. Please try again.",
            "KeyError": "❌ Missing required information. Please check input.",
            "TypeError": "❌ Data type error. Please check format.",
            "ImportError": "❌ Missing required library. Run: pip install -r requirements.txt",
            "default": "❌ An error occurred. Please try again or contact support."
        }
    }
    
    lang_messages = messages.get(language, messages["vi"])
    error_type = type(error).__name__
    
    # Check if it's our custom error with user message
    if isinstance(error, AppError):
        return error.user_message
    
    # Get predefined message or default
    return lang_messages.get(error_type, lang_messages["default"])


def handle_error(func):
    """Decorator for consistent error handling.
    
    Example:
        @handle_error
        def process_file(file):
            # Your code here
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}: {str(e)}",
                exc_info=True,
                extra={"args": args, "kwargs": kwargs}
            )
            raise
    return wrapper


def safe_execute(func, *args, default=None, log_error: bool = True, **kwargs) -> Tuple[Any, Optional[Exception]]:
    """Safely execute function and return result or error.
    
    Args:
        func: Function to execute
        *args: Function arguments
        default: Default value if error occurs
        log_error: Whether to log errors
        **kwargs: Function keyword arguments
        
    Returns:
        Tuple of (result, error)
        
    Example:
        >>> result, error = safe_execute(risky_function, arg1, arg2)
        >>> if error:
        ...     print(f"Error: {error}")
        ... else:
        ...     print(f"Success: {result}")
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except Exception as e:
        if log_error:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
        return default, e


def format_error_response(error: Exception, language: str = "vi") -> Dict[str, Any]:
    """Format error as response dictionary.
    
    Args:
        error: Exception to format
        language: Language for message
        
    Returns:
        Error response dictionary
        
    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     return format_error_response(e)
    """
    user_message = get_user_friendly_message(error, language)
    
    response = {
        "success": False,
        "error": user_message,
        "error_type": type(error).__name__,
    }
    
    # Add details for custom errors
    if isinstance(error, AppError):
        response["details"] = error.details
    
    return response


def validate_file(file_path: str, max_size_mb: int = 100, allowed_extensions: list = None) -> Tuple[bool, Optional[str]]:
    """Validate file before processing.
    
    Args:
        file_path: Path to file
        max_size_mb: Maximum file size in MB
        allowed_extensions: List of allowed extensions (e.g., ['.txt', '.docx'])
        
    Returns:
        Tuple of (is_valid, error_message)
        
    Example:
        >>> is_valid, error = validate_file("test.txt", max_size_mb=10, allowed_extensions=['.txt'])
        >>> if not is_valid:
        ...     print(error)
    """
    from pathlib import Path
    
    try:
        file = Path(file_path)
        
        # Check if file exists
        if not file.exists():
            return False, "File không tồn tại"
        
        # Check if it's a file (not directory)
        if not file.is_file():
            return False, "Đường dẫn không phải là file"
        
        # Check file size
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"File quá lớn ({size_mb:.1f} MB). Tối đa {max_size_mb} MB"
        
        # Check extension
        if allowed_extensions:
            if file.suffix.lower() not in allowed_extensions:
                return False, f"Định dạng không hỗ trợ. Chỉ chấp nhận: {', '.join(allowed_extensions)}"
        
        # Check if file is readable
        try:
            with open(file, 'rb') as f:
                f.read(1)
        except PermissionError:
            return False, "Không có quyền đọc file"
        except Exception as e:
            return False, f"Không thể đọc file: {str(e)}"
        
        return True, None
        
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}", exc_info=True)
        return False, f"Lỗi kiểm tra file: {str(e)}"


def sanitize_input(text: str, max_length: int = 50000) -> str:
    """Sanitize user input text.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Truncate if too long
    if len(text) > max_length:
        logger.warning(f"Input truncated from {len(text)} to {max_length} chars")
        text = text[:max_length]
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text


def create_error_report(error: Exception, context: dict = None) -> str:
    """Create detailed error report for debugging.
    
    Args:
        error: Exception to report
        context: Additional context information
        
    Returns:
        Formatted error report
    """
    report = []
    report.append("=" * 80)
    report.append("ERROR REPORT")
    report.append("=" * 80)
    report.append(f"Error Type: {type(error).__name__}")
    report.append(f"Error Message: {str(error)}")
    report.append("")
    
    if context:
        report.append("Context:")
        for key, value in context.items():
            report.append(f"  {key}: {value}")
        report.append("")
    
    report.append("Traceback:")
    report.append(traceback.format_exc())
    report.append("=" * 80)
    
    return "\n".join(report)
