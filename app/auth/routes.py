from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, UserCreationForm
from app.models  import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/log-me-in', methods=["GET", "POST"])
def logMeIn():

    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    print("successfully logged in")
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    print("incorrect password")
            else:
                print("user does not exist")

    return render_template('log-me-in.html', form=form)

@auth.route('/signup', methods=["GET", "POST"])
def signUp():

    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)

            user = User(username, email, password)
            user.saveToDB()

            return redirect(url_for('auth.logMeIn'))

    return render_template('sign_up.html', form=form)

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('homePage'))