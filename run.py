#!/usr/bin/env python3
"""
RetroForum - Simple startup script for production deployment
"""
import os
from app import app

if __name__ == '__main__':
    # Check if we're in production mode
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting RetroForum on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(host=host, port=port, debug=debug_mode)