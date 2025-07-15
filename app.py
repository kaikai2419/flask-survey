from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# 資料庫連線設定（使用 Render 的環境變數）
def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),
        port=int(os.environ.get("MYSQL_PORT", 3306))
    )

# 問卷送出 API
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

# 問卷主頁
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

