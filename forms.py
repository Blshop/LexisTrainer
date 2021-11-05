from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField("username",
                            validators=[DataRequired(), Length(min=2, max=20)])