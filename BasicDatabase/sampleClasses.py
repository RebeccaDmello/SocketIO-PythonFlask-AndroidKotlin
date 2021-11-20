from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CreateTask(FlaskForm):
    title = TextField('Task Title',validators=[DataRequired()])
    shortdesc = TextField('Short Description',validators=[DataRequired()])
    priority = IntegerField('Priority',validators=[DataRequired()])
    create = SubmitField('Create')
    

class DeleteTask(FlaskForm):
    key = TextField('Task ID')
    title = TextField('Task Title')
    delete = SubmitField('Delete')

class UpdateTask(FlaskForm):
    key = TextField('Task Key',validators=[DataRequired()])
    shortdesc = TextField('Short Description',validators=[DataRequired()])
    update = SubmitField('Update')

class ResetTask(FlaskForm):
    reset = SubmitField('Reset')

