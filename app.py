from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'abc123'


def get_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    search  = request.args.get('search', '')
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
    
    students = cursor.fetchall()
    conn.close()
    return render_template('home.html', students=students, search=search, total=len(students))

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        
        if not name or not age or not grade:
            error = "All fields are required!"
        elif not age.isdigit():
            error = "Age must be a number"
        else:
            conn = get_connection()
            conn.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, int(age), grade))
            conn.commit()
            conn.close()
            flash("Student added successfully!")
            return redirect(url_for("home"))
    return render_template('add.html', error=error)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted!")
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        cursor.execute("UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?", (name, int(age), grade, id))
        conn.commit()
        conn.close()
        flash("Student updated!")
        return redirect(url_for('home'))
    student = cursor.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('edit.html', student=student)










if __name__=='__main__':
    app.run()
