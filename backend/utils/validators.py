import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email format.
    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """
    Validate password strength.
    Args:
        password (str): The password to validate.
    Returns:
        bool: True if strong, False otherwise.
    """
    if not password or len(password) < 8:
        return False
    
    # Check for at least one uppercase, one lowercase, and one digit
    has_upper: bool = any(c.isupper() for c in password)
    has_lower: bool = any(c.islower() for c in password)
    has_digit: bool = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit

def validate_username(username: str) -> bool:
    """
    Validate username format.
    Args:
        username (str): The username to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False
    
    # Username should only contain alphanumeric characters, underscores, and hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, username))

def sanitize_input(text: str) -> str:
    """
    Basic input sanitization to prevent XSS.
    Args:
        text (str): The input text to sanitize.
    Returns:
        str: The sanitized text.
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars: list[str] = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def validate_flag_format(flag: str) -> bool:
    """
    Validate CTF flag format.
    Args:
        flag (str): The flag string to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    if not flag:
        return False
    
    # Common CTF flag formats
    flag_patterns: list[str] = [
        r'^flag\{[^}]+\}$',  # flag{...}
        r'^CTF\{[^}]+\}$',   # CTF{...}
        r'^picoCTF\{[^}]+\}$',  # picoCTF{...}
        r'^[a-zA-Z0-9_\-]{3,50}$'  # Simple alphanumeric flags
    ]
    
    return any(re.match(pattern, flag) for pattern in flag_patterns) 