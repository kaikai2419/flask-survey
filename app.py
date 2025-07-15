from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# 建立 MySQL 資料庫連線
def get_connection():
    return mysql.connector.connect(
        host="centerbeam.proxy.rlwy.net",
        user="root",
        password="HlqQFyubVDkDbnZBhqxjiqPtkGQiRVLJ",
        database="railway",
        port=15852
    )

# 使用者表單頁
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# 接收表單資料 API
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    feedback = request.form.get("feedback")

    if not name or not feedback:
        return jsonify({"status": "error", "message": "請填寫所有欄位"}), 400

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
        return jsonify({"status": "success", "message": "已成功送出回饋！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 管理者後台（查看留言）
@app.route("/admin", methods=["GET"])
def admin():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedbacks ORDER BY created_at DESC")
        feedbacks = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin.html", feedbacks=feedbacks)
    except Exception as e:
        return f"讀取資料失敗：{e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
