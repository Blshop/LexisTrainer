from models import (
    db,
    Parts,
    Languages,
)
from flask import json
from datetime import date
from sqlalchemy import func


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

    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"
    relation_attr = f"{primary_model.__tablename__}_{secondary_model.__tablename__}"

    if new_word["id"] == "":
        word_obj = primary_model(word_desc=new_word["word"])
        setattr(word_obj, f"{secondary_model.__tablename__}_verified", True)
        setattr(word_obj, repeat_attr, date.today())
        db.session.add(word_obj)
        db.session.flush()

        for part, translations in new_word["parts"].items():
            part_obj = Parts.query.filter_by(part_desc=part).first()
            word_part = primary_part_model(word_id=word_obj.id, part_id=part_obj.id)
            db.session.add(word_part)
            db.session.flush()

            for transl in translations:
                translation = add_translation(
                    secondary_model,
                    primary_model,
                    secondary_part_model,
                    part_obj.id,
                    transl,
                )
                getattr(word_part, relation_attr).append(translation)

    else:
        word_obj = primary_model.query.filter_by(word_desc=new_word["word"]).first()
        setattr(word_obj, f"{secondary_model.__tablename__}_answer", 0)
        setattr(word_obj, f"{secondary_model.__tablename__}_verified", True)
        setattr(word_obj, repeat_attr, date.today())
        db.session.flush()

        existing_word = load_word(new_word["word"], lang)

        for part, new_translations in new_word["parts"].items():
            part_obj = Parts.query.filter_by(part_desc=part).first()
            word_part = primary_part_model.query.filter_by(
                part_id=part_obj.id, word_id=word_obj.id
            ).first()

            if not word_part:
                word_part = primary_part_model(word_id=word_obj.id, part_id=part_obj.id)
                db.session.add(word_part)
                db.session.flush()

            existing_translations = set(existing_word["parts"].get(part, []))
            new_translations_set = set(new_translations)

            # Remove old translations
            for transl in existing_translations - new_translations_set:
                translation = add_translation(
                    secondary_model,
                    primary_model,
                    secondary_part_model,
                    part_obj.id,
                    transl,
                )
                getattr(word_part, relation_attr).remove(translation)

            # Add new translations
            for transl in new_translations_set - existing_translations:
                translation = add_translation(
                    secondary_model,
                    primary_model,
                    secondary_part_model,
                    part_obj.id,
                    transl,
                )
                getattr(word_part, relation_attr).append(translation)

            # Remove part if empty
            if new_translations == [""]:
                setattr(word_part, relation_attr, [])
                word_obj.word_parts.remove(word_part)

    db.session.commit()


def add_translation(secondary_model, primary_model, part_model, part_id, word):
    relation_prefix = primary_model.__tablename__

    # Try to find existing translation
    translation = secondary_model.query.filter_by(word_desc=word).first()

    if not translation:
        translation = secondary_model(word_desc=word)
        db.session.add(translation)
        db.session.flush()

    # Initialize spaced repetition fields
    setattr(translation, f"{relation_prefix}_answer", 0)
    setattr(translation, f"{relation_prefix}_delay", 5)

    # Ensure part relationship exists
    translation_part = part_model.query.filter_by(
        part_id=part_id, word_id=translation.id
    ).first()

    if not translation_part:
        translation_part = part_model(word_id=translation.id, part_id=part_id)
        db.session.add(translation_part)
        db.session.flush()

    return translation_part


def study_words(lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    primary_table = primary_model.__tablename__
    secondary_table = secondary_model.__tablename__

    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"
    delay_attr = f"{secondary_model.__tablename__}_delay"
    answer_attr = f"{secondary_table}_answer"
    verified_attr = f"{secondary_table}_verified"
    relation_attr = f"{primary_table}_{secondary_table}"

    prep_words = {}

    words = primary_model.query.filter(
        getattr(primary_model, answer_attr) < 100,
        getattr(primary_model, verified_attr) == True,
        func.date(getattr(primary_model, repeat_attr)) < func.date("now"),
    ).all()

    for word in words:
        prep_words[word.word_desc] = {
            "id": word.id,
            "answer": getattr(word, answer_attr),
            "parts": {},
        }

        for part_link in word.word_parts:
            part_name = part_link.part.part_desc
            translations = [
                t.word_part.word_desc for t in getattr(part_link, relation_attr)
            ]
            prep_words[word.word_desc]["parts"][part_name] = translations

    return prep_words


def learned(lang, words):
    words = json.loads(words)
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    delay_attr = f"{secondary_model.__tablename__}_delay"
    answer_attr = f"{secondary_model.__tablename__}_answer"
    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"

    for word_desc, data in words.items():
        word_obj = primary_model.query.filter_by(word_desc=word_desc).first()
        if not word_obj:
            continue  # skip if word not found

        setattr(word_obj, answer_attr, data["answer"])
        setattr(word_obj, repeat_attr, date.today())

        if data["answer"] == 100:
            setattr(word_obj, delay_attr, 5)

    db.session.commit()


def not_verified(lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    verified_attr = f"{secondary_model.__tablename__}_verified"

    words = (
        primary_model.query.filter(getattr(primary_model, verified_attr) == False)
        .with_entities(primary_model.word_desc)
        .all()
    )

    return [word_desc for (word_desc,) in words]


from datetime import date


def stats(lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    delay_attr = f"{secondary_model.__tablename__}_delay"
    answer_attr = f"{secondary_model.__tablename__}_answer"
    verified_attr = f"{secondary_model.__tablename__}_verified"
    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"

    # Total words
    all_words = db.session.query(primary_model.word_desc).distinct().count()

    # Learned words
    learned = (
        db.session.query(primary_model.word_desc)
        .filter(
            getattr(primary_model, answer_attr) == 100,
            getattr(primary_model, verified_attr) == True,
        )
        .distinct()
        .count()
    )

    # Words still being learned
    learning_subq = (
        db.session.query(
            primary_model.word_desc, getattr(primary_model, answer_attr).label("answer")
        )
        .filter(
            getattr(primary_model, answer_attr) < 100,
            getattr(primary_model, verified_attr) == True,
        )
        .distinct()
        .subquery()
    )

    to_learn = (
        db.session.query(learning_subq.c.answer, db.func.count(learning_subq.c.answer))
        .group_by(learning_subq.c.answer)
        .all()
    )

    count = db.session.query(learning_subq.c.answer).count()

    # Words due for review

    to_review = (
        db.session.query(primary_model.word_desc)
        .filter(
            getattr(primary_model, answer_attr) == 100,
            getattr(primary_model, verified_attr) == True,
            func.date(
                getattr(primary_model, repeat_attr),
                "+"
                + func.cast(getattr(primary_model, delay_attr), db.String)
                + " days",
            )
            < func.date("now"),
        )
        .distinct()
        .count()
    )

    return {
        "all_words": all_words,
        "remaining": all_words - learned,
        "learned": learned,
        "count": to_learn,
        "to_learn": count,
        "to_review": to_review,
    }


def prep_revew(lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    delay_attr = f"{secondary_model.__tablename__}_delay"
    answer_attr = f"{secondary_model.__tablename__}_answer"
    verified_attr = f"{secondary_model.__tablename__}_verified"
    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"
    relation_attr = f"{primary_model.__tablename__}_{secondary_model.__tablename__}"

    prep_words = {}

    words = primary_model.query.filter(
        getattr(primary_model, answer_attr) == 100,
        getattr(primary_model, verified_attr) == True,
        func.date(
            getattr(primary_model, repeat_attr),
            "+" + func.cast(getattr(primary_model, delay_attr), db.String) + " days",
        )
        < func.date("now"),
    ).all()

    for word in words:
        prep_words[word.word_desc] = {
            "id": word.id,
            "answer": getattr(word, answer_attr),
            "parts": {},
        }

        for part_link in word.word_parts:
            part_name = part_link.part.part_desc
            translations = [
                t.word_part.word_desc for t in getattr(part_link, relation_attr)
            ]
            prep_words[word.word_desc]["parts"][part_name] = translations

    return prep_words


def reviewed(lang, words):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    delay_attr = f"{secondary_model.__tablename__}_delay"
    answer_attr = f"{secondary_model.__tablename__}_answer"
    repeat_attr = f"{secondary_model.__tablename__}_repeat_date"

    for word_desc, score in words.items():
        word_obj = primary_model.query.filter_by(word_desc=word_desc).first()
        if not word_obj:
            continue  # skip if word not found

        if score == 100:
            delay = getattr(word_obj, delay_attr)
            setattr(word_obj, repeat_attr, date.today())
            setattr(word_obj, delay_attr, delay * 3)
        else:
            setattr(word_obj, repeat_attr, date.today())
            setattr(word_obj, answer_attr, 0)
            setattr(word_obj, delay_attr, 5)

    db.session.commit()


def load_word(word_desc, lang):
    print(word_desc)
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]

    answer_attr = f"{secondary_model.__tablename__}_answer"
    relation_attr = f"{primary_model.__tablename__}_{secondary_model.__tablename__}"

    word_obj = primary_model.query.filter_by(word_desc=word_desc).first()
    if not word_obj:
        return None  # or raise an exception, depending on your use case

    prep_words = {
        "word": word_obj.word_desc,
        "id": word_obj.id,
        "answer": getattr(word_obj, answer_attr),
        "parts": {},
    }

    for part_link in word_obj.word_parts:
        part_name = part_link.part.part_desc
        translations = [
            t.word_part.word_desc for t in getattr(part_link, relation_attr)
        ]
        prep_words["parts"][part_name] = translations

    return prep_words


def add_word_new(new_word, lang):
    models = load_models(lang)
    primary_model = models["primary_model"]
    secondary_model = models["secondary_model"]
    primary_part_model = models["primary_part_model"]
    secondary_part_model = models["secondary_part_model"]

    relation_attr = f"{primary_model.__tablename__}_{secondary_model.__tablename__}"
    answer_attr = f"{secondary_model.__tablename__}_answer"
    verified_attr = f"{secondary_model.__tablename__}_verified"

    word_desc = new_word["word"]
    word_obj = primary_model.query.filter_by(word_desc=word_desc).first()

    if not word_obj:
        word_obj = primary_model(word_desc=word_desc)
        db.session.add(word_obj)
        db.session.flush()

    setattr(word_obj, answer_attr, 0)
    setattr(word_obj, verified_attr, True)

    for part_name, translations in new_word["parts"].items():
        part_obj = Parts.query.filter_by(part_desc=part_name).first()
        word_part = primary_part_model.query.filter_by(
            word_id=word_obj.id, part_id=part_obj.id
        ).first()

        if not word_part:
            word_part = primary_part_model(word_id=word_obj.id, part_id=part_obj.id)
            db.session.add(word_part)
            db.session.flush()

        relation_list = getattr(word_part, relation_attr)

        # Clear existing translations
        relation_list[:] = []

        if translations == [""]:
            db.session.delete(word_part)
            continue

        for transl in translations:
            translation = add_translation(
                secondary_model, secondary_part_model, part_obj.id, transl
            )
            relation_list.append(translation)

    db.session.commit()
