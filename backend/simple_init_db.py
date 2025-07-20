#!/usr/bin/env python3
"""
Simple database initialization script for CipherQuest
Creates tables and populates with initial seed data
"""

import os
import sys
from datetime import datetime
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database configuration
DB_CONFIG = {
    'host': 'db',  # Docker service name
    'port': 3306,
    'user': 'root',
    'password': 'Arjun@231',
    'database': 'cipherquest_db',
    'charset': 'utf8mb4'
}

def create_tables():
    """Create database tables using raw SQL"""
    print("🔧 Creating database tables...")
    
    try:
        # Connect to MySQL
        connection = pymysql.connect(**DB_CONFIG)
        
        with connection.cursor() as cursor:
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    is_admin BOOLEAN DEFAULT FALSE,
                    email_verified BOOLEAN DEFAULT FALSE,
                    level INT DEFAULT 1,
                    experience INT DEFAULT 0,
                    user_rank VARCHAR(20) DEFAULT 'Novice',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Create modules table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS modules (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    content LONGTEXT,
                    category VARCHAR(50),
                    difficulty VARCHAR(20),
                    order_num INT,
                    estimated_time INT,
                    points INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Create challenges table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS challenges (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    category VARCHAR(50),
                    difficulty VARCHAR(20),
                    points INT DEFAULT 0,
                    hints JSON,
                    module_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (module_id) REFERENCES modules(id)
                )
            """)
            
            # Create flags table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    flag_value VARCHAR(255) NOT NULL,
                    challenge_id INT,
                    points INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
                )
            """)
            
            # Create user_progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    module_id INT,
                    challenge_id INT,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP NULL,
                    score INT DEFAULT 0,
                    attempts INT DEFAULT 0,
                    time_spent INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (module_id) REFERENCES modules(id),
                    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
                )
            """)
            
            # Create leaderboard_entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard_entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    total_score INT DEFAULT 0,
                    modules_completed INT DEFAULT 0,
                    challenges_completed INT DEFAULT 0,
                    leaderboard_rank INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            connection.commit()
            print("✅ Database tables created successfully!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_seed_data():
    """Insert seed data into the database"""
    print("🌱 Inserting seed data...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        
        with connection.cursor() as cursor:
            # Check if seed data already exists
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count > 0:
                print("📋 Seed data already exists. Skipping...")
                return True
            
            # Insert admin user
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, is_admin, email_verified, level, experience, user_rank)
                VALUES ('admin', 'admin@cipherquest.com', 'Admin123!', 'Admin', 'User', TRUE, TRUE, 100, 10000, 'Master')
            """)
            
            # Insert demo users
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, level, experience, user_rank)
                VALUES 
                ('hacker1', 'hacker1@example.com', 'Password123!', 'Alice', 'Hacker', 15, 1500, 'Expert'),
                ('hacker2', 'hacker2@example.com', 'Password123!', 'Bob', 'Security', 8, 800, 'Advanced'),
                ('newbie', 'newbie@example.com', 'Password123!', 'Charlie', 'Learner', 2, 150, 'Novice')
            """)
            
            # Insert modules
            cursor.execute("""
                INSERT INTO modules (title, description, content, category, difficulty, order_num, estimated_time, points)
                VALUES 
                ('Introduction to Cryptography', 'Learn the basics of cryptography, including encryption, decryption, and common algorithms.', '# Introduction to Cryptography\n\nCryptography is the practice and study of techniques for secure communication in the presence of third parties.\n\n## Key Concepts:\n- **Encryption**: Converting plaintext to ciphertext\n- **Decryption**: Converting ciphertext back to plaintext\n- **Key**: Secret information used in encryption/decryption\n- **Algorithm**: Mathematical procedure for encryption/decryption', 'Cryptography', 'Beginner', 1, 30, 10),
                ('Web Security Fundamentals', 'Understand common web vulnerabilities and how to protect against them.', '# Web Security Fundamentals\n\nWeb security is crucial in today''s interconnected world.\n\n## Common Vulnerabilities:\n- **SQL Injection**: Malicious SQL code injection\n- **XSS (Cross-Site Scripting)**: Client-side code injection\n- **CSRF (Cross-Site Request Forgery)**: Unauthorized commands', 'Web Security', 'Beginner', 2, 45, 15)
            """)
            
            # Insert challenges
            cursor.execute("""
                INSERT INTO challenges (title, description, category, difficulty, points, hints, module_id)
                VALUES 
                ('Caesar Cipher', 'Decrypt this message encrypted with a Caesar cipher: "KHOOR ZRUOG" (shift = 3)', 'Cryptography', 'Easy', 10, '["The shift is 3 positions backward in the alphabet"]', 1),
                ('Vigenère Cipher', 'Decrypt this message: "LXFOPVEFRNHR" using the key "LEMON"', 'Cryptography', 'Medium', 20, '["Use the Vigenère square or calculate manually"]', 1),
                ('SQL Injection', 'Find the admin password by exploiting the login form at /admin/login', 'Web Security', 'Medium', 25, '["Try using single quotes and OR statements"]', 2),
                ('XSS Challenge', 'Execute JavaScript in the comment section to steal cookies', 'Web Security', 'Hard', 30, '["Try using <script> tags or event handlers"]', 2)
            """)
            
            # Insert flags
            cursor.execute("""
                INSERT INTO flags (flag_value, challenge_id, points)
                VALUES 
                ('HELLO WORLD', 1, 10),
                ('ATTACKATDAWN', 2, 20),
                ('admin123', 3, 25),
                ('flag{xss_success}', 4, 30)
            """)
            
            # Insert progress data
            cursor.execute("""
                INSERT INTO user_progress (user_id, module_id, completed, completed_at, score, attempts, time_spent)
                VALUES 
                (2, 1, TRUE, NOW(), 10, 1, 1800),
                (2, 1, TRUE, NOW(), 10, 2, 900),
                (3, 1, TRUE, NOW(), 10, 1, 2000),
                (4, 1, FALSE, NULL, 0, 3, 1500)
            """)
            
            # Insert leaderboard entries
            cursor.execute("""
                INSERT INTO leaderboard_entries (user_id, total_score, modules_completed, challenges_completed, leaderboard_rank)
                VALUES 
                (1, 0, 0, 0, 1),
                (2, 20, 1, 1, 2),
                (3, 10, 1, 0, 3),
                (4, 0, 0, 0, 4)
            """)
            
            connection.commit()
            print("✅ Seed data inserted successfully!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error inserting seed data: {e}")
        return False

def main():
    """Main function to initialize database"""
    print("🚀 CipherQuest Database Initialization")
    print("=" * 50)
    
    # Step 1: Create tables
    if not create_tables():
        print("❌ Failed to create tables!")
        return False
    
    # Step 2: Insert seed data
    if not insert_seed_data():
        print("❌ Failed to insert seed data!")
        return False
    
    print("\n🎉 Database initialization completed successfully!")
    print("\n📋 What was created:")
    print("   ✅ Database: cipherquest_db")
    print("   ✅ Tables: users, modules, challenges, flags, user_progress, leaderboard_entries")
    print("   ✅ Seed data: 4 users, 2 modules, 4 challenges, 4 flags, progress tracking")
    
    print("\n🔑 Default login credentials:")
    print("   Admin: admin@cipherquest.com / Admin123!")
    print("   User 1: hacker1@example.com / Password123!")
    print("   User 2: hacker2@example.com / Password123!")
    print("   User 3: newbie@example.com / Password123!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 