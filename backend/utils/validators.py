import re
import html
import unicodedata
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
import bleach
from werkzeug.security import safe_str_cmp

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def sanitize_input(text: str, max_length: int = 1000, allow_html: bool = False) -> str:
    """
    Comprehensive input sanitization to prevent XSS and injection attacks.
    
    Args:
        text (str): The input text to sanitize
        max_length (int): Maximum allowed length
        allow_html (bool): Whether to allow safe HTML tags
    
    Returns:
        str: The sanitized text
    """
    if not text:
        return ""
    
    # Convert to string if needed
    text = str(text)
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Remove null bytes and control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    
    if allow_html:
        # Allow only safe HTML tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'code', 'pre']
        allowed_attrs = {}
        text = bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    else:
        # Escape HTML entities
        text = html.escape(text)
    
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
        r'<form[^>]*>',
        r'<input[^>]*>',
        r'<textarea[^>]*>',
        r'<select[^>]*>',
        r'<button[^>]*>',
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    return text.strip()

def validate_email(email: str) -> bool:
    """
    Enhanced email validation with additional security checks.
    
    Args:
        email (str): The email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    # Check length
    if len(email) > 254:  # RFC 5321 limit
        return False
    
    # Enhanced email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'\.\.',  # Double dots
        r'\.-',   # Dot followed by dash
        r'-\.',   # Dash followed by dot
        r'^\.',   # Starts with dot
        r'\.$',   # Ends with dot
        r'@\.',   # @ followed by dot
        r'\.@',   # Dot followed by @
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, email):
            return False
    
    return True

def validate_password(password: str) -> bool:
    """
    Enhanced password strength validation.
    
    Args:
        password (str): The password to validate
    
    Returns:
        bool: True if strong, False otherwise
    """
    if not password or not isinstance(password, str):
        return False
    
    # Check length
    if len(password) < 8 or len(password) > 128:
        return False
    
    # Check for common weak passwords
    weak_passwords = [
        'password', '123456', 'qwerty', 'admin', 'user',
        'letmein', 'welcome', 'monkey', 'dragon', 'master'
    ]
    
    if password.lower() in weak_passwords:
        return False
    
    # Check character requirements
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    # Require at least 3 out of 4 character types
    char_types = sum([has_upper, has_lower, has_digit, has_special])
    if char_types < 3:
        return False
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        return False
    
    # Check for sequential characters
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        return False
    
    return True

def validate_username(username: str) -> bool:
    """
    Enhanced username validation with security considerations.
    
    Args:
        username (str): The username to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    username = username.strip()
    
    # Check length
    if len(username) < 3 or len(username) > 30:
        return False
    
    # Username should only contain alphanumeric characters, underscores, and hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    if not re.match(pattern, username):
        return False
    
    # Check for reserved usernames
    reserved_usernames = [
        'admin', 'administrator', 'root', 'system', 'support',
        'help', 'info', 'mail', 'webmaster', 'noreply', 'test',
        'guest', 'anonymous', 'null', 'undefined', 'api'
    ]
    
    if username.lower() in reserved_usernames:
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'^[0-9]+$',  # All numbers
        r'\.\.',      # Double dots
        r'__',        # Double underscores
        r'--',        # Double dashes
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, username):
            return False
    
    return True

def validate_flag_format(flag: str) -> bool:
    """
    Enhanced CTF flag validation with security checks.
    
    Args:
        flag (str): The flag string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not flag or not isinstance(flag, str):
        return False
    
    flag = flag.strip()
    
    # Check length
    if len(flag) < 3 or len(flag) > 100:
        return False
    
    # Common CTF flag formats
    flag_patterns = [
        r'^flag\{[^}]{1,80}\}$',      # flag{...} with content limit
        r'^CTF\{[^}]{1,80}\}$',       # CTF{...} with content limit
        r'^picoCTF\{[^}]{1,80}\}$',   # picoCTF{...} with content limit
        r'^[a-zA-Z0-9_\-]{3,50}$'     # Simple alphanumeric flags
    ]
    
    if not any(re.match(pattern, flag) for pattern in flag_patterns):
        return False
    
    # Check for suspicious content
    suspicious_patterns = [
        r'<script', r'javascript:', r'vbscript:', r'on\w+\s*=',
        r'<iframe', r'<object', r'<embed', r'<form', r'<input'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, flag, re.IGNORECASE):
            return False
    
    return True

def validate_url(url: str) -> bool:
    """
    Validate and sanitize URLs.
    
    Args:
        url (str): The URL to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'javascript:', r'vbscript:', r'data:', r'file:',
            r'<script', r'<iframe', r'<object', r'<embed'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False
        
        return True
    except Exception:
        return False

def sanitize_url(url: str) -> str:
    """
    Sanitize URL input.
    
    Args:
        url (str): The URL to sanitize
    
    Returns:
        str: The sanitized URL
    """
    if not url:
        return ""
    
    url = str(url).strip()
    
    # Remove dangerous protocols
    dangerous_protocols = ['javascript:', 'vbscript:', 'data:', 'file:']
    for protocol in dangerous_protocols:
        if url.lower().startswith(protocol):
            return ""
    
    # Ensure HTTPS for external URLs
    if url.startswith('http://'):
        url = url.replace('http://', 'https://', 1)
    
    return url

def validate_json_data(data: Dict[str, Any], required_fields: List[str] = None, 
                      optional_fields: Dict[str, type] = None) -> Dict[str, Any]:
    """
    Validate and sanitize JSON data.
    
    Args:
        data (dict): The JSON data to validate
        required_fields (list): List of required field names
        optional_fields (dict): Dict of optional field names and their types
    
    Returns:
        dict: The validated and sanitized data
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary")
    
    validated_data = {}
    
    # Validate required fields
    if required_fields:
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"Required field '{field}' is missing")
            validated_data[field] = data[field]
    
    # Validate optional fields
    if optional_fields:
        for field, field_type in optional_fields.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], field_type):
                    raise ValidationError(f"Field '{field}' must be of type {field_type.__name__}")
                validated_data[field] = data[field]
    
    return validated_data

def sanitize_user_input(input_data: Any, field_type: str = 'text') -> Any:
    """
    Sanitize user input based on field type.
    
    Args:
        input_data: The input data to sanitize
        field_type (str): The type of field ('text', 'email', 'username', 'url', 'flag')
    
    Returns:
        The sanitized input data
    """
    if input_data is None:
        return None
    
    if field_type == 'text':
        return sanitize_input(str(input_data))
    elif field_type == 'email':
        email = str(input_data).strip().lower()
        return email if validate_email(email) else ""
    elif field_type == 'username':
        username = str(input_data).strip()
        return username if validate_username(username) else ""
    elif field_type == 'url':
        return sanitize_url(str(input_data))
    elif field_type == 'flag':
        flag = str(input_data).strip()
        return flag if validate_flag_format(flag) else ""
    else:
        return sanitize_input(str(input_data))

def validate_rate_limit_key(key: str) -> bool:
    """
    Validate rate limiting key format.
    
    Args:
        key (str): The rate limiting key to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not key or not isinstance(key, str):
        return False
    
    # Rate limit keys should be alphanumeric with limited special characters
    pattern = r'^[a-zA-Z0-9_\-\.:]+$'
    return bool(re.match(pattern, key))

def sanitize_sql_like_pattern(pattern: str) -> str:
    """
    Sanitize SQL LIKE pattern to prevent injection.
    
    Args:
        pattern (str): The pattern to sanitize
    
    Returns:
        str: The sanitized pattern
    """
    if not pattern:
        return ""
    
    # Escape SQL LIKE special characters
    pattern = str(pattern)
    pattern = pattern.replace('%', '\\%')
    pattern = pattern.replace('_', '\\_')
    pattern = pattern.replace('[', '\\[')
    pattern = pattern.replace(']', '\\]')
    
    return sanitize_input(pattern)

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension for security.
    
    Args:
        filename (str): The filename to validate
        allowed_extensions (list): List of allowed file extensions
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not filename or not isinstance(filename, str):
        return False
    
    # Get file extension
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Check if extension is allowed
    return extension in [ext.lower() for ext in allowed_extensions]

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename (str): The filename to sanitize
    
    Returns:
        str: The sanitized filename
    """
    if not filename:
        return ""
    
    filename = str(filename)
    
    # Remove path traversal characters
    filename = filename.replace('..', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    
    # Remove dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename.strip()

def constant_time_compare(a: str, b: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks.
    
    Args:
        a (str): First string
        b (str): Second string
    
    Returns:
        bool: True if strings are equal, False otherwise
    """
    return safe_str_cmp(a, b) 