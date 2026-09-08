from flask import Blueprint, render_template


page_bp = Blueprint("pages", __name__)


@page_bp.route("/")
def home():
    return render_template("index.html")


@page_bp.route("/games/single-player")
def single_player_page():
    return render_template("games/single_player.html")


@page_bp.route("/games/two-player")
def two_player_page():
    return render_template("games/two_player.html")


@page_bp.route("/games/two-player/choose")
def two_player_choose_page():
    return render_template("games/two_player_choose.html")


@page_bp.route("/games/two-player/computer")
def two_player_computer_page():
    return render_template("games/two_player_computer.html")


@page_bp.route("/games/player-vs-computer")
def player_vs_computer_page():
    return render_template("games/player_vs_computer.html")


@page_bp.route("/statistics")
def statistics_page():
    return render_template("statistics.html")


@page_bp.route("/history")
def history_page():
    return render_template("history.html")