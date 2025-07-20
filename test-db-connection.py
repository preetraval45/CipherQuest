#!/usr/bin/env python3
"""
Test script to verify database connection with the specified credentials.
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def test_database_connection():
    """Test connection to MySQL database with specified credentials."""
    
    # Database configuration
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'cipherquest_db'),
        'charset': 'utf8mb4'
    }
    
    # Validate required environment variables
    if not config['password']:
        print("❌ Error: DB_PASSWORD environment variable is not set")
        print("Please set DB_PASSWORD in your .env file")
        return False
    
    print("Testing database connection with the following configuration:")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"User: {config['user']}")
    print(f"Database: {config['database']}")
    print("-" * 50)
    
    try:
        # Test connection
        connection = pymysql.connect(**config)
        print("✅ Database connection successful!")
        
        # Test if database exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            print(f"✅ Connected to database: {current_db}")
            
            # Test if we can create tables (basic permissions test)
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Database permissions OK. Found {len(tables)} tables.")
            
            if tables:
                print("Tables found:")
                for table in tables:
                    print(f"  - {table[0]}")
        
        connection.close()
        print("✅ All database tests passed!")
        return True
        
    except pymysql.Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1) 