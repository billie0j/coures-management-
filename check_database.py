#!/usr/bin/env python3
"""
Database Inspection Script for Student Course Management System
This script helps you check and inspect the SQLite database contents.
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'students.db'

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DATABASE):
        print(f"❌ Database file '{DATABASE}' not found!")
        return None
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def check_database_structure():
    """Check the database structure and tables"""
    print("🔍 DATABASE STRUCTURE")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Get table information
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Tables found: {len(tables)}")
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Get table schema
            cursor = conn.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("   Columns:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] else ''}")
    
    except sqlite3.Error as e:
        print(f"❌ Error checking database structure: {e}")
    finally:
        conn.close()

def check_database_contents():
    """Check the contents of the database"""
    print("\n📊 DATABASE CONTENTS")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Count total students
        cursor = conn.execute("SELECT COUNT(*) FROM students;")
        total_students = cursor.fetchone()[0]
        print(f"👥 Total Students: {total_students}")
        
        if total_students > 0:
            print("\n📝 Student Records:")
            print("-" * 80)
            print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Courses'}")
            print("-" * 80)
            
            cursor = conn.execute("SELECT * FROM students ORDER BY name;")
            students = cursor.fetchall()
            
            for student in students:
                courses = student['courses'][:40] + "..." if len(student['courses']) > 40 else student['courses']
                print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {courses}")
        else:
            print("📭 No students found in the database.")
    
    except sqlite3.Error as e:
        print(f"❌ Error checking database contents: {e}")
    finally:
        conn.close()

def search_student_by_id():
    """Interactive search for a student by ID"""
    print("\n🔍 SEARCH STUDENT BY ID")
    print("=" * 50)
    
    student_id = input("Enter Student ID to search (or press Enter to skip): ").strip()
    if not student_id:
        return
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.execute("SELECT * FROM students WHERE student_id = ?;", (student_id,))
        student = cursor.fetchone()
        
        if student:
            print(f"\n✅ Student Found:")
            print(f"   ID: {student['student_id']}")
            print(f"   Name: {student['name']}")
            print(f"   Age: {student['age']}")
            print(f"   Courses: {student['courses']}")
            
            # Show courses as a list
            courses_list = student['courses'].split(',') if student['courses'] else []
            print(f"   Courses List: {courses_list}")
        else:
            print(f"❌ No student found with ID: {student_id}")
    
    except sqlite3.Error as e:
        print(f"❌ Error searching for student: {e}")
    finally:
        conn.close()

def show_database_stats():
    """Show database statistics"""
    print("\n📈 DATABASE STATISTICS")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Basic stats
        cursor = conn.execute("SELECT COUNT(*) FROM students;")
        total_students = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT AVG(age) FROM students;")
        avg_age = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT MIN(age), MAX(age) FROM students;")
        age_range = cursor.fetchone()
        
        print(f"👥 Total Students: {total_students}")
        if total_students > 0:
            print(f"📊 Average Age: {avg_age:.1f}" if avg_age else "📊 Average Age: N/A")
            print(f"📊 Age Range: {age_range[0]} - {age_range[1]}" if age_range[0] else "📊 Age Range: N/A")
            
            # Most common courses
            cursor = conn.execute("SELECT courses FROM students;")
            all_courses = cursor.fetchall()
            
            course_count = {}
            for row in all_courses:
                courses = row[0].split(',') if row[0] else []
                for course in courses:
                    course = course.strip()
                    if course:
                        course_count[course] = course_count.get(course, 0) + 1
            
            if course_count:
                print(f"\n📚 Most Popular Courses:")
                sorted_courses = sorted(course_count.items(), key=lambda x: x[1], reverse=True)
                for course, count in sorted_courses[:5]:  # Top 5
                    print(f"   - {course}: {count} students")
    
    except sqlite3.Error as e:
        print(f"❌ Error getting database statistics: {e}")
    finally:
        conn.close()

def main():
    """Main function to run database checks"""
    print("🎓 STUDENT COURSE MANAGEMENT SYSTEM")
    print("📊 Database Inspection Tool")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Database File: {DATABASE}")
    print(f"📍 Database Path: {os.path.abspath(DATABASE)}")
    print()
    
    # Check if database exists
    if not os.path.exists(DATABASE):
        print(f"❌ Database file '{DATABASE}' not found!")
        print("💡 Make sure you're running this script from the correct directory.")
        print("💡 Run the Flask app first to create the database.")
        return
    
    # Run all checks
    check_database_structure()
    check_database_contents()
    show_database_stats()
    search_student_by_id()
    
    print("\n" + "=" * 60)
    print("✅ Database inspection complete!")

if __name__ == "__main__":
    main()