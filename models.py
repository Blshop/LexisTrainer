from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


translation = db.Table(
    "translation",
    db.Column("english_id", db.Integer, db.ForeignKey("english.id")),
    db.Column("russian_id", db.Integer, db.ForeignKey("russian.id")),
)


class English(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column("word", db.String(100))
    part = db.Column("part", db.String(20))
    answer = db.Column("answer", db.Integer, default=0)
    verified = db.Column("verified", db.Boolean, default=False, nullable=False)
    translation = db.relationship(
        "Russian", secondary=translation, backref="translations"
    )


class Russian(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column("word", db.String(100))
    part = db.Column("part", db.String(20))
    answer = db.Column("answer", db.Integer, default=0)
    verified = db.Column("verified", db.Boolean, default=False, nullable=False)
    translation = db.relationship(
        "English", secondary=translation, backref="translations"
    )


class RepeatRus(db.Model):
    word_id = db.Column("word_id", db.Integer, primary_key=True)
    answer = db.Column("answer", db.Integer)

    def __init__(self, word_id, answer):
        self.word_id = word_id
        self.answer = answer


class RepeatEng(db.Model):
    word_id = db.Column("word_id", db.Integer, primary_key=True)
    answer = db.Column("answer", db.Integer)

    def __init__(self, word_id, answer):
        self.word_id = word_id
        self.answer = answer
