#!/usr/bin/env python3
"""
Script to generate secure random secrets for environment variables.
This script generates cryptographically secure random strings for use as
secret keys, passwords, and other sensitive configuration values.
"""

import secrets
import string
import os
from pathlib import Path

def generate_secure_string(length=32, include_special=True):
    """Generate a secure random string."""
    if include_special:
        # Include alphanumeric and special characters
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    else:
        # Alphanumeric only
        characters = string.ascii_letters + string.digits
    
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_url_safe_string(length=32):
    """Generate a URL-safe random string."""
    return secrets.token_urlsafe(length)

def create_env_file():
    """Create a .env file with secure random values."""
    
    # Check if .env file already exists
    env_path = Path("backend/.env")
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Aborting. Existing .env file preserved.")
            return
    
    # Generate secure values
    env_content = f"""# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cipherquest_db
DB_USER=root
DB_PASSWORD={generate_secure_string(16, include_special=True)}

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY={generate_url_safe_string(32)}

# JWT Configuration
JWT_SECRET_KEY={generate_url_safe_string(32)}
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Security Configuration
BCRYPT_LOG_ROUNDS=12
RATE_LIMIT_PER_MINUTE=60

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Requested-With

# Security Headers Configuration
STRICT_TRANSPORT_SECURITY=max-age=31536000; includeSubDomains
CONTENT_SECURITY_POLICY=default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:; frame-ancestors 'none';

# Docker Environment Variables
MYSQL_ROOT_PASSWORD={generate_secure_string(16, include_special=True)}
"""
    
    # Create backend directory if it doesn't exist
    env_path.parent.mkdir(exist_ok=True)
    
    # Write the .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created secure .env file at {env_path}")
    print("\n🔐 Generated secure values:")
    print(f"   - Database Password: {env_content.split('DB_PASSWORD=')[1].split()[0]}")
    print(f"   - Flask Secret Key: {env_content.split('SECRET_KEY=')[1].split()[0]}")
    print(f"   - JWT Secret Key: {env_content.split('JWT_SECRET_KEY=')[1].split()[0]}")
    print(f"   - MySQL Root Password: {env_content.split('MYSQL_ROOT_PASSWORD=')[1].split()[0]}")
    
    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("1. Keep this .env file secure and never commit it to version control")
    print("2. Use different values for production environments")
    print("3. Regularly rotate these secrets")
    print("4. Store production secrets in a secure secret management system")

def main():
    """Main function."""
    print("🔐 CipherQuest Secure Environment Generator")
    print("=" * 50)
    
    try:
        create_env_file()
        print("\n🎉 Environment file created successfully!")
        print("\nNext steps:")
        print("1. Review and customize the generated .env file")
        print("2. Set up your database with the generated password")
        print("3. Configure OAuth providers if needed")
        print("4. Set your OpenAI API key if using AI features")
        print("5. Run: docker-compose up --build")
        
    except Exception as e:
        print(f"❌ Error creating environment file: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 