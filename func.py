from models import db, Russian, English
from flask import json


def edit_prep(words):
    prep_words = {}
    for rus, eng in words:
        if rus not in prep_words.keys():
            prep_words[rus] = [
                eng,
            ]

        else:
            prep_words[rus].append(eng)
    return prep_words


def select_words(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    words = db.session.query(model.word).all()
    word_list = [word.word for word in words]
    return json.dumps(word_list, ensure_ascii=False)


def add_words(lang, params):
    if lang == "russian":
        add_model = Russian
        trans_model = English
    elif lang == "english":
        add_model = English
        trans_model = Russian
    if (
        add_model.query.filter_by(word=params["add_word"], part=params["part"]).first()
        is None
    ):
        add_word = add_model(
            word=params["add_word"], part=params["part"], verified=True
        )
        db.session.add(add_word)
        for item in params["translations"]:
            if (
                trans_model.query.filter_by(word=item, part=params["part"]).first()
                is None
            ):
                trans_word = trans_model(word=item, part=params["part"])
                db.session.add(trans_word)
                add_word.translation.append(trans_word)
            else:
                trans_word = trans_model.query.filter_by(
                    word=item, part=params["part"]
                ).first()
                add_word.translation.append(trans_word)
        db.session.commit()
