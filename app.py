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
    all_words,
    add_words,
    study_words,
    learned,
    not_verified,
    stats,
    prep_revew,
    reviewed,
    load_word,
    load_models,
)
from models import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/set_lang", methods=["POST"])
def lang_select():
    if request.method == "POST":
        session["active_languages"] = request.json
    return "", 204


@app.route("/")
def index():
    if "all_languages" not in session.keys():
        session["all_languages"] = get_languages()
    return render_template("index.html")


@app.route("/addword", methods=["GET", "POST"])
def add_word():
    if request.method == "POST" and request.form["add_word"] != "":
        for i in range(3):
            print(request.form[f"translation-{i}"] == "")
            if not (
                request.form[f"translation-{i}"] == "" and request.form[f"id-{i}"] == ""
            ):
                add_words(
                    session["lang"],
                    request.form["add_word"],
                    request.form[f"id-{i}"],
                    request.form[f"part-{i}"],
                    request.form[f"translation-{i}"].split("\r\n"),
                )
        return redirect(url_for("index"))
    else:
        words = all_words(session["lang"])
        unverified = not_verified(session["lang"])
        parts = get_parts()
        return render_template(
            "AddWords.html",
            words=words,
            lang=session["lang"],
            unverified=unverified,
            parts=json.dumps(parts),
        )


@app.route("/study", methods=["GET", "POST"])
def learn():
    prep_words = study_words(session["lang"])
    return render_template(
        "study.html", words=json.dumps(prep_words, ensure_ascii=False)
    )


@app.route("/finish", methods=["GET", "POST"])
def finish():
    data = json.loads(request.form.get("data"))
    learned(session["lang"], data)
    return redirect(url_for("index"))


@app.route("/statistics")
def statistics():
    words = stats(session["lang"])
    return render_template("stats.html", all_words=words)


@app.route("/review")
def review():
    if request.method == "POST":
        pass
    else:
        words = prep_revew(session["lang"])
        return render_template(
            "review.html", words=json.dumps(words, ensure_ascii=False)
        )


@app.route("/review_finish", methods=["GET", "POST"])
def review_finish():
    data = json.loads(request.form.get("data"))
    reviewed(session["lang"], data)
    return redirect(url_for("index"))


@app.route("/get_word", methods=["GET", "POST"])
def get_word():
    word = request.json
    return jsonify(load_word(word, session["lang"]))


if __name__ == "__main__":
    app.run(debug=True)
