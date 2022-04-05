from email.policy import default
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Languages.db'


db = SQLAlchemy(app)
class English(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    part = db.Column('part', db.String(20))
    def __init__(self, word, part):
        self.word = word
        self.part = part

class Russian(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    part = db.Column('part', db.String(20))

    def __init__(self, word, part):
        self.word = word
        self.part = part

class Translation(db.Model):
    
    english_id = db.Column('english_id', db.Integer, db.ForeignKey('english.id'), primary_key=True)
    russian_id = db.Column('russian_id', db.Integer, db.ForeignKey('russian.id'), primary_key=True)
    def __init__(self, english_id, russian_id):
        self.english_id = english_id
        self.russian_id = russian_id

class LearningRus(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    answer = db.Column('answer', db.Integer)

    def __init__(self, word, answer):
        self.word = word
        self.answer = answer

class LearningEng(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    answer = db.Column('answer', db.Integer)

    def __init__(self, word, answer):
        self.word = word
        self.answer = answer


class RepeatRus(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    answer = db.Column('answer', db.Integer)

    def __init__(self, word, answer):
        self.word = word
        self.answer = answer

class RepeatEng(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    answer = db.Column('answer', db.Integer)

    def __init__(self, word, answer):
        self.word = word
        self.answer = answer


def learning(words):
    return render_template("learn.html", words=words)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword", methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        translations = request.form['translation'].split('/')
        if Russian.query.filter_by(word=request.form['word'],part=request.form['part']).first() is None:
            ru_word = Russian(request.form['word'], request.form['part'])
            new_word = LearningRus(request.form['word'],0)
            db.session.add(new_word)
            db.session.add(ru_word)
            for item in translations:
                if English.query.filter_by(word=item, part=request.form['part']).first() is None:  
                    eng_word = English(item, request.form['part'])
                    db.session.add(eng_word)
                    db.session.flush()
                    translation = Translation(eng_word.id, ru_word.id)
                    db.session.add(translation)
                else:
                    eng_word = English.query.filter_by(word=item, part=request.form['part']).first()
                    translation = Translation(eng_word.id, ru_word.id)
                    db.session.add(translation)
            db.session.commit()
            # flash('Record was successfully added')
            return redirect(url_for('index'))
    return render_template("AddWords.html")


@app.route("/view")
def view():
    return render_template("viewWords.html", words = LearningRus.query.all())

@app.route("/learn")
def learn():
    words = LearningRus.query.filter(LearningRus.answer<100).all()
    learning(words)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)