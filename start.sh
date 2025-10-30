#!/bin/bash

# Render startup script for Student Management System
echo "🚀 Starting Student Management System..."

# Initialize the database
echo "📊 Initializing database..."
python -c "
import sqlite3
import os

def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            courses TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Database initialized successfully!')

init_db()
"

# Start the Flask application with Gunicorn
echo "🌐 Starting Flask application with Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app