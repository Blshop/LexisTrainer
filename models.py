from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

# translation = db.Table(
#     "translation",
#     db.Column("english_id", db.Integer, db.ForeignKey("english_temp.id")),
#     db.Column("russian_id", db.Integer, db.ForeignKey("russian_temp.id")),
# )


# class English_temp(db.Model):
#     id = db.Column("id", db.Integer, primary_key=True)
#     word = db.Column("word", db.String(100))
#     part = db.Column("part", db.String(20))
#     answer = db.Column("answer", db.Integer, default=0)
#     learned_date = db.Column("learned_date", db.Date, default=date.today())
#     repeat_delay = db.Column("repeat_delay", db.Integer, default=5)
#     verified = db.Column("verified", db.Boolean, default=False, nullable=False)
#     translation = db.relationship(
#         "Russian_temp",
#         secondary=translation,
#         backref="translations",
#         overlaps="translation,translations",
#     )


# class Russian_temp(db.Model):
#     id = db.Column("id", db.Integer, primary_key=True)
#     word = db.Column("word", db.String(100))
#     part = db.Column("part", db.String(20))
#     answer = db.Column("answer", db.Integer, default=0)
#     learned_date = db.Column("learned_date", db.Date, default=date.today())
#     repeat_delay = db.Column("repeat_delay", db.Integer, default=5)
#     verified = db.Column("verified", db.Boolean, default=False, nullable=False)
#     translation = db.relationship(
#         "English_temp",
#         secondary=translation,
#         backref="translations",
#         overlaps="translation,translations",
#     )


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
    id = db.Column("id", db.Integer, primary_key=True)
    part = db.Column("part", db.String(10), unique=True, nullable=False)
    english_parts = db.Relationship("English_part", backref="part")
    russian_parts = db.Relationship("Russian_part", backref="part")


class English(db.Model):
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    word = db.Column("word", db.String(30), unique=True)
    answer = db.Column("answer", db.Integer, nullable=False, default=0)
    verified = db.Column("verified", db.Boolean, nullable=False, default=False)
    delay = db.Column("delay", db.Integer, nullable=False, default=5)
    repeat_date = db.Column(
        "repeat_date", db.String, nullable=False, default=date.today()
    )
    word_parts = db.Relationship("English_part", backref="word")


english_russian = db.Table(
    "english_russian",
    db.Column(
        "main_part_id", db.Integer, db.ForeignKey("english_part.id"), primary_key=True
    ),
    db.Column(
        "sec_part_id", db.Integer, db.ForeignKey("russian_part.id"), primary_key=True
    ),
)


class English_part(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    part_id = db.Column("part_id", db.Integer, db.ForeignKey("parts.id"))
    word_id = db.Column("word_id", db.Integer, db.ForeignKey("english.id"))
    russian = db.relationship(
        "Russian_part", secondary=english_russian, backref="english"
    )


class Russian(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column("word", db.String(30), unique=True)
    answer = db.Column("answer", db.Integer, nullable=False, default=0)
    verified = db.Column("verified", db.Boolean, nullable=False, default=False)
    delay = db.Column("delay", db.Integer, nullable=False, default=5)
    repeat_date = db.Column(
        "repeat_date", db.Date, nullable=False, default=date.today()
    )
    word_parts = db.Relationship("Russian_part", backref="word")


class Russian_part(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    part_id = db.Column("part_id", db.Integer, db.ForeignKey("parts.id"))
    word_id = db.Column("word_id", db.Integer, db.ForeignKey("russian.id"))


class Languages(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    language = db.Column("language", db.String(15), unique=True, nullable=False)
