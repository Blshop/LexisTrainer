from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Languages.db'


db = SQLAlchemy(app)
class English(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    word = db.Column('word', db.String(100))
    part = db.Column('part', db.String(20))

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




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword", methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        translations = request.form['translation'].split('/')
        for item in translations:
            word = Russian(item, request.form['part'])  
            db.session.add(word)
        db.session.commit()
        # flash('Record was successfully added')
        return redirect(url_for('index'))
    return render_template("AddWords.html")


# db.create_all()


if __name__ == '__main__':
    app.run(debug=True)