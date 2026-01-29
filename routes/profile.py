from flask import Blueprint, request, jsonify
import sqlite3
import json
from utils import token_required

profile_bp = Blueprint("profile", __name__)

# ---------- UPDATE PROFILE ----------
@profile_bp.route("/update", methods=["POST"])
@token_required
def update_profile(current_user):
    data = request.json
    profile_data = json.dumps(data.get("profile", {}))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (current_user,))
    if not c.fetchone():
        conn.close()
        return jsonify({"message": "User not found"}), 404

    c.execute("UPDATE users SET profile=? WHERE username=?", (profile_data, current_user))
    conn.commit()
    conn.close()
    return jsonify({"message": "Profile updated successfully"})


# ---------- GET PROFILE WITH USER DATA ----------
@profile_bp.route("/", methods=["GET"])
@token_required
def get_profile(current_user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT username, email, number, profile FROM users WHERE username=?", (current_user,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "User not found"}), 404

    username, email, number, profile_json = row
    profile_data = json.loads(profile_json) if profile_json else {}

    return jsonify({
        "username": username,
        "email": email,
        "number": number,
        "profile": profile_data
    })
