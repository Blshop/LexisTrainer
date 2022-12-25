from models import db, Russian, English
from flask import json
from datetime import date, timedelta
from sqlalchemy import func


def single_model(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    return model


def double_model(lang):
    if lang == "russian":
        add_model = Russian
        trans_model = English
    elif lang == "english":
        add_model = English
        trans_model = Russian
    return (add_model, trans_model)


def select_words(lang):
    model = single_model(lang)
    words = db.session.query(model.word).distinct().all()
    word_list = [word.word for word in words]
    return json.dumps(word_list, ensure_ascii=False)


def add_translation(model, word, part):
    trans = model.query.filter(model.word == word).all()
    tran = model.query.filter(model.word == word, model.part == part).first()
    if tran is None:
        tran = model(word=word, part=part)
        db.session.add(tran)
    for tran in trans:
        tran.answer = 0
    return tran


def add_words(lang, add_word, id, part, translations):
    print(lang, add_word, id, part, translations)
    add_model, trans_model = double_model(lang)
    if id == "":
        add_word = add_model(word=add_word, part=part, verified=True)
        db.session.add(add_word)
        for translation in translations:
            add_word.translation.append(
                add_translation(trans_model, translation, part))
    elif translations == [""]:
        print("here")
        add_word = add_model.query.filter_by(id=id).first()
        add_word.translation = []
        add_model.query.filter_by(id=id).delete()
    else:
        add_word = add_model.query.filter(add_model.id == id).first()
        add_word.part = part
        add_word.answer = 0
        add_word.verified = True
        old_trans = add_word.translation
        for old in old_trans:
            if old.word not in translations:
                old_trans.remove(old)
            else:
                translations.remove(old.word)
        for translation in translations:
            add_word.translation.append(
                add_translation(trans_model, translation, part))
    db.session.commit()


def study_words(lang):
    model = single_model(lang)
    words = model.query.filter(
        model.answer < 100, model.verified == True).all()
    prep_words = {}
    for word in words:
        if word.word in prep_words.keys():
            prep_words[word.word][word.part] = {
                "answer": word.answer,
                "translation": [trans.word for trans in word.translation],
            }
        else:
            prep_words[word.word] = {
                word.part: {
                    "answer": word.answer,
                    "translation": [trans.word for trans in word.translation],
                }
            }
    print(prep_words)
    return prep_words


def learned(lang, words):
    model = single_model(lang)
    for word, parts in words.items():
        for part, data in parts.items():
            if data["answer"] == 100:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(
                        answer=data["answer"], learned_date=date.today(), repeat_delay=5
                    )
                )
            else:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(answer=data["answer"])
                )
    db.session.commit()


def not_verified(lang):
    model = single_model(lang)
    words = model.query.filter(model.verified == False).all()
    prep_words = {}
    for word in words:
        if word.word in prep_words.keys():
            prep_words[word.word][word.part] = [
                word.answer,
                [trans.word for trans in word.translation],
            ]
        else:
            prep_words[word.word] = {
                word.part: [word.answer, [
                    trans.word for trans in word.translation]]
            }
    return prep_words


def stats(lang):
    model = single_model(lang)
    all_words = len(model.query.group_by(model.word).all())
    learned = len(
        model.query.filter(model.answer == 100, model.verified == True)
        .group_by(model.word)
        .all()
    )
    sq = (
        db.session.query(model.word, model.answer)
        .filter(model.answer < 100, model.verified == True)
        .group_by(model.word)
        .subquery()
    )
    to_learn = (
        db.session.query(sq.c.answer, db.func.count(sq.c.answer))
        .group_by(sq.c.answer)
        .all()
    )
    count = db.session.query(sq.c.answer).count()

    to_review = len(
        model.query.filter(model.answer == 100, model.verified == True)
        .filter(model.learned_date < date.today())
        .group_by(model.word)
        .all()
    )
    return {
        "all_words": all_words,
        "learned": learned,
        "count": to_learn,
        "to_learn": count,
        "to_review": to_review,
    }


def prep_revew(lang):
    model = single_model(lang)
    words = (
        model.query.filter(model.answer == 100, model.verified == True)
        .filter(model.learned_date < date.today())
        .all()
    )
    prep_words = {}
    for word in words:
        if word.word in prep_words.keys():
            prep_words[word.word][word.part] = [
                word.answer,
                word.repeat_delay,
                [trans.word for trans in word.translation],
            ]
        else:
            prep_words[word.word] = {
                word.part: [
                    word.answer,
                    word.repeat_delay,
                    [trans.word for trans in word.translation],
                ]
            }
    return prep_words


def reviewed(lang, words):
    model = single_model(lang)
    for word, parts in words.items():
        for part, answer in parts.items():
            if answer[0] == 1:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(
                        learned_date=date.today() +
                        timedelta(days=answer[1] * 3),
                        repeat_delay=answer[1] * 3,
                    )
                )
            if answer[0] == 0:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(
                        answer=answer[0],
                        learned_date=date.today(),
                        repeat_delay=5,
                    )
                )
    db.session.commit()


def load_word(word, lang):
    model = single_model(lang)
    words = model.query.filter(model.word == word).all()
    prep_words = {}
    for word in words:
        prep_words[word.part] = {
            "translation": [trans.word for trans in word.translation],
            "id": word.id,
            "answer": word.answer,
        }
    return prep_words
