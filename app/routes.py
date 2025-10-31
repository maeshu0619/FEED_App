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

def reset_for_today():
    """DBの全データを削除し、当日分の初期レコードを作成する"""
    # 全削除（テーブル構造は残す）
    db.session.query(Feed).delete()
    db.session.query(Trash).delete()
    db.session.query(Walk).delete()
    db.session.commit()

    # 当日分を初期化
    today = datetime.date.today().isoformat()
    for dog in DOGS:
        for t in TIMES:
            db.session.add(Feed(date=today, dog=dog, time=t, fed=False))
    db.session.add(Trash(date=today, taken=False))
    db.session.add(Walk(date=today, taken=False))
    db.session.commit()

def ensure_today_exists():
    """（保守用）当日分の行が欠けていれば補完する"""
    today = datetime.date.today().isoformat()
    for dog in DOGS:
        for t in TIMES:
            if not Feed.query.filter_by(date=today, dog=dog, time=t).first():
                db.session.add(Feed(date=today, dog=dog, time=t, fed=False))
    if not Trash.query.filter_by(date=today).first():
        db.session.add(Trash(date=today, taken=False))
    if not Walk.query.filter_by(date=today).first():
        db.session.add(Walk(date=today, taken=False))
    db.session.commit()

@bp.route("/")
def index():
    # 初回アクセスでテーブル作成
    db.create_all()

    today = datetime.date.today().isoformat()

    # 「今日のFeedが1件も無い」＝新しい日とみなす
    is_new_day = not Feed.query.filter_by(date=today).first()

    if is_new_day:
        # 日付が変わった瞬間の最初のアクセス時にフルリセット＋初期化
        reset_for_today()
    else:
        # 念のため欠けている行を補完
        ensure_today_exists()

    # 表示用データ取得
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

@bp.route("/daily_reset")
def daily_reset():
    """手動・外部からも同じ挙動で初期化できるようにしておく"""
    reset_for_today()
    return "✅ Daily reset completed"
