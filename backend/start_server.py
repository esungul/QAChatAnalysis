#!/usr/bin/env python3
"""
Quick start script for QA Analyzer Backend
"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    print("Starting QA Chat Analyzer Backend Server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)