from flask import Flask, render_template
from flask.typing import ResponseReturnValue
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Lexis.db'
db = SQLAlchemy(app)

class all_lang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(80), unique=True, nullable=False)



@app.route("/")
def index():
    return(render_template('index.html'))

if __name__ == '__main__':
    app.run(debug=True)