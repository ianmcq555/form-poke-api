from app import app
from flask import render_template

@app.route('/')
def homePage():
    people = [{
        'name': 'Ian',
        'age': 25
    },{
        'name': 'Sia',
        'age': 22
    },{
        'name': 'Caroline',
        'age': 25
    }]
    return render_template('index.html', names=people)

@app.route('/login')
def loginPage():
    return render_template('login.html')