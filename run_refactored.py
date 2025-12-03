#!/usr/bin/env python3
"""
Entry point for the refactored Finance Tracker application.
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.main import run_app

if __name__ == '__main__':
    run_app()