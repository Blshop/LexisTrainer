from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    json,
)
import random
from func import edit_prep, select_words, add_words, study_words
from models import db, Russian, English


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Languages.db"
db.init_app(app)

ACTIVE_LANGUAGE = "russian"


@app.route("/get_lang", methods=["POST"])
def lang_select():
    if request.method == "POST":
        global ACTIVE_LANGUAGE
        ACTIVE_LANGUAGE = request.json
    return "", 204


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword", methods=["GET", "POST"])
def add_word():
    if request.method == "POST" and request.form["add_word"] != "":
        for i in range(1, 4):
            if request.form[f"translation-{i}"] != "":
                add_words(
                    ACTIVE_LANGUAGE,
                    request.form["add_word"],
                    request.form[f"part-{i}"],
                    request.form[f"translation-{i}"].split("\r\n"),
                )
        return redirect(url_for("index"))
    else:
        words = select_words(ACTIVE_LANGUAGE)
        return render_template("AddWords.html", words=words, lang=ACTIVE_LANGUAGE)


@app.route("/view")
def view():
    return render_template("viewWords.html")


@app.route("/learn", methods=["GET", "POST"])
def learn():
    prep_words = study_words(ACTIVE_LANGUAGE)
    print(prep_words)
    return render_template(
        "learn.html", words=json.dumps(prep_words, ensure_ascii=False)
    )


@app.route("/finish", methods=["GET", "POST"])
def finish():
    data = json.loads(request.form.get("data"))
    for key, value in data.items():
        Russian.query.filter(Russian.word == key).update(dict(answer=value[0]))
    db.session.commit()
    return jsonify("everything is good")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST" and request.form["word"] != "":
        new_translation = request.form["translation"].split("\r\n")
        old_word = Russian.query.filter_by(word=request.form["word"]).first()
        new_word = LearningRus.query.filter_by(rus_id=old_word.id).first()
        new_word.answer = 0
        old_translation = (
            db.session.query(
                Translation.russian_id, Translation.english_id, English.word
            )
            .join(Translation)
            .filter(Translation.russian_id == old_word.id)
            .all()
        )
        for word in old_translation:
            if word[2] not in new_translation:
                Translation.query.filter_by(
                    english_id=word[1], russian_id=word[0]
                ).delete()
            else:
                new_translation.remove(word[2])
        db.session.commit()
        for word in new_translation:
            if English.query.filter_by(word=word).first() is None:
                new_word = English(word=word, part=request.form["part"])
                db.session.add(new_word)
                db.session.flush()
                translation = Translation(new_word.id, old_word.id)
                db.session.add(translation)
                db.session.commit()
            else:
                new_word = English.query.filter_by(word=word).first()
                translation = Translation(new_word.id, old_word.id)
                db.session.add(translation)
                db.session.commit()
        return redirect(url_for("index"))
    else:
        all_words = (
            db.session.query(Russian.word, English.word)
            .join(Translation, Translation.russian_id == Russian.id)
            .join(English)
            .all()
        )
        all_words = edit_prep(all_words)
        return render_template("edit.html", words=json.dumps(all_words))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
