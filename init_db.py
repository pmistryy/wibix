#!/usr/bin/env python3
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from app.db.models import Base
from app.db.database import engine

def wait_for_db():
    """Wait for database to be ready"""
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Try to connect to database
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            return True
        except OperationalError:
            attempt += 1
            print(f"Waiting for database... (attempt {attempt}/{max_attempts})")
            time.sleep(2)
    
    print("Database connection failed!")
    return False

def init_database():
    """Initialize database tables"""
    if wait_for_db():
        try:
            # Create all tables
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully!")
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False
    return False

if __name__ == "__main__":
    init_database() 