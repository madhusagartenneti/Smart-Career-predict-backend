from flask import Blueprint, request, jsonify, current_app
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime

auth_bp = Blueprint("auth", __name__)

# ---------- DB INIT ----------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            number TEXT NOT NULL,
            profile TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- REGISTER ----------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    email = data.get("email")
    number = data.get("number")

    if not all([username, password, confirm_password, email, number]):
        return jsonify({"message": "All fields required"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    password_hash = generate_password_hash(password)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return jsonify({"message": "User already exists"}), 400

    c.execute(
        "INSERT INTO users (username, password, email, number) VALUES (?, ?, ?, ?)",
        (username, password_hash, email, number)
    )
    conn.commit()
    conn.close()

    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"message": "Registered successfully", "token": token}), 201


# ---------- LOGIN ----------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    if not row or not check_password_hash(row[0], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token})
