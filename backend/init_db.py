#!/usr/bin/env python3
"""
Database initialization script for CipherQuest
Creates tables and populates with initial seed data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.user import db as user_db, User
from models.module import db as module_db, Module
from models.challenge import db as challenge_db, Challenge, Flag
from models.progress import db as progress_db, UserProgress
from models.leaderboard import db as leaderboard_db, LeaderboardEntry

def init_database():
    """Initialize database with tables and seed data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        user_db.create_all()
        module_db.create_all()
        challenge_db.create_all()
        progress_db.create_all()
        leaderboard_db.create_all()
        
        print("Database tables created successfully!")
        
        # Check if seed data already exists
        if User.query.first():
            print("Seed data already exists. Skipping...")
            return
        
        print("Populating database with seed data...")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@cipherquest.com',
            password='Admin123!',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            email_verified=True,
            level=100,
            experience=10000,
            rank='Master'
        )
        user_db.session.add(admin_user)
        
        # Create sample users
        sample_users = [
            User(
                username='hacker1',
                email='hacker1@example.com',
                password='Password123!',
                first_name='Alice',
                last_name='Hacker',
                level=15,
                experience=1500,
                rank='Expert'
            ),
            User(
                username='hacker2',
                email='hacker2@example.com',
                password='Password123!',
                first_name='Bob',
                last_name='Security',
                level=8,
                experience=800,
                rank='Advanced'
            ),
            User(
                username='newbie',
                email='newbie@example.com',
                password='Password123!',
                first_name='Charlie',
                last_name='Learner',
                level=2,
                experience=150,
                rank='Novice'
            )
        ]
        
        for user in sample_users:
            user_db.session.add(user)
        
        user_db.session.commit()
        print("Users created successfully!")
        
        # Create modules
        modules = [
            Module(
                title='Introduction to Cryptography',
                description='Learn the basics of cryptography, including encryption, decryption, and common algorithms.',
                content='''
# Introduction to Cryptography

Cryptography is the practice and study of techniques for secure communication in the presence of third parties.

## Key Concepts:
- **Encryption**: Converting plaintext to ciphertext
- **Decryption**: Converting ciphertext back to plaintext
- **Key**: Secret information used in encryption/decryption
- **Algorithm**: Mathematical procedure for encryption/decryption

## Common Algorithms:
1. **Caesar Cipher**: Simple substitution cipher
2. **Vigenère Cipher**: Polyalphabetic substitution cipher
3. **RSA**: Public-key cryptography
4. **AES**: Advanced Encryption Standard
                ''',
                category='Cryptography',
                difficulty='Beginner',
                order=1,
                estimated_time=30,
                points=10
            ),
            Module(
                title='Web Security Fundamentals',
                description='Understand common web vulnerabilities and how to protect against them.',
                content='''
# Web Security Fundamentals

Web security is crucial in today's interconnected world.

## Common Vulnerabilities:
- **SQL Injection**: Malicious SQL code injection
- **XSS (Cross-Site Scripting)**: Client-side code injection
- **CSRF (Cross-Site Request Forgery)**: Unauthorized commands
- **File Upload Vulnerabilities**: Malicious file uploads

## Protection Methods:
1. Input validation and sanitization
2. Prepared statements
3. Content Security Policy (CSP)
4. CSRF tokens
                ''',
                category='Web Security',
                difficulty='Beginner',
                order=2,
                estimated_time=45,
                points=15
            ),
            Module(
                title='Network Security',
                description='Learn about network protocols, vulnerabilities, and security measures.',
                content='''
# Network Security

Network security involves protecting network infrastructure and data.

## Key Topics:
- **TCP/IP Protocol Stack**
- **Network Scanning and Enumeration**
- **Packet Analysis**
- **Firewall Configuration**
- **Intrusion Detection Systems**

## Common Attacks:
1. Man-in-the-Middle (MITM)
2. Denial of Service (DoS)
3. ARP Spoofing
4. DNS Spoofing
                ''',
                category='Network Security',
                difficulty='Intermediate',
                order=3,
                estimated_time=60,
                points=20
            ),
            Module(
                title='Reverse Engineering',
                description='Learn to analyze and understand compiled programs and malware.',
                content='''
# Reverse Engineering

Reverse engineering is the process of analyzing software to understand its functionality.

## Tools and Techniques:
- **Disassemblers**: Convert machine code to assembly
- **Debuggers**: Step through program execution
- **Decompilers**: Convert machine code to high-level language
- **Static Analysis**: Analyze code without execution
- **Dynamic Analysis**: Analyze code during execution

## Common Targets:
1. Malware analysis
2. Software security assessment
3. Protocol analysis
4. Legacy system understanding
                ''',
                category='Reverse Engineering',
                difficulty='Advanced',
                order=4,
                estimated_time=90,
                points=30
            )
        ]
        
        for module in modules:
            module_db.session.add(module)
        
        module_db.session.commit()
        print("Modules created successfully!")
        
        # Create challenges
        challenges = [
            Challenge(
                title='Caesar Cipher',
                description='Decrypt this message encrypted with a Caesar cipher: "KHOOR ZRUOG" (shift = 3)',
                category='Cryptography',
                difficulty='Easy',
                points=10,
                hints=['The shift is 3 positions backward in the alphabet'],
                module_id=1
            ),
            Challenge(
                title='Vigenère Cipher',
                description='Decrypt this message: "LXFOPVEFRNHR" using the key "LEMON"',
                category='Cryptography',
                difficulty='Medium',
                points=20,
                hints=['Use the Vigenère square or calculate manually'],
                module_id=1
            ),
            Challenge(
                title='SQL Injection',
                description='Find the admin password by exploiting the login form at /admin/login',
                category='Web Security',
                difficulty='Medium',
                points=25,
                hints=['Try using single quotes and OR statements'],
                module_id=2
            ),
            Challenge(
                title='XSS Challenge',
                description='Execute JavaScript in the comment section to steal cookies',
                category='Web Security',
                difficulty='Hard',
                points=30,
                hints=['Try using <script> tags or event handlers'],
                module_id=2
            ),
            Challenge(
                title='Network Traffic Analysis',
                description='Analyze the provided pcap file and find the secret message',
                category='Network Security',
                difficulty='Medium',
                points=25,
                hints=['Look for HTTP traffic and base64 encoding'],
                module_id=3
            ),
            Challenge(
                title='Binary Analysis',
                description='Reverse engineer the provided binary and find the hidden flag',
                category='Reverse Engineering',
                difficulty='Hard',
                points=40,
                hints=['Use a disassembler and look for string references'],
                module_id=4
            )
        ]
        
        for challenge in challenges:
            challenge_db.session.add(challenge)
        
        challenge_db.session.commit()
        print("Challenges created successfully!")
        
        # Create flags for challenges
        flags = [
            Flag(flag_value='HELLO WORLD', challenge_id=1, points=10),
            Flag(flag_value='ATTACKATDAWN', challenge_id=2, points=20),
            Flag(flag_value='admin123', challenge_id=3, points=25),
            Flag(flag_value='flag{xss_success}', challenge_id=4, points=30),
            Flag(flag_value='secret_message_2024', challenge_id=5, points=25),
            Flag(flag_value='flag{reverse_engineering_master}', challenge_id=6, points=40)
        ]
        
        for flag in flags:
            challenge_db.session.add(flag)
        
        challenge_db.session.commit()
        print("Flags created successfully!")
        
        # Create some sample progress
        progress_entries = [
            UserProgress(
                user_id=2,  # hacker1
                module_id=1,
                completed=True,
                completed_at=datetime.utcnow(),
                score=10,
                attempts=1,
                time_spent=1800
            ),
            UserProgress(
                user_id=2,  # hacker1
                challenge_id=1,
                completed=True,
                completed_at=datetime.utcnow(),
                score=10,
                attempts=2,
                time_spent=900
            ),
            UserProgress(
                user_id=3,  # hacker2
                module_id=1,
                completed=True,
                completed_at=datetime.utcnow(),
                score=10,
                attempts=1,
                time_spent=2000
            ),
            UserProgress(
                user_id=4,  # newbie
                module_id=1,
                completed=False,
                score=0,
                attempts=3,
                time_spent=1500
            )
        ]
        
        for progress in progress_entries:
            progress_db.session.add(progress)
        
        progress_db.session.commit()
        print("Progress entries created successfully!")
        
        # Create leaderboard entries
        leaderboard_entries = [
            LeaderboardEntry(
                user_id=1,  # admin
                total_score=0,
                modules_completed=0,
                challenges_completed=0,
                rank=1
            ),
            LeaderboardEntry(
                user_id=2,  # hacker1
                total_score=20,
                modules_completed=1,
                challenges_completed=1,
                rank=2
            ),
            LeaderboardEntry(
                user_id=3,  # hacker2
                total_score=10,
                modules_completed=1,
                challenges_completed=0,
                rank=3
            ),
            LeaderboardEntry(
                user_id=4,  # newbie
                total_score=0,
                modules_completed=0,
                challenges_completed=0,
                rank=4
            )
        ]
        
        for entry in leaderboard_entries:
            leaderboard_db.session.add(entry)
        
        leaderboard_db.session.commit()
        print("Leaderboard entries created successfully!")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nDefault credentials:")
        print("Admin: admin@cipherquest.com / Admin123!")
        print("User 1: hacker1@example.com / Password123!")
        print("User 2: hacker2@example.com / Password123!")
        print("User 3: newbie@example.com / Password123!")

if __name__ == '__main__':
    init_database() 