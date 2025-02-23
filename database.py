from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ❌ Hardcoded database credentials
DB_NAME = "test_db"
DB_USER = "admin"
DB_PASS = "password123"  # Security risk!

# ❌ Inefficient database connection (Opens a new connection for each request)
def get_db_connection():
    return sqlite3.connect("database.db")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    # ❌ No input validation (Accepts any data)
    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ❌ SQL Injection vulnerability (User input directly in query)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    
    # ❌ No input validation
    username = data["username"]
    password = data["password"]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ❌ SQL Injection vulnerability
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User added"}), 201

@app.route("/slow-endpoint", methods=["GET"])
def slow_endpoint():
    import time
    time.sleep(5)  # ❌ Blocking operation (Causes performance issues)
    return jsonify({"message": "This endpoint is slow!"})

if __name__ == "__main__":
    app.run(debug=True)  # ❌ Debug mode enabled in production (Security risk)
