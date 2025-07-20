import pytest
from backend.utils.validators import validate_email, validate_password, validate_username, sanitize_input

class TestValidators:
    def test_validate_email_valid(self):
        """Test valid email addresses"""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'user+tag@example.org',
            '123@numbers.com'
        ]
        for email in valid_emails:
            assert validate_email(email) is True

    def test_validate_email_invalid(self):
        """Test invalid email addresses"""
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'user@',
            'user@.com',
            'user..name@example.com',
            ''
        ]
        for email in invalid_emails:
            assert validate_email(email) is False

    def test_validate_password_valid(self):
        """Test valid passwords"""
        valid_passwords = [
            'TestPass123!',
            'SecurePassword1',
            'MyP@ssw0rd',
            'LongPassword123!'
        ]
        for password in valid_passwords:
            assert validate_password(password) is True

    def test_validate_password_invalid(self):
        """Test invalid passwords"""
        invalid_passwords = [
            '123',  # Too short
            'password',  # No uppercase, numbers, or special chars
            'PASSWORD',  # No lowercase, numbers, or special chars
            'Password',  # No numbers or special chars
            '',  # Empty
            'a' * 100  # Too long
        ]
        for password in invalid_passwords:
            assert validate_password(password) is False

    def test_validate_username_valid(self):
        """Test valid usernames"""
        valid_usernames = [
            'testuser',
            'user123',
            'test_user',
            'User123',
            'a' * 20  # Max length
        ]
        for username in valid_usernames:
            assert validate_username(username) is True

    def test_validate_username_invalid(self):
        """Test invalid usernames"""
        invalid_usernames = [
            '',  # Empty
            'a',  # Too short
            'a' * 21,  # Too long
            'user@name',  # Invalid characters
            'user name',  # Spaces
            '123',  # Numbers only
            'user-name'  # Hyphens
        ]
        for username in invalid_usernames:
            assert validate_username(username) is False

    def test_sanitize_input(self):
        """Test input sanitization"""
        test_cases = [
            ('<script>alert("xss")</script>', '&lt;script&gt;alert("xss")&lt;/script&gt;'),
            ('<img src="x" onerror="alert(1)">', '&lt;img src="x" onerror="alert(1)"&gt;'),
            ('Normal text', 'Normal text'),
            ('Text with & symbols', 'Text with &amp; symbols'),
            ('', ''),
            (None, '')
        ]
        
        for input_text, expected in test_cases:
            result = sanitize_input(input_text)
            assert result == expected

    def test_sanitize_input_complex(self):
        """Test complex input sanitization scenarios"""
        complex_input = '''
        <script>alert('xss')</script>
        <img src="javascript:alert('xss')" />
        <a href="javascript:alert('xss')">Click me</a>
        <iframe src="http://evil.com"></iframe>
        '''
        
        sanitized = sanitize_input(complex_input)
        
        # Should not contain any script tags
        assert '<script>' not in sanitized
        assert '</script>' not in sanitized
        
        # Should not contain javascript: URLs
        assert 'javascript:' not in sanitized
        
        # Should contain escaped HTML
        assert '&lt;script&gt;' in sanitized
        assert '&lt;/script&gt;' in sanitized

    def test_validate_email_edge_cases(self):
        """Test email validation edge cases"""
        edge_cases = [
            ('test@example.com.', False),  # Trailing dot
            ('test..test@example.com', False),  # Consecutive dots
            ('test@example..com', False),  # Consecutive dots in domain
            ('test@-example.com', False),  # Domain starts with hyphen
            ('test@example-.com', False),  # Domain ends with hyphen
            ('test@example.com-', False),  # Domain ends with hyphen
        ]
        
        for email, expected in edge_cases:
            assert validate_email(email) == expected

    def test_validate_password_edge_cases(self):
        """Test password validation edge cases"""
        edge_cases = [
            ('Test1!', True),  # Minimum valid password
            ('Test1!a' * 10, False),  # Too long
            ('test1!', False),  # No uppercase
            ('TEST1!', False),  # No lowercase
            ('Test!', False),   # No numbers
            ('Test1', False),   # No special characters
        ]
        
        for password, expected in edge_cases:
            assert validate_password(password) == expected 