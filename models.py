from flask_sqlalchemy import SQLAlchemy
from datetime import date
db = SQLAlchemy()

translation = db.Table(
    "translation",
    db.Column("english_id", db.Integer, db.ForeignKey("english_temp.id")),
    db.Column("russian_id", db.Integer, db.ForeignKey("russian_temp.id")),
)


class English_temp(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column("word", db.String(100))
    part = db.Column("part", db.String(20))
    answer = db.Column("answer", db.Integer, default=0)
    learned_date = db.Column("learned_date", db.Date, default=date.today())
    repeat_delay = db.Column("repeat_delay", db.Integer, default=5)
    verified = db.Column("verified", db.Boolean, default=False, nullable=False)
    translation = db.relationship(
        "Russian_temp",
        secondary=translation,
        backref="translations",
        overlaps="translation,translations",
    )

     
class Russian_temp(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column("word", db.String(100))
    part = db.Column("part", db.String(20))
    answer = db.Column("answer", db.Integer, default=0)
    learned_date = db.Column("learned_date", db.Date, default=date.today())
    repeat_delay = db.Column("repeat_delay", db.Integer, default=5)
    verified = db.Column("verified", db.Boolean, default=False, nullable=False)
    translation = db.relationship(
        "English_temp",
        secondary=translation,
        backref="translations",
        overlaps="translation,translations",
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


class Parts(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    part = db.Column("part", db.String(10), unique=True, nullable=False)


class English(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    word = db.Column("word", db.String(30), unique=True)
    answer = db.Column("answer", db.Integer, nullable=False, default=0)
    verified = db.Column("verified", db.Boolean, nullable=False, default=False)
    delay = db.Column("delay", db.Interval, nullable=False, default=5)
    date_repeat = db.Column("date_repeat", db.Date, nullable=False, default=date.today())