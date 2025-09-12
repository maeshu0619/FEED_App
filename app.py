from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "犬ごはんチェックアプリにようこそ！"

if __name__ == "__main__":
    app.run()
