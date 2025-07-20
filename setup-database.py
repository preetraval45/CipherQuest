#!/usr/bin/env python3
"""
Database setup script for CipherQuest
Creates the MySQL database and initializes it with seed data
"""

import os
import sys
import pymysql
from pathlib import Path

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Arjun@231',
    'charset': 'utf8mb4'
}

def create_database():
    """Create the cipherquest_db database"""
    print("🔧 Setting up CipherQuest database...")
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS cipherquest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'cipherquest_db' created successfully!")
            
            # Show existing databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("📋 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error creating database: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure MySQL is running")
        print("2. Verify the credentials are correct")
        print("3. Try using Docker: docker-compose up --build")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def set_environment_variables():
    """Set environment variables for the application"""
    print("\n🔧 Setting environment variables...")
    
    # Set environment variables
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '3306'
    os.environ['DB_NAME'] = 'cipherquest_db'
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASSWORD'] = 'Arjun@231'
    os.environ['SECRET_KEY'] = 'cipherquest-secret-key-change-in-production-minimum-32-characters'
    os.environ['JWT_SECRET_KEY'] = 'cipherquest-jwt-secret-key-change-in-production-minimum-32-characters'
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['CORS_ORIGINS'] = 'http://localhost:3000'
    
    print("✅ Environment variables set successfully!")

def run_database_initialization():
    """Run the database initialization script"""
    print("\n🔧 Initializing database with seed data...")
    
    try:
        # Add backend directory to Python path
        backend_path = Path("backend")
        if backend_path.exists():
            sys.path.insert(0, str(backend_path.absolute()))
            
            # Import and run the initialization script
            from init_db import init_database
            init_database()
            return True
        else:
            print("❌ Backend directory not found!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and backend dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 CipherQuest Database Setup")
    print("=" * 50)
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Database creation failed!")
        return False
    
    # Step 2: Set environment variables
    set_environment_variables()
    
    # Step 3: Run database initialization
    if not run_database_initialization():
        print("\n❌ Database initialization failed!")
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📋 What was created:")
    print("   ✅ Database: cipherquest_db")
    print("   ✅ Tables: users, modules, challenges, flags, user_progress, leaderboard_entries")
    print("   ✅ Seed data: 4 users, 4 modules, 6 challenges, 6 flags, progress tracking")
    
    print("\n🔑 Default login credentials:")
    print("   Admin: admin@cipherquest.com / Admin123!")
    print("   User 1: hacker1@example.com / Password123!")
    print("   User 2: hacker2@example.com / Password123!")
    print("   User 3: newbie@example.com / Password123!")
    
    print("\n🚀 Next steps:")
    print("1. Install backend dependencies: cd backend && pip install -r requirements.txt")
    print("2. Start the backend: cd backend && python run.py")
    print("3. Start the frontend: cd frontend && npm start")
    print("4. Or use Docker: docker-compose up --build")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 