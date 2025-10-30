from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Database configuration
DATABASE = 'students.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            courses TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def process_student_data(students_raw):
    """
    Process raw database data using dictionaries and lists
    as required by the assignment
    """
    students_list = []
    for student in students_raw:
        student_dict = {
            'student_id': student['student_id'],
            'name': student['name'],
            'age': student['age'],
            'courses': student['courses'].split(',') if student['courses'] else []
        }
        students_list.append(student_dict)
    return students_list

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        student_id = request.form['student_id'].strip()
        name = request.form['name'].strip()
        age = request.form['age']
        courses = request.form['courses'].strip()
        
        # Validation
        if not student_id or not name or not age or not courses:
            flash('All fields are required!', 'error')
            return render_template('add_student.html')
        
        try:
            age = int(age)
            if age <= 0:
                flash('Age must be a positive number!', 'error')
                return render_template('add_student.html')
        except ValueError:
            flash('Age must be a valid number!', 'error')
            return render_template('add_student.html')
        
        conn = get_db_connection()
        try:
            # Check if student ID already exists
            existing = conn.execute('SELECT student_id FROM students WHERE student_id = ?', (student_id,)).fetchone()
            if existing:
                flash('Student ID already exists! Please use a different ID.', 'error')
                return render_template('add_student.html')
            
            # Insert new student
            conn.execute(
                'INSERT INTO students (student_id, name, age, courses) VALUES (?, ?, ?, ?)',
                (student_id, name, age, courses)
            )
            conn.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('view_students'))
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('add_student.html')

@app.route('/view_students')
def view_students():
    """View all students"""
    conn = get_db_connection()
    students_raw = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    conn.close()
    
    # Process data using dictionaries and lists as required
    students = process_student_data(students_raw)
    
    return render_template('view_students.html', students=students)

@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    """Search for a student by ID"""
    student = None
    if request.method == 'POST':
        student_id = request.form['student_id'].strip()
        
        if not student_id:
            flash('Please enter a Student ID!', 'error')
            return render_template('search_student.html')
        
        conn = get_db_connection()
        student_raw = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
        conn.close()
        
        if student_raw:
            # Process data using dictionary as required
            student = {
                'student_id': student_raw['student_id'],
                'name': student_raw['name'],
                'age': student_raw['age'],
                'courses': student_raw['courses'].split(',') if student_raw['courses'] else []
            }
        else:
            flash('Student not found!', 'error')
    
    return render_template('search_student.html', student=student)

@app.route('/update_courses/<student_id>', methods=['GET', 'POST'])
def update_courses(student_id):
    """Update courses for a student"""
    conn = get_db_connection()
    student_raw = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    if not student_raw:
        flash('Student not found!', 'error')
        return redirect(url_for('view_students'))
    
    # Process data using dictionary as required
    student = {
        'student_id': student_raw['student_id'],
        'name': student_raw['name'],
        'age': student_raw['age'],
        'courses': student_raw['courses']
    }
    
    if request.method == 'POST':
        new_courses = request.form['courses'].strip()
        
        if not new_courses:
            flash('Courses field cannot be empty!', 'error')
            return render_template('update_courses.html', student=student)
        
        try:
            conn.execute(
                'UPDATE students SET courses = ? WHERE student_id = ?',
                (new_courses, student_id)
            )
            conn.commit()
            flash('Courses updated successfully!', 'success')
            return redirect(url_for('view_students'))
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            conn.close()
    else:
        conn.close()
    
    return render_template('update_courses.html', student=student)

@app.route('/delete_student/<student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete a student"""
    conn = get_db_connection()
    try:
        # Check if student exists
        student = conn.execute('SELECT student_id FROM students WHERE student_id = ?', (student_id,)).fetchone()
        if not student:
            flash('Student not found!', 'error')
        else:
            conn.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            conn.commit()
            flash('Student deleted successfully!', 'success')
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Get port from environment variable (for Render deployment) or default to 5000
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)