from flask import Flask, render_template
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

class Translation(db.Model):
    english_id = db.Column('english_id', db.Integer, db.ForeignKey('english.id'), primary_key=True)
    russian_id = db.Column('russian_id', db.Integer, db.ForeignKey('russian.id'), primary_key=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addword")
def add_word():
    return render_template("AddWords.html")


# db.create_all()


if __name__ == '__main__':
    app.run(debug=True)