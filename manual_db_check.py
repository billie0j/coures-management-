#!/usr/bin/env python3
"""
Manual Database Check Examples
This file shows you how to manually check the database using Python code.
"""

import sqlite3

# Example 1: Basic database connection and query
def basic_check():
    """Basic way to check database"""
    print("=== BASIC DATABASE CHECK ===")
    
    # Connect to database
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    
    # Execute a simple query
    cursor = conn.execute('SELECT * FROM students')
    students = cursor.fetchall()
    
    print(f"Total students: {len(students)}")
    for student in students:
        print(f"ID: {student['student_id']}, Name: {student['name']}, Age: {student['age']}")
    
    conn.close()

# Example 2: Using the same connection function as the app
def app_style_check():
    """Check database using the same method as the Flask app"""
    print("\n=== APP-STYLE DATABASE CHECK ===")
    
    def get_db_connection():
        """Same function as in app.py"""
        conn = sqlite3.connect('students.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    # Get all students (same as view_students route)
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    conn.close()
    
    print(f"Students (ordered by name): {len(students)}")
    for student in students:
        courses_list = student['courses'].split(',') if student['courses'] else []
        print(f"- {student['name']} (ID: {student['student_id']}) - Courses: {courses_list}")

# Example 3: Search for specific student
def search_example():
    """Example of searching for a specific student"""
    print("\n=== SEARCH EXAMPLE ===")
    
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    
    # Search for student with specific ID
    student_id = "24312103555"  # Replace with actual ID
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    if student:
        print(f"Found student: {student['name']}")
        print(f"Age: {student['age']}")
        print(f"Courses: {student['courses']}")
    else:
        print(f"No student found with ID: {student_id}")
    
    conn.close()

# Example 4: Count and statistics
def statistics_example():
    """Example of getting database statistics"""
    print("\n=== STATISTICS EXAMPLE ===")
    
    conn = sqlite3.connect('students.db')
    
    # Count total students
    count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    print(f"Total students: {count}")
    
    # Get average age
    avg_age = conn.execute('SELECT AVG(age) FROM students').fetchone()[0]
    print(f"Average age: {avg_age:.1f}" if avg_age else "Average age: N/A")
    
    # Get all unique courses
    all_courses = conn.execute('SELECT courses FROM students').fetchall()
    unique_courses = set()
    for row in all_courses:
        if row[0]:  # If courses is not empty
            courses = row[0].split(',')
            for course in courses:
                unique_courses.add(course.strip())
    
    print(f"Unique courses: {sorted(unique_courses)}")
    
    conn.close()

# Example 5: Raw SQL queries
def raw_sql_examples():
    """Examples of raw SQL queries you can run"""
    print("\n=== RAW SQL EXAMPLES ===")
    
    conn = sqlite3.connect('students.db')
    
    # Show table structure
    print("Table structure:")
    schema = conn.execute("PRAGMA table_info(students)").fetchall()
    for col in schema:
        print(f"  {col[1]} ({col[2]})")
    
    # Show all data
    print("\nAll data:")
    cursor = conn.execute("SELECT * FROM students")
    for row in cursor:
        print(f"  {row}")
    
    conn.close()

if __name__ == "__main__":
    print("🔍 MANUAL DATABASE CHECK EXAMPLES")
    print("=" * 50)
    
    try:
        basic_check()
        app_style_check()
        search_example()
        statistics_example()
        raw_sql_examples()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Database file 'students.db' not found!")
        print("💡 Make sure you're in the correct directory and the Flask app has been run at least once.")