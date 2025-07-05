import email
from click import confirm
from flask import Blueprint, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from db.database import session_scope
from db.models import User
from werkzeug.security import generate_password_hash


main_blueprint = Blueprint('main', __name__)



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=100, min=4)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=36)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
        if user:
            flash('Пользователь с таким именем уже существует!', category='danger')
            return redirect(url_for('main.register'), form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        with session_scope() as session:
            session.add(user)
        return redirect(url_for('main.login'))
    elif form.errors:
        flash(form.errors, category='danger')


    return render_template('register.html', form=form)

@main_blueprint.route('/login')
def login():
    pass
