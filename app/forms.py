from flask_wtf import FlaskForm
from wtforms import validators
import wtforms as wf
from app.models import Employee, User


class EmployeeForm(FlaskForm):
    full_name = wf.StringField(label="Имя", validators=[
        wf.validators.DataRequired(),
    ])
    phone = wf.StringField(label="Номер телефона", validators=[
        wf.validators.DataRequired(),
    ])
    short_info = wf.TextAreaField(label="Краткая информация", validators=[
        wf.validators.DataRequired(),
    ])
    experience = wf.IntegerField(label="Опыт работы", validators=[
        wf.validators.DataRequired(),
    ])
    preferred_position = wf.StringField(label="Номер телефона")
    submit = wf.StringField("Ok")

    def validate_full_name(self, full_name):
        if " " not in full_name:
            raise validators.ValidationError("ФИО должны быть полностью")

class UserForm(FlaskForm):
    username = wf.StringField(label="Название должности", validators=[
        wf.validators.DataRequired(),
    ])
    password = wf.PasswordField("Пароль", validators=[wf.validators.DataRequired(),
                                                      wf.validators.Length(min=8, max=30)
                                                      ])
    submit = wf.StringField("Ok")