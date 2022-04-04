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
    russian_word = db.Column('russian_word', db.String(100))
    correct_count = db.Column('correct_count', db.Integer)

    def __init__(self, russian_word, correct_count):
        self.russian_word = russian_word
        self.correct_count = correct_count



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword", methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        translations = request.form['translation'].split('/')
        ru_word = Russian(request.form['name'], request.form['part'])
        print (ru_word.word != LearningRus.query.filter_by(russian_word=ru_word.word).first())
        if ru_word.word != LearningRus.query.filter_by(russian_word=ru_word.word).first():
            print(request.form['name'])
            new_word = LearningRus('dfgdf',0)
            print(new_word.russian_word)
            db.session.add(new_word)
        db.session.add(ru_word)
        for item in translations:
            eng_word = English(item, request.form['part'])  
            db.session.add(eng_word)
            db.session.flush()
            translation = Translation(eng_word.id, ru_word.id)
            db.session.add(translation)
        db.session.commit()
        # flash('Record was successfully added')
        return redirect(url_for('index'))
    return render_template("AddWords.html")


@app.route("/view")
def view():
    return render_template("viewWords.html", words = LearningRus.query.all())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)