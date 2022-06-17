import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bcrypt = Bcrypt(app)

def connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def check_auth():
    if "user" not in session.keys():
        return False
    return True


@app.route('/')
def index():
    if check_auth():
        return render_template('home.html')
    return redirect(url_for("login"))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if check_auth():
        return redirect(url_for('index'))
    if request.method == 'POST':
        password = request.form['password']
        conn = connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                            (request.form['username'],)).fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = user["username"]
            return redirect(url_for('index'))
        else:
            flash("Incorrect username or password!")
    return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if check_auth():
        return redirect(url_for('index'))
    if request.method == 'POST':
        errors = []
        username = request.form['username']
        password = request.form['password']

        conn = connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                            (username,)).fetchone()
        conn.close()

        if user:
            errors.append("Username {} already exists!".format(username))

        if len(username) < 3 or len(username) > 20:
            errors.append("Username should be 3-20 characters long!")
        if len(password) < 5 or len(password) > 20:
            errors.append("Password should be 5-20 characters long!")
        if request.form["g-recaptcha-response"] == "":
            errors.append("Prove you are not a robot!")

        if len(errors) > 0:
            for error in errors:
                flash(error)

        if len(errors) < 1:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            conn = connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, password))
            conn.commit()
            conn.close()
            session["user"] = username
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/logout")
def logout():
    if check_auth():
        session.pop("user")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
