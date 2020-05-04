from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):

    comment = TextAreaField('Comment...',validators=[Required()])
    submit = SubmitField('Submit')