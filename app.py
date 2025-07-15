from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="centerbeam.proxy.rlwy.net",
        user="root",
        password="HlqQFyubVDkDbnZBhqxjiqPtkGQiRVLJ",
        database="railway",
        port=15852
    )

@app.route("/")
def home():
    return render_template("index.html")

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
        return jsonify({"status": "success", "message": "留言成功！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin")
def admin():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedbacks ORDER BY created_at DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin.html", feedbacks=data)
    except Exception as e:
        return f"資料讀取失敗：{e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
