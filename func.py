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
    main_model = load_models(lang)["primary_model"]
    words = db.session.query(main_model.word).all()
    word_list = [word.word for word in words]
    return json.dumps(word_list, ensure_ascii=False)


def add_words(new_word, lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    primary_part_model = models["primary_part_model"]
    secondary_part_model = models["secondary_part_model"]

    if new_word["id"] == "":
        add_word = primary_model(word=new_word["word"], verified=True)
        db.session.add(add_word)
        db.session.flush()
        for part in new_word["parts"].keys():
            add_part = Parts.query.filter_by(part=part).first()
            add_word_part = primary_part_model(word_id=add_word.id, part_id=add_part.id)
            db.session.add(add_word_part)
            for transl in new_word["parts"][part]:
                translation = add_translation(
                    secondary_model, secondary_part_model, add_part.id, transl
                )
                getattr(add_word_part, secondary_model.__tablename__).append(
                    translation
                )
    else:
        add_word = primary_model.query.filter_by(word=new_word["word"]).first()
        add_word.answer = 0
        for part in new_word["parts"].keys():
            add_part = Parts.query.filter_by(part=part).first()
            add_word_part = primary_part_model.query.filter(
                primary_part_model.part_id == add_part.id,
                primary_part_model.word_id == add_word.id,
            ).first()
            if not add_word_part:
                add_word_part = primary_part_model(
                    word_id=add_word.id, part_id=add_part.id
                )
            old_translations = getattr(add_word_part, secondary_model.__tablename__)
            getattr(add_word_part, secondary_model.__tablename__)[:] = []
            for transl in new_word["parts"][part]:
                translation = add_translation(
                    secondary_model, secondary_part_model, add_part.id, transl
                )
                getattr(add_word_part, secondary_model.__tablename__).append(
                    translation
                )
    db.session.commit()


def add_translation(model, part_model, part_id, word):
    translation = model.query.filter_by(word=word).first()
    if translation:
        translation_part = part_model.query.filter(
            part_model.part_id == part_id, part_model.word_id == translation.id
        ).first()
        if not translation_part:
            translation_part = part_model(word_id=translation.id, part_id=part_id)
        db.session.add(translation_part)
    else:
        translation = model(word=word)
        db.session.add(translation)
        db.session.flush()
        translation_part = part_model(word_id=translation.id, part_id=part_id)
        db.session.add(translation_part)
    db.session.commit()
    return translation_part


def study_words(lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    prep_words = {}
    words = primary_model.query.filter(
        primary_model.answer < 100, primary_model.verified == True
    ).all()
    for word in words:
        prep_words[word.word] = {"id": word.id, "answer": word.answer, "parts": {}}
        for part in word.word_parts:
            prep_words[word.word]["parts"][part.part.part] = [
                word.word.word for word in getattr(part, secondary_model.__tablename__)
            ]
    print(prep_words)
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
    main_model = models["primary_model"]
    sec_model = models["secondary_model"]
    word = main_model.query.filter_by(word=word).first()
    prep_words = {"word": word.word, "id": word.id, "answer": word.answer, "parts": {}}
    for part in word.word_parts:
        prep_words["parts"][part.part.part] = [
            word.word.word for word in getattr(part, sec_model.__tablename__)
        ]
    return prep_words
