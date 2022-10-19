from flask import Blueprint, render_template, request, redirect, url_for
from app.auth.forms import UserCreationForm
from app.models  import User
import requests, json

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/log-me-in')
def logMeIn():
    return render_template('log-me-in.html')

@auth.route('/signup', methods=["GET", "POST"])
def signUp():

    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data

            print(username)
            
            # user = User(username)
            # user.saveToDB()
            
            url = f'https://pokeapi.co/api/v2/pokemon/{username}'
            requests.get(url)
            response = requests.get(url)
            if response.ok:
                pokemon_dict = {}
                name =  response.json()["name"]
                pokemon_dict[name] = {
                    'image' : response.json()["sprites"]["front_shiny"],
                    'abilities' : response.json()["abilities"][0],
                    'base_exp' : response.json()["base_experience"]
                }
            return pokemon_dict

            

        return redirect(url_for('auth.signUp'))

    return render_template('sign_up.html', form=form)

# def get_pokemon_info(pokemon):
#     url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
#     requests.get(url)
#     response = requests.get(url)
#     if response.ok:
#         my_dict = response.json()
#         pokemon_dict = {}
#         name =  response.json()["name"]
#         pokemon_dict[name] = {
#             'image' : response.json()["sprites"]["front_shiny"],
#             'abilities' : response.json()["abilities"][0],
#             'base_exp' : response.json()["base_experience"]
#         }
#     return pokemon_dict