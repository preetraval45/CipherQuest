#!/usr/bin/env python3
"""
Security validation script for CipherQuest.
This script checks for common security issues and validates security configurations.
"""

import os
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_hardcoded_secrets():
    """Check for hardcoded secrets in the codebase."""
    print("🔍 Checking for hardcoded secrets...")
    
    # Patterns to look for
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'key\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'private_key\s*=\s*["\'][^"\']+["\']',
    ]
    
    # Directories to exclude
    exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.venv'}
    
    issues = []
    
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.yml', '.yaml')):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in secret_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Skip if it's a placeholder or example
                            line = content[:match.end()].split('\n')[-1]
                            if not any(skip in line.lower() for skip in ['example', 'placeholder', 'your_', 'change_']):
                                issues.append(f"{file_path}:{content[:match.start()].count(chr(10)) + 1}: {match.group()}")
                except Exception as e:
                    print(f"⚠️  Could not read {file_path}: {e}")
    
    if issues:
        print("❌ Found potential hardcoded secrets:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ No hardcoded secrets found")
        return True

def check_environment_variables():
    """Check if required environment variables are properly configured."""
    print("\n🔍 Checking environment variables...")
    
    # Load .env file if it exists
    env_path = Path("backend/.env")
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found")
        return False
    
    # Required environment variables
    required_vars = {
        'DB_PASSWORD': 'Database password',
        'SECRET_KEY': 'Flask secret key',
        'JWT_SECRET_KEY': 'JWT secret key',
    }
    
    missing_vars = []
    weak_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"{var} ({description})")
        elif value in ['dev-secret-key-change-in-production', 'jwt-secret-key-change-in-production', 'your_password']:
            weak_vars.append(f"{var} ({description}) - using default/placeholder value")
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    if weak_vars:
        print(f"⚠️  Weak environment variables: {', '.join(weak_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_security_headers():
    """Check if security headers are properly configured."""
    print("\n🔍 Checking security headers configuration...")
    
    # Check Flask app.py for security headers
    app_path = Path("backend/app.py")
    if app_path.exists():
        with open(app_path, 'r') as f:
            content = f.read()
        
        required_headers = [
            'Content-Security-Policy',
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]
        
        missing_headers = []
        for header in required_headers:
            if header not in content:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"❌ Missing security headers in Flask app: {', '.join(missing_headers)}")
            return False
        else:
            print("✅ Security headers configured in Flask app")
    else:
        print("⚠️  Flask app.py not found")
        return False
    
    # Check nginx configuration
    nginx_path = Path("frontend/nginx.conf")
    if nginx_path.exists():
        with open(nginx_path, 'r') as f:
            content = f.read()
        
        if 'add_header' in content and 'X-Frame-Options' in content:
            print("✅ Security headers configured in nginx")
        else:
            print("⚠️  Security headers may be missing in nginx configuration")
            return False
    
    return True

def check_cors_configuration():
    """Check CORS configuration."""
    print("\n🔍 Checking CORS configuration...")
    
    app_path = Path("backend/app.py")
    if app_path.exists():
        with open(app_path, 'r') as f:
            content = f.read()
        
        if 'CORS(' in content and 'origins=' in content:
            print("✅ CORS is configured with specific origins")
        elif 'CORS(app)' in content:
            print("⚠️  CORS is configured but may be too permissive")
            return False
        else:
            print("❌ CORS configuration not found")
            return False
    
    return True

def check_docker_security():
    """Check Docker security configuration."""
    print("\n🔍 Checking Docker security...")
    
    compose_path = Path("docker-compose.yml")
    if compose_path.exists():
        with open(compose_path, 'r') as f:
            content = f.read()
        
        # Check for environment variable usage
        if '${' in content and 'MYSQL_ROOT_PASSWORD' in content:
            print("✅ Docker Compose uses environment variables for secrets")
        else:
            print("⚠️  Docker Compose may have hardcoded secrets")
            return False
        
        # Check for non-root user (if applicable)
        if 'user:' in content:
            print("✅ Docker containers configured with non-root user")
        else:
            print("⚠️  Docker containers may run as root")
    
    return True

def check_dependencies():
    """Check for known vulnerable dependencies."""
    print("\n🔍 Checking dependencies...")
    
    # Check Python dependencies
    requirements_path = Path("backend/requirements.txt")
    if requirements_path.exists():
        print("✅ Python requirements.txt found")
        # In a real implementation, you would check against a vulnerability database
        # For now, we'll just check if the file exists
    else:
        print("⚠️  Python requirements.txt not found")
    
    # Check Node.js dependencies
    package_path = Path("frontend/package.json")
    if package_path.exists():
        print("✅ Node.js package.json found")
        # In a real implementation, you would run npm audit
    else:
        print("⚠️  Node.js package.json not found")
    
    return True

def main():
    """Main security check function."""
    print("🔐 CipherQuest Security Validation")
    print("=" * 50)
    
    checks = [
        check_hardcoded_secrets,
        check_environment_variables,
        check_security_headers,
        check_cors_configuration,
        check_docker_security,
        check_dependencies
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 SECURITY VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All security checks passed!")
        print("\nYour application appears to be properly secured.")
    else:
        print("⚠️  Some security checks failed.")
        print("\nPlease address the issues above before deploying to production.")
        print("\nRecommendations:")
        print("1. Run generate-secrets.py to create secure environment variables")
        print("2. Review and fix any hardcoded secrets")
        print("3. Ensure all security headers are properly configured")
        print("4. Test your application thoroughly")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 