# forms.py

from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class UploadAvatarForm(FlaskForm):
    avatar = FileField('Upload Avatar', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
