#!/usr/bin/env python3
"""
Comprehensive setup verification script for CipherQuest Docker configuration.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_docker_installation():
    """Check if Docker is installed and running."""
    print("🔍 Checking Docker installation...")
    
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker installed: {result.stdout.strip()}")
        
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker Compose installed: {result.stdout.strip()}")
        
        # Check if Docker daemon is running
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, check=True)
        print("✅ Docker daemon is running")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker check failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker and Docker Compose.")
        return False

def check_docker_hub_login():
    """Check if logged into Docker Hub."""
    print("\n🔍 Checking Docker Hub login...")
    
    try:
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, check=True)
        
        if "Username" in result.stdout:
            print("✅ Logged into Docker Hub")
            return True
        else:
            print("⚠️  Not logged into Docker Hub")
            print("   Run: docker login -u preetraval45@gmail.com -p Arjuntower@231")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Could not check Docker Hub login status")
        return False

def check_required_files():
    """Check if all required files exist."""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'docker-compose.yml',
        'backend/Dockerfile',
        'frontend/Dockerfile',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/package.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_docker_compose_config():
    """Check if docker-compose.yml has required configuration."""
    print("\n🔍 Checking docker-compose.yml configuration...")
    
    try:
        with open('docker-compose.yml', 'r') as f:
            compose_content = f.read()
        
        required_env_vars = [
            'DB_HOST=db',
            'DB_USER=root',
            'DB_NAME=cipherquest_db',
            'MYSQL_DATABASE: cipherquest_db'
        ]
        
        for var in required_env_vars:
            if var in compose_content:
                print(f"✅ {var}")
            else:
                print(f"❌ {var} - NOT FOUND")
                return False
        
        # Check for environment variable usage instead of hardcoded passwords
        if 'DB_PASSWORD=' in compose_content and 'MYSQL_ROOT_PASSWORD:' in compose_content:
            print("✅ Database password configuration found")
        else:
            print("⚠️  Database password configuration not found - should use environment variables")
        
        return True
        
    except FileNotFoundError:
        print("❌ docker-compose.yml not found")
        return False

def check_database_config():
    """Check database configuration in config.py."""
    print("\n🔍 Checking database configuration...")
    
    try:
        # Read config.py
        with open('backend/config.py', 'r') as f:
            config_content = f.read()
        
        # Check for required database settings
        checks = [
            ('cipherquest_db', 'Database name configured'),
            ('mysql+pymysql', 'PyMySQL driver configured'),
            ('os.environ.get', 'Environment variables used'),
        ]
        
        for check, description in checks:
            if check in config_content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NOT FOUND")
                return False
        
        return True
        
    except FileNotFoundError:
        print("❌ backend/config.py not found")
        return False
    except Exception as e:
        print(f"❌ Error reading config.py: {e}")
        return False

def check_environment_variables():
    """Check if environment variables are properly configured."""
    print("\n🔍 Checking environment variables...")
    
    # Check if .env file exists (it should be in .gitignore)
    env_file = Path('backend/.env')
    if env_file.exists():
        print("⚠️  .env file exists (should be in .gitignore)")
    else:
        print("ℹ️  .env file not found (this is expected)")
    
    # Check docker-compose.yml for environment variables
    try:
        with open('docker-compose.yml', 'r') as f:
            compose_content = f.read()
        
        required_env_vars = [
            'DB_HOST=db',
            'DB_USER=root',
            'DB_PASSWORD=Arjun@231',
            'DB_NAME=cipherquest_db',
            'MYSQL_ROOT_PASSWORD: Arjun@231',
            'MYSQL_DATABASE: cipherquest_db'
        ]
        
        for var in required_env_vars:
            if var in compose_content:
                print(f"✅ {var}")
            else:
                print(f"❌ {var} - NOT FOUND")
                return False
        
        return True
        
    except FileNotFoundError:
        print("❌ docker-compose.yml not found")
        return False

def check_gitignore():
    """Check if sensitive files are in .gitignore."""
    print("\n🔍 Checking .gitignore...")
    
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        sensitive_files = ['.env', '__pycache__/', '*.pyc']
        
        for file in sensitive_files:
            if file in gitignore_content:
                print(f"✅ {file} in .gitignore")
            else:
                print(f"⚠️  {file} not in .gitignore")
        
        return True
        
    except FileNotFoundError:
        print("❌ .gitignore not found")
        return False

def main():
    """Run all verification checks."""
    print("🚀 CipherQuest Docker Setup Verification")
    print("=" * 50)
    
    checks = [
        check_docker_installation,
        check_docker_hub_login,
        check_required_files,
        check_docker_compose_config,
        check_database_config,
        check_environment_variables,
        check_gitignore
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
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Create a .env file in the backend directory with your configuration")
        print("2. Run: docker-compose up --build")
        print("3. Access the application at http://localhost:3000")
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\nCommon fixes:")
        print("- Install Docker and Docker Compose")
        print("- Set up environment variables in .env file")
        print("- Check file permissions")
        print("- Verify configuration files")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 