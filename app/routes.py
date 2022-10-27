from app import app
from flask import render_template, flash, url_for, redirect
from flask_login import current_user
from .models import User, Pokedex

@app.route('/')
def homePage():
    users = User.query.all()

    team_set = dict()
    for u in users:
        my_team = u.my_team.all()
        print(my_team)
        team_set[u.username] = my_team

    return render_template('index.html', team_set=team_set)

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/battle')
def battlePage():
    users = User.query.all()

    team_set = dict()
    for u in users:
        my_team = u.my_team.all()
        print(my_team)
        team_set[u.username] = my_team

    return render_template('battle.html', team_set=team_set)

@app.route('/battle/results')
def battle():
    flash('VICTORY!!!', 'success')
    return redirect(url_for('homePage'))