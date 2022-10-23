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


def add_words(lang, add_word, part, translations):
    if lang == "russian":
        add_model = Russian
        trans_model = English
    elif lang == "english":
        add_model = English
        trans_model = Russian
    if add_model.query.filter_by(word=add_word, part=part).first() is None:
        add_word = add_model(word=add_word, part=part, verified=True)
        db.session.add(add_word)
        for item in translations:
            if trans_model.query.filter_by(word=item, part=part).first() is None:
                trans_word = trans_model(word=item, part=part)
                db.session.add(trans_word)
                add_word.translation.append(trans_word)
            else:
                trans_word = trans_model.query.filter_by(
                    word=item, part=part).first()
                add_word.translation.append(trans_word)
        db.session.commit()


def study_words(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    words = model.query.filter(
        model.answer < 100, model.verified == True).all()
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


def learned(lang, words):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    for word, parts in words.items():
        for part, answer in parts.items():
            model.query.filter(model.word == word, model.part == part).update(
                dict(answer=answer[0])
            )
    db.session.commit()


def all_words(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    words = model.query.all()
    prep_words = {}
    for word in words:
        if word.word in prep_words.keys():
            prep_words[word.word][word.part] = [
                word.answer,
                word.id,
                word.answer,
                [trans.word for trans in word.translation],
            ]
        else:
            prep_words[word.word] = {
                word.part: [
                    word.answer,
                    word.id,
                    word.answer,
                    [trans.word for trans in word.translation],
                ]
            }
    return prep_words


def not_verified(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
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


def edit_word(lang, word_id, edit_word, part, translations, answer):
    if lang == "russian":
        add_model = Russian
        trans_model = English
    elif lang == "english":
        add_model = English
        trans_model = Russian
    if word_id == "":
        add_word = add_model(word=edit_word, part=part, verified=True)
        db.session.add(add_word)
    elif translations == [""]:
        print("deleted")
        add_word = add_model.query.filter_by(id=word_id).first()
        add_word.translation = []
        add_model.query.filter_by(id=word_id).delete()
        db.session.commit()
        return None
    elif add_model.query.filter_by(id=word_id).first().part != part:
        add_word = add_model.query.filter_by(id=word_id).first()
        add_word.translation = []
        add_model.query.filter_by(id=word_id).delete()
        add_word = add_model(word=edit_word, part=part, verified=True)
        db.session.add(add_word)
    else:
        add_word = add_model.query.filter_by(id=word_id).first()
        add_model.query.filter_by(id=word_id).update(
            dict(word=edit_word, answer=0, verified=True)
        )
    all_trans = []
    print(all_trans)
    for trans in add_word.translation:
        print(trans.word, translations)
        if trans.word in translations:
            translations.remove(trans.word)
            all_trans.append(trans)
        else:
            pass
    add_word.translation = all_trans
    print(add_word.translation)
    print(all_trans)
    for trans in translations:
        if trans_model.query.filter_by(word=trans, part=part).first() is None:
            trans_word = trans_model(
                word=trans, part=part, answer=0, verified=False)
            db.session.add(trans_word)
            add_word.translation.append(trans_word)
            trans_model.query.filter_by(word=trans).update(dict(answer=0))
        else:
            trans_model.query.filter_by(word=trans).update(dict(answer=0))
            trans_word = trans_model.query.filter_by(
                word=trans, part=part).first()
            add_word.translation.append(trans_word)
    db.session.commit()


def stats(lang):
    if lang == "russian":
        model = Russian
    elif lang == "english":
        model = English
    all_words = len(model.query.group_by(model.word).all())
    learned = len(model.query.filter(
        model.answer == 100).group_by(model.word).all())
    to_learn = len(model.query.filter(
        model.answer < 100, model.verified == True).group_by(model.word).all())
    return [all_words, learned, to_learn]
