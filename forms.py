from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from main import User
from flask import flash


class RegistrationForm(FlaskForm):
    name = StringField('Přezdívka *')
    email = StringField('Email *', validators=[Email("Zadej opravdový email")])
    jidelna = StringField('Přihlašovací jméno do iCanteen')
    jidelna_heslo = StringField('Heslo do iCanteen')
    password = PasswordField('Heslo *')
    submit = SubmitField('Zaregistovat')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()

        if user:
            raise ValidationError('Tuto přezdívku už někdo používá')

        if name is None or len(name.data) > 15 or len(name.data) < 2:
            raise ValidationError('Jméno musí být delší než 2 a kratší než 15 znaků')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('Tento email už někdo používá')

    def validate_jidelna(self, jidelna):
        if jidelna.data != "":
            jidelna = User.query.filter_by(icanteen=jidelna.data).first()
            if jidelna:
                raise ValidationError('Tuto CanteenID již někdo používá')

    def validate_password(self, password):
        if password is None or len(password.data) < 6:
            raise ValidationError('Jméno musí být delší než 6 znaky')


class LoginForm(FlaskForm):
    name = StringField('Přezdívka:')
    password = PasswordField('Heslo:')
    remember = BooleanField('Zapamatuj si mě')
    submit = SubmitField('Přihlásit')


class UpdateAccountForm(FlaskForm):
    name = StringField('Přezdívka:', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    jidelna = StringField('iCanteen: ', validators=[Length(min=0, max=10)])
    jidelna_heslo = StringField('iC. heslo: ')
    picture = FileField('Profilovka:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Uložit')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                flash('Tato přezdívka je zabraná', 'danger')
                raise ValidationError()

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()

            if email:
                flash('Tento email je zabraný', 'danger')
                raise ValidationError()


class PostForm(FlaskForm):
    title = StringField('Název:', validators=[DataRequired()])
    content = TextAreaField('Obsah:', validators=[DataRequired()])
    picture = FileField('Obrázek:', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    jidlo = StringField('Název jídla:', validators=[DataRequired()])
    submit = SubmitField('Přidat')


class PriznaniForm(FlaskForm):
    content = TextAreaField('Obsah:', validators=[DataRequired()])
    picture = FileField('Obrázek:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Přidat')


class HlaskaForm(FlaskForm):
    ucitel = SelectField('Učitel:', choices=[('Kořínek', 'Milan Kořínek'), ('Halašková', 'Halašková'), ('Janšta', 'Petr Janšta')])
    content = TextAreaField('Obsah:', validators=[DataRequired()])
    submit = SubmitField('Přidat')


class CommentForm(FlaskForm):
    content = StringField('Obsah:', validators=[DataRequired()])
    picture = FileField('Obrázek:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Přidat')


class RequestResetForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Odeslat')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if not email:
            raise ValidationError('Tento email nikdo nepoužívá')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Heslo')
    submit = SubmitField('Potvrdit')
