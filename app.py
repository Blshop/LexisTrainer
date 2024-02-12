from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    json,
    jsonify,
    session,
)
from config import Config
from func import (
    get_languages,
    get_parts,
    get_all_words,
    add_word,
    study_words,
    learned,
    not_verified,
    stats,
    prep_revew,
    reviewed,
    load_word,
)
from models import db
import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# home page of an application
@app.route("/")
def index():
    #  TODO: find a better way to initialize session
    if "all_languages" not in session.keys():
        session["all_languages"] = get_languages()
    return render_template(
        "index.html", active_languages=json.dumps(session.get("active_languages", ""))
    )


# route used to set active languages on home page
@app.route("/set_lang", methods=["POST"])
def set_lang():
    if request.method == "POST":
        session["active_languages"] = request.json
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/add_words", methods=["GET", "POST"])
def add_words():
    if request.method == "POST":
        add_word(request.json, session["active_languages"])
        return "", 200
    else:
        words = get_all_words(session["active_languages"])
        unverified = not_verified(session["active_languages"])
        parts = get_parts()
        return render_template(
            "AddWords.html",
            words=words,
            lang=session["active_languages"],
            unverified=unverified,
            parts=json.dumps(parts),
        )


@app.route("/study", methods=["GET", "POST"])
def learn():
    prep_words = study_words(session["active_languages"])
    parts = get_parts()
    return render_template(
        "study.html",
        words=json.dumps(prep_words, ensure_ascii=False),
        parts=json.dumps(parts),
    )


@app.route("/finish", methods=["GET", "POST"])
def finish():
    data = json.loads(request.form.get("data"))
    learned(session["active_languages"], data)
    return redirect(url_for("index"))


@app.route("/statistics")
def statistics():
    words = stats(session["active_languages"])
    return render_template("stats.html", all_words=words)


@app.route("/review")
def review():
    if request.method == "POST":
        pass
    else:
        words = prep_revew(session["active_languages"])
        parts = get_parts()
        return render_template(
            "review.html",
            words=json.dumps(words, ensure_ascii=False),
            parts=json.dumps(parts),
        )


@app.route("/review_finish", methods=["GET", "POST"])
def review_finish():
    data = json.loads(request.form.get("data"))
    reviewed(session["active_languages"], data)
    return redirect(url_for("index"))


@app.route("/get_word", methods=["GET", "POST"])
def get_word():
    word = request.json
    return jsonify(load_word(word, session["active_languages"]))


if __name__ == "__main__":
    app.run(debug=True)
