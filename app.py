from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# MySQL 連線設定（用 Render 環境變數）
def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    feedback = request.form.get("feedback")
    if not name or not feedback:
        return jsonify({"status": "error", "message": "缺少欄位"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                feedback TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO feedbacks (name, feedback) VALUES (%s, %s)", (name, feedback))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "感謝你的填寫！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "後端運作正常 / Backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
