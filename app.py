from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# MySQL 連線設定
def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),
        port=int(os.environ.get("MYSQL_PORT", 3306))
    )

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # 顯示問卷頁面

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

@app.route("/admin", methods=["GET"])
def view_feedbacks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, feedback, created_at FROM feedbacks ORDER BY created_at DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        html = "<h2>所有填寫紀錄</h2><ul>"
        for row in data:
            html += f"<li><strong>{row[0]}</strong>：{row[1]} <em>({row[2]})</em></li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"❌ 錯誤：{str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
