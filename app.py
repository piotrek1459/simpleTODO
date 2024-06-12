from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import sqlite3


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    user_id = session["user_id"][0]

    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM users WHERE id = (?)", (user_id,))
    name = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM tasks WHERE user_id = (?)", (user_id,))
    tasks = cursor.fetchall()

    connection.close()

    return render_template("index.html", name=name, tasks=tasks)


@app.route("/task-create", methods=["POST", "GET"])
@login_required
def add_task():

    user_id = session["user_id"][0]

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        if not title:
            flash("You need to provide title for the task", "error")
            return render_template("add_task.html")

        isComplete = request.form.get("isComplete")

        if not isComplete:
            isComplete = 0
        else:
            isComplete = 1

        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (user_id, title, description, is_complete) VALUES (?, ?, ?, ?)", (user_id, title, description, isComplete))
        connection.commit()
        connection.close()
        flash("Task has been succesfully added", "success")
        return redirect("/")
    else:
        return render_template("add_task.html")


@app.route("/task-update/<todo_id>", methods=["GET", "POST"])
@login_required
def task_update(todo_id):

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        if not title:
            flash("You need to provide title for the task", "error")
            return render_template("add_task.html")

        isComplete = request.form.get("isComplete")
        if not isComplete:
            isComplete = 0
        else:
            isComplete = 1

        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET title=(?), description=(?), is_complete=(?) WHERE id=(?)", (title, description, isComplete, todo_id))
        connection.commit()
        connection.close()
        return redirect("/")

    else:
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = (?)", (todo_id,))
        task = cursor.fetchall()
        connection.close()
        return render_template("task_update.html", task=task[0], todo_id=todo_id)


@app.route("/task-delete/<todo_id>")
@login_required
def task_delete(todo_id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = (?)", (todo_id,))
    flash("Task has been successfully deleted", "success")
    connection.commit()
    connection.close()
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("You need to provide username", "error")
            return render_template("login.html")

        if not password:
            flash("You need to provide password", "error")
            return render_template("login.html")

        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = (?)", (username,))
        row = cursor.fetchall()

        if len(row) != 1 or not check_password_hash(row[0][3], password):
            flash("Invalid username and/or password", "error")
            connection.close()
            return render_template("login.html")

        session["user_id"] = row[0]
        connection.close()
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not name:
            flash("You need to provide name", "error")
            return render_template("register.html")

        if not username:
            flash("You need to provide username", "error")
            return render_template("register.html")

        if not password:
            flash("You need to provide password", "error")
            return render_template("register.html")

        if not confirmation:
            flash("You need to provide confirmation", "error")
            return render_template("register.html")

        if password != confirmation:
            flash("Password and confirmation don't match", "error")
            return render_template("register.html")

        hash = generate_password_hash(password)

        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = (?)", (username,))
        row = cursor.fetchall()

        if not row:

            cursor.execute("INSERT INTO users (name, username, hash) VALUES (?, ?, ?)", (name, username, hash))
            connection.commit()
            flash("Your account has been created", "success")

            cursor.execute("SELECT * FROM users WHERE username = (?)", (username,))
            row = cursor.fetchall()
            session["user_id"] = row[0]

            connection.close()
            return redirect("/")

        else:
            flash("This username already exists", "error")
            return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run()
