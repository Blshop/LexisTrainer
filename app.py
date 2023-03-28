from flask import Flask, render_template, request, redirect, url_for, json, jsonify
from func import (
    select_words,
    add_words,
    study_words,
    learned, 
    not_verified,
    stats,
    prep_revew,
    reviewed,
    load_word,
)
from models import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Languages.db"
db.init_app(app)

ACTIVE_LANGUAGE = "russian"


@app.route("/set_lang", methods=["POST"])
def lang_select():
    if request.method == "POST":
        global ACTIVE_LANGUAGE
        ACTIVE_LANGUAGE = request.json
    return "", 204


@app.route("/")
def index():
    return render_template("index.html", lang=json.dumps(ACTIVE_LANGUAGE))


@app.route("/addword", methods=["GET", "POST"])
def add_word():
    if request.method == "POST" and request.form["add_word"] != "":
        for i in range(3):
            print(request.form[f"translation-{i}"] == "")
            if not (
                request.form[f"translation-{i}"] == "" and request.form[f"id-{i}"] == ""
            ):
                add_words(
                    ACTIVE_LANGUAGE,
                    request.form["add_word"],
                    request.form[f"id-{i}"],
                    request.form[f"part-{i}"],
                    request.form[f"translation-{i}"].split("\r\n"),
                )
        return redirect(url_for("index"))
    else:
        words = select_words(ACTIVE_LANGUAGE)
        unverified = not_verified(ACTIVE_LANGUAGE)
        return render_template(
            "AddWords.html",
            words=words,
            lang=ACTIVE_LANGUAGE,
            unverified=unverified,
        )


@app.route("/study", methods=["GET", "POST"])
def learn():
    prep_words = study_words(ACTIVE_LANGUAGE)
    return render_template(
        "study.html", words=json.dumps(prep_words, ensure_ascii=False)
    )


@app.route("/finish", methods=["GET", "POST"])
def finish():
    data = json.loads(request.form.get("data"))
    learned(ACTIVE_LANGUAGE, data)
    return redirect(url_for("index"))


@app.route("/statistics")
def statistics():
    words = stats(ACTIVE_LANGUAGE)
    return render_template("stats.html", all_words=words)


@app.route("/review")
def review():
    if request.method == "POST":
        pass
    else:
        words = prep_revew(ACTIVE_LANGUAGE)
        return render_template(
            "review.html", words=json.dumps(words, ensure_ascii=False)
        )


@app.route("/review_finish", methods=["GET", "POST"])
def review_finish():
    data = json.loads(request.form.get("data"))
    reviewed(ACTIVE_LANGUAGE, data)
    return redirect(url_for("index"))


@app.route("/get_word", methods=["GET", "POST"])
def get_word():
    word = request.json
    return jsonify(load_word(word, ACTIVE_LANGUAGE))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
