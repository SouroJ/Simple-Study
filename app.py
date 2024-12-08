import sqlite3
from flask import Flask, request, redirect, url_for, render_template, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "diana_and_janelle_yay"

# Database setup
DATABASE = 'users.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                time_added TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                time_added TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")

        conn.commit()

# Initialize database
init_db()

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("login"))

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists. Try logging in."
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))
        return "Invalid credentials. Try again."
    return render_template("login.html")

# Welcome when user is in
@app.route("/welcome")
def welcome():
    if "user" in session:
        return f"Welcome {session['user']}! <a href='/logout'>Logout</a>"
    return redirect(url_for("login"))

# Log out
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        tasks = cursor.fetchall()
    return render_template("dashboard.html", tasks=tasks)

# Add a task
@app.route("/add", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    task = request.form.get("task")

    # Formats the date as a string
    time_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, user_id, time_added) VALUES (?, ?, ?)", (task, user_id, time_added))
        conn.commit()
    return redirect(url_for("dashboard"))

# Delete task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Retrieves information first, just in case it gets deleted
        cursor.execute("SELECT task, time_added FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        task = cursor.fetchone()
        if task:
            # If task found then delete it from tasks table
            cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            
            # Insert the deleted task into the history table
            cursor.execute("INSERT INTO history (task, user_id, time_added) VALUES (?, ?, ?)", (task[0], user_id, task[1]))
            conn.commit()

    return redirect(url_for("dashboard"))

# Edit task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        # Get the updated task text from the form
        updated_task = request.form["task"]

        # Update the task in the database
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET task = ? WHERE id = ? AND user_id = ?",(updated_task, task_id, user_id),)
            conn.commit()
        return redirect(url_for("dashboard"))

    # Get task to edit
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task FROM tasks WHERE id = ? AND user_id = ?",(task_id, user_id),)
        task = cursor.fetchone()

    if not task:
        return "Task not found"
    return render_template("edit_task.html", task_id=task_id, task_text=task[0])

# Allows user to see history of their tasks
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Retrieves task and time it was added to list
        cursor.execute("SELECT task, time_added FROM history WHERE user_id = ?", (session["user_id"],))
        time_tasks = cursor.fetchall()
    
    # It will display in history.html for the user
    return render_template("history.html", time_tasks=time_tasks)

@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("quiz.html")

if __name__ == "__main__":
    app.run(debug=True)