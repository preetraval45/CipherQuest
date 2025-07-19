#!/usr/bin/env python3
"""
Simple run script for CipherQuest Flask backend
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting CipherQuest Backend...")
    print("📍 API will be available at: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/api/health")
    print("📚 API Documentation: Check README.md")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    ) 