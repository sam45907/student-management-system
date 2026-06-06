from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Login Page
@app.route('/login')
def login():
    return render_template('login.html')

# Add Student Page
@app.route('/add')
def add_student():
    return render_template('add_student.html')

# Save Student
@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']
    email = request.form['email']

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
        (name, age, course, email)
    )

    conn.commit()
    conn.close()

    return redirect('/view')

# View Students
@app.route('/view')
def view():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template('view_students.html', students=students)

# Delete Student
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view')

# Update Page
@app.route('/update/<int:id>')
def update_page(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cur.fetchone()

    conn.close()

    return render_template('update_student.html', student=student)

# Update Student
@app.route('/update_student', methods=['POST'])
def update_student():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']
    email = request.form['email']

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?, email = ?
        WHERE id = ?
    """, (name, age, course, email, id))

    conn.commit()
    conn.close()

    return redirect('/view')

# Search Student
@app.route('/search', methods=['GET', 'POST'])
def search():
    students = []

    if request.method == 'POST':
        keyword = request.form['keyword']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + keyword + '%',)
        )

        students = cur.fetchall()

        conn.close()

    return render_template('search_student.html', students=students)

if __name__ == '__main__':
    app.run(debug=True, port=8070)