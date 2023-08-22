from models import (
    db,
    English,
    English_part,
    Parts,
    Russian,
    Russian_part,
    Languages,
)
from flask import json
from datetime import date, timedelta
from sqlalchemy import func


def get_languages():
    return [lang.language for lang in Languages.query.all()]


def get_parts():
    return [part.part for part in Parts.query.all()]


def load_models(lang):
    all_models = {
        classes.__tablename__: classes for classes in db.Model.__subclasses__()
    }
    print(lang)
    models = {
        "primary_model": all_models[lang["primary_language"]],
        "primary_part_model": all_models[lang["primary_language"] + "_part"],
        "secondary_model": all_models[lang["secondary_language"]],
        "secondary_part_model": all_models[lang["secondary_language"] + "_part"],
        "translation_model": [
            s
            for s in all_models.keys()
            if (lang["primary_language"] in s and lang["secondary_language"] in s)
        ],
    }
    return models


def all_words(lang):
    print(lang)
    main_model = load_models(lang)["primary_model"]
    words = db.session.query(main_model.word).all()
    word_list = [word.word for word in words]
    return json.dumps(word_list, ensure_ascii=False)


def add_translation(model, word, part):
    trans = model.query.filter(model.word == word).all()
    existing_tran = model.query.filter(model.word == word, model.part == part).first()
    verified = False
    for tran in trans:
        if tran.verified == True:
            verified = True
        tran.answer = 0
    if existing_tran is None:
        new_tran = model(word=word, part=part, verified=verified)
        db.session.add(new_tran)
        return new_tran
    return existing_tran


def add_words(lang, word, id, part, translations):
    print(lang, word, id, part, translations)
    add_model, add_part, trans_model, trans_part = double_model(lang)
    if id == "":
        add_word = add_model(word=word, verified=True)
        db.session.flush()
        part_id = Parts.query.filter_by(part=part).first()
        add_word_part = add_part(word_id=add_word.id, part_id=part_id)
        db.session.add(add_word)
        db.session.add(add_word_part)
        for translation in translations:
            add_word.translation.append(add_translation(trans_model, translation, part))
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
            add_word.translation.append(add_translation(trans_model, translation, part))
    db.session.commit()


def study_words(lang):
    model = single_model(lang)
    words = model.query.filter(model.answer < 100, model.verified == True).all()
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
    return prep_words


def learned(lang, words):
    model = single_model(lang)
    for word, parts in words.items():
        for part, data in parts.items():
            if data["answer"] == 100:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(
                        answer=data["answer"],
                        learned_date=date.today() + timedelta(days=5),
                        repeat_delay=5,
                    )
                )
            else:
                model.query.filter(model.word == word, model.part == part).update(
                    dict(answer=data["answer"])
                )
    db.session.commit()


def not_verified(lang):
    main_model = load_models(lang)["primary_model"]
    words = main_model.query.filter(main_model.verified == False).all()
    word_list = [word.word for word in words]
    return word_list


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
                        learned_date=date.today() + timedelta(days=answer[1] * 3),
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
    models = load_models(lang)
    main_model = models["main_model"]
    sec_model = models["secondary_model"]
    word = main_model.query.filter_by(word=word).first()
    prep_words = {"word": word.word, "id": word.id, "parts": {}}
    for part in word.word_parts:
        prep_words["parts"][part.part.part] = [
            word.word.word for word in getattr(part, sec_model.__tablename__)
        ]
    return prep_words
