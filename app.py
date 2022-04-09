from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, json
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

    english_id = db.Column('english_id', db.Integer,
                           db.ForeignKey('english.id'), primary_key=True)
    russian_id = db.Column('russian_id', db.Integer,
                           db.ForeignKey('russian.id'), primary_key=True)

    def __init__(self, english_id, russian_id):
        self.english_id = english_id
        self.russian_id = russian_id


class LearningRus(db.Model):
    rus_id = db.Column('rus_id', db.Integer, db.ForeignKey(
        'russian.id'), primary_key=True)
    answer = db.Column('answer', db.Integer)

    def __init__(self, rus_id, answer):
        self.rus_id = rus_id
        self.answer = answer


class LearningEng(db.Model):
    eng_id = db.Column('eng_id', db.Integer, db.ForeignKey(
        'english.id'), primary_key=True)
    answer = db.Column('answer', db.Integer)

    def __init__(self, eng_id, answer):
        self.eng_id = eng_id
        self.answer = answer


class RepeatRus(db.Model):
    word_id = db.Column('word_id', db.Integer, primary_key=True)
    answer = db.Column('answer', db.Integer)

    def __init__(self, word_id, answer):
        self.word_id = word_id
        self.answer = answer


class RepeatEng(db.Model):
    word_id = db.Column('word_id', db.Integer, primary_key=True)
    answer = db.Column('answer', db.Integer)

    def __init__(self, word_id, answer):
        self.word_id = word_id
        self.answer = answer


def serialize(words):
    word_dict = {}
    n = 1
    for word in words:
        word_dict[n] = [word.word, word.part, word.answer]
        n += 1
    return word_dict


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword", methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        translations = request.form['translation'].split('/')
        if Russian.query.filter_by(word=request.form['word'], part=request.form['part']).first() is None:
            ru_word = Russian(request.form['word'], request.form['part'])
            db.session.add(ru_word)
            db.session.flush()
            new_word = LearningRus(ru_word.id, 0)
            db.session.add(new_word)
            for item in translations:
                if English.query.filter_by(word=item, part=request.form['part']).first() is None:
                    eng_word = English(item, request.form['part'])
                    db.session.add(eng_word)
                    db.session.flush()
                    translation = Translation(eng_word.id, ru_word.id)
                    db.session.add(translation)
                else:
                    eng_word = English.query.filter_by(
                        word=item, part=request.form['part']).first()
                    translation = Translation(eng_word.id, ru_word.id)
                    db.session.add(translation)
            db.session.commit()
            # flash('Record was successfully added')
            return redirect(url_for('index'))
    return render_template("AddWords.html")


@app.route("/view")
def view():
    return render_template("viewWords.html", words=LearningRus.query.all())


@app.route("/learn", methods=['GET', 'POST'])
def learn():
    # if request.method == 'POST':
    #     data = json.loads(request.form.get('data'))
    #     print(data)
    #     return render_template("viewWords.html", words=LearningRus.query.all())
    # words = LearningRus.query.filter(LearningRus.answer<100).all()
    words = db.session.query(Russian.word, Russian.part,
                             Translation.russian_id, Translation.english_id, LearningRus.rus_id, LearningRus.answer).join(Translation).join(LearningRus).all()
    # print(serialize(words))
    return render_template("learn.html", words=serialize(words))

@app.route("/finish", methods=['GET', 'POST'])
def finish():
    data = json.loads(request.form.get('data'))
    print(data)
    return jsonify('everything is good')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
