from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "犬ごはんチェックアプリにようこそ！"

if __name__ == "__main__":
    app.run()
from flask import Flask, render_template_string, redirect, url_for
import sqlite3, datetime

app = Flask(__name__)
DB = "dogfeed.db"

# 初期化：1日ごとにリセットする仕組み
def init_db():
    today = datetime.date.today().isoformat()
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feeds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                dog TEXT,
                time TEXT,
                fed INTEGER
            )
        """)
        # てつ & ぽんず x 朝昼夜 = 6件
        for dog in ["てつ", "ぽんず"]:
            for time in ["朝", "昼", "夜"]:
                cur.execute("SELECT * FROM feeds WHERE date=? AND dog=? AND time=?", (today, dog, time))
                if cur.fetchone() is None:
                    cur.execute("INSERT INTO feeds(date, dog, time, fed) VALUES (?,?,?,0)", (today, dog, time))
        con.commit()

@app.route("/")
def index():
    init_db()
    today = datetime.date.today().isoformat()
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT dog, time, fed FROM feeds WHERE date=? ORDER BY dog, time", (today,))
        rows = cur.fetchall()
    # 表示用に辞書化
    state = { (dog, time): fed for dog, time, fed in rows }
    return render_template_string(TEMPLATE, today=today, state=state)

@app.route("/toggle/<dog>/<time>")
def toggle(dog, time):
    today = datetime.date.today().isoformat()
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT fed FROM feeds WHERE date=? AND dog=? AND time=?", (today, dog, time))
        fed = cur.fetchone()[0]
        newval = 0 if fed else 1
        cur.execute("UPDATE feeds SET fed=? WHERE date=? AND dog=? AND time=?", (newval, today, dog, time))
        con.commit()
    return redirect(url_for("index"))

# HTML テンプレート（Bootstrap で2x3ボタン配置）
TEMPLATE = """
<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>犬ごはんチェック</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
  body { padding:20px; }
  .dog-label { width:60px; font-weight:bold; }
  .btn-fed { background-color: lightgreen !important; }
</style>
</head>
<body>
  <div class="d-flex justify-content-end">
    <h5>{{ today }}</h5>
  </div>
  <div class="container mt-4">
    <table class="table table-borderless text-center">
      <thead>
        <tr>
          <th></th>
          <th>朝</th>
          <th>昼</th>
          <th>夜</th>
        </tr>
      </thead>
      <tbody>
        {% for dog in ["てつ", "ぽんず"] %}
        <tr>
          <td class="dog-label">{{ dog }}</td>
          {% for time in ["朝","昼","夜"] %}
            {% set fed = state[(dog, time)] %}
            <td>
              <a href="{{ url_for('toggle', dog=dog, time=time) }}"
                 class="btn btn-lg w-100 {% if fed %}btn-fed{% else %}btn-outline-secondary{% endif %}">
                 {{ time }}
              </a>
            </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
