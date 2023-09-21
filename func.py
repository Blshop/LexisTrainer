from models import (
    db,
    Parts,
    Languages,
)
from flask import json
from datetime import date, timedelta


def get_languages():
    return [lang.language for lang in Languages.query.all()]


def get_parts():
    return [part.part_desc for part in Parts.query.all()]


def load_models(lang):
    all_models = {
        classes.__tablename__: classes for classes in db.Model.__subclasses__()
    }
    models = {
        "primary_model": all_models[lang["primary_language"]],
        "primary_part_model": all_models[lang["primary_language"] + "_part"],
        "secondary_model": all_models[lang["secondary_language"]],
        "secondary_part_model": all_models[lang["secondary_language"] + "_part"],
    }
    return models


def get_all_words(lang):
    primary_model = load_models(lang)["primary_model"]
    words = db.session.query(primary_model.word_desc).all()
    word_list = [word.word_desc for word in words]
    return json.dumps(word_list, ensure_ascii=False)


def add_word(new_word, lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    primary_part_model = models["primary_part_model"]
    secondary_part_model = models["secondary_part_model"]

    if new_word["id"] == "":
        add_word = primary_model(word_desc=new_word["word"])
        setattr(add_word, lang["secondary_language"], True)
        db.session.add(add_word)
        db.session.flush()
        for part in new_word["parts"].keys():
            add_part = Parts.query.filter_by(part_desc=part).first()
            add_word_part = primary_part_model(word_id=add_word.id, part_id=add_part.id)
            db.session.add(add_word_part)
            for transl in new_word["parts"][part]:
                translation = add_translation(
                    secondary_model, secondary_part_model, add_part.id, transl
                )
                getattr(
                    add_word_part,
                    (primary_model.__tablename__ + "_" + secondary_model.__tablename__),
                ).append(translation)
    else:
        add_word = primary_model.query.filter_by(word_desc=new_word["word"]).first()
        add_word.answer = 0
        for part in new_word["parts"].keys():
            add_part = Parts.query.filter_by(part_desc=part).first()
            add_word_part = primary_part_model.query.filter(
                primary_part_model.part_id == add_part.id,
                primary_part_model.word_id == add_word.id,
            ).first()
            if not add_word_part:
                add_word_part = primary_part_model(
                    word_id=add_word.id, part_id=add_part.id
                )
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
    translation = model.query.filter_by(word_desc=word).first()
    if translation:
        translation_part = part_model.query.filter(
            part_model.part_id == part_id, part_model.word_id == translation.id
        ).first()
        if not translation_part:
            translation_part = part_model(word_id=translation.id, part_id=part_id)
        db.session.add(translation_part)
    else:
        translation = model(word_desc=word)
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
        primary_model.answer < 100,
        getattr(primary_model, secondary_model.__tablename__) == True,
    ).all()
    for word in words:
        prep_words[word.word_desc] = {"id": word.id, "answer": word.answer, "parts": {}}
        for part in word.word_parts:
            prep_words[word.word_desc]["parts"][part.part.part_desc] = [
                word.word_part.word_desc
                for word in getattr(
                    part,
                    (primary_model.__tablename__ + "_" + secondary_model.__tablename__),
                )
            ]
    return prep_words


def learned(lang, words):
    models = load_models(lang)
    primary_model = models["primary_model"]
    for word in words.keys():
        if words[word]["answer"] == 100:
            delay = primary_model.query.filter_by(word_desc=word).first().delay
            primary_model.query.filter_by(word_desc=word).update(
                dict(
                    answer=words[word]["answer"],
                    repeat_date=date.today() + timedelta(days=delay),
                )
            )
        else:
            primary_model.query.filter_by(word_desc=word).update(
                dict(answer=words[word]["answer"])
            )
    db.session.commit()


def not_verified(lang):
    main_model = load_models(lang)["primary_model"]
    words = main_model.query.filter(
        getattr(main_model, lang["secondary_language"]) == False
    ).all()
    word_list = [word.word_desc for word in words]
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
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    prep_words = {}
    words = primary_model.query.filter(
        primary_model.answer == 100,
        getattr(primary_model, secondary_model.__tablename__) == True,
        primary_model.repeat_date < date.today(),
    ).all()
    for word in words:
        prep_words[word.word_desc] = {"id": word.id, "answer": word.answer, "parts": {}}
        for part in word.word_parts:
            prep_words[word.word_desc]["parts"][part.part.part_desc] = [
                word.word_part.word_desc
                for word in getattr(
                    part,
                    (primary_model.__tablename__ + "_" + secondary_model.__tablename__),
                )
            ]
    print(prep_words)
    return prep_words


def reviewed(lang, words):
    print(words)
    models = load_models(lang)
    primary_model = models["primary_model"]
    for word in words.keys():
        if words[word]["answer"] == 100:
            delay = primary_model.query.filter_by(word_desc=word).first().delay
            primary_model.query.filter_by(word_desc=word).update(
                dict(
                    answer=words[word]["answer"],
                    repeat_date=date.today() + timedelta(days=delay),
                    delay=delay * 3,
                )
            )
        else:
            primary_model.query.filter_by(word_desc=word).update(
                dict(answer=0, delay=5)
            )
    db.session.commit()


def load_word(word, lang):
    models = load_models(lang)
    main_model = models["primary_model"]
    sec_model = models["secondary_model"]
    word = main_model.query.filter_by(word_desc=word).first()
    prep_words = {
        "word": word.word_desc,
        "id": word.id,
        "answer": word.answer,
        "parts": {},
    }
    for part in word.word_parts:
        prep_words["parts"][part.part.part_desc] = [
            word.word_part.word_desc
            for word in getattr(
                part, (main_model.__tablename__ + "_" + sec_model.__tablename__)
            )
        ]
    return prep_words
