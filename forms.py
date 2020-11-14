from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class NewUserNameForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])

class UploadAvatarForm(FlaskForm):
    file = FileField('Upload (<=3M)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()

class BuyStyleForm(FlaskForm):
    bthing = HiddenField()
