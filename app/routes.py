from flask import Blueprint, render_template, redirect, url_for
from .db import init_db_for_today, get_state_for_today, toggle_feed_today, \
                DOGS, TIMES, init_trash_for_today, get_trash_for_today, toggle_trash_today


bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    init_db_for_today()
    init_trash_for_today()
    state, today = get_state_for_today()
    trash = get_trash_for_today()
    return render_template("index.html", today=today, state=state,
                           DOGS=DOGS, TIMES=TIMES, trash=trash)

@bp.route("/toggle/<dog>/<time>")
def toggle(dog, time):
    toggle_feed_today(dog, time)
    return redirect(url_for("main.index"))

@bp.route("/toggle_trash")
def toggle_trash():
    toggle_trash_today()
    return redirect(url_for("main.index"))