from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ability = StringField('Ability', validators=[DataRequired()])
    img_url = StringField('Image', validators=[DataRequired()])
    base_exp = StringField('Base Experience', validators=[DataRequired()])
    submit = SubmitField()