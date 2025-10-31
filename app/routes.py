from flask import Blueprint, render_template, redirect, url_for
from .models import Feed, Trash, Walk
from . import db
import datetime

bp = Blueprint("main", __name__)

DOGS = ["ぽんず", "てつ"]
TIMES = ["朝", "昼", "夜"]

@bp.route("/initdb")
def initdb():
    db.create_all()
    return "✅ Tables created"


def clean_old_data():
    """
    📅 今日より前の日付のデータを削除してDBをクリーンに保つ関数
    （テーブル構造や今日のデータは保持）
    """
    today = datetime.date.today().isoformat()
    # 前日以前のレコードを削除
    db.session.query(Feed).filter(Feed.date != today).delete()
    db.session.query(Trash).filter(Trash.date != today).delete()
    db.session.query(Walk).filter(Walk.date != today).delete()
    db.session.commit()


@bp.route("/")
def index():
    # 初回アクセス時にテーブルを作成
    db.create_all()

    today = datetime.date.today().isoformat()

    # ★ 日付が変わっていたら古いデータをクリーンアップ
    clean_old_data()

    # 今日のレコードが無ければ初期化
    for dog in DOGS:
        for t in TIMES:
            if not Feed.query.filter_by(date=today, dog=dog, time=t).first():
                db.session.add(Feed(date=today, dog=dog, time=t, fed=False))

    if not Trash.query.filter_by(date=today).first():
        db.session.add(Trash(date=today, taken=False))

    if not Walk.query.filter_by(date=today).first():
        db.session.add(Walk(date=today, taken=False))
    db.session.commit()

    # 表示データを取得
    feeds = Feed.query.filter_by(date=today).all()
    walk = Walk.query.filter_by(date=today).first()
    trash = Trash.query.filter_by(date=today).first()

    state = {(f.dog, f.time): f.fed for f in feeds}

    return render_template("index.html", today=today, state=state,
                           DOGS=DOGS, TIMES=TIMES,
                           trash=trash.taken, take_walk=walk.taken)


@bp.route("/toggle/<dog>/<time>")
def toggle(dog, time):
    today = datetime.date.today().isoformat()
    feed = Feed.query.filter_by(date=today, dog=dog, time=time).first()
    feed.fed = not feed.fed
    db.session.commit()
    return redirect(url_for("main.index"))


@bp.route("/toggle_take_walk")
def toggle_take_walk():
    today = datetime.date.today().isoformat()
    walk = Walk.query.filter_by(date=today).first()
    walk.taken = not walk.taken
    db.session.commit()
    return redirect(url_for("main.index"))


@bp.route("/toggle_trash")
def toggle_trash():
    today = datetime.date.today().isoformat()
    trash = Trash.query.filter_by(date=today).first()
    trash.taken = not trash.taken
    db.session.commit()
    return redirect(url_for("main.index"))
