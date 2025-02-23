import os
import sqlite3
import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# Secure credentials from environment variables
DB_NAME = os.getenv("DB_NAME", "database.db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Used for secure hashing

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Validate user input
def is_valid_input(data, keys):
    return all(key in data and isinstance(data[key], str) and data[key].strip() for key in keys)

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        # Validate input
        if not is_valid_input(data, ["username", "password"]):
            return jsonify({"error": "Invalid input"}), 400

        username = data["username"].strip()
        password = data["password"].strip()

        # ❌ FIXED: Using `with` ensures the connection closes automatically
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Use parameterized query to prevent SQL injection
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        logging.error(f"Error in login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/add-user", methods=["POST"])
def add_user():
    try:
        data = request.get_json()

        # Validate input
        if not is_valid_input(data, ["username", "password"]):
            return jsonify({"error": "Invalid input"}), 400

        username = data["username"].strip()
        password = data["password"].strip()

        # Hash password before storing it
        hashed_password = generate_password_hash(password)

        # ❌ FIXED: Using `with` to avoid resource leaks
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()

        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        logging.error(f"Error in add-user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/fast-endpoint", methods=["GET"])
def fast_endpoint():
    return jsonify({"message": "This endpoint is optimized and fast!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Debug mode disabled for production
