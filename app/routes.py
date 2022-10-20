from app import app
from flask import render_template

@app.route('/')
def homePage():
    trainers = [{
        'name': 'Ian',
        'pokemon': 'Blastoise'
    },{
        'name': 'Sia',
        'pokemon': 'Charizard'
    },{
        'name': 'Ash',
        'pokemon': 'Pikachu'
    }]
    return render_template('index.html', names=trainers)

@app.route('/login')
def loginPage():
    return render_template('login.html')