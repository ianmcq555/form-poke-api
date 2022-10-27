from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app.models  import Pokemon, Pokedex
from .forms import CreatePostForm
import requests, json

pokedex = Blueprint('pokedex', __name__, template_folder='pokedex_templates')

@pokedex.route('/pokedex/add', methods=["GET", "POST"])
@login_required
def searchPokemon():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data

            
 
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            requests.get(url)
            response = requests.get(url)
            if response.ok:
                pokemon_dict = {}
                data =  response.json()
                pokemon_dict[name.title()] = {
                    'Image' : data["sprites"]["front_default"],
                    'Ability' : data["abilities"][0]["ability"]["name"],
                    'Base_Exp' : data["base_experience"],
                    'HP' : data["stats"][0]["base_stat"],
                    'Attack' : data["stats"][1]["base_stat"],
                    'Defense' : data["stats"][2]["base_stat"],
                    'Speed' : data["stats"][5]["base_stat"]
            }

                img_url = pokemon_dict[name.title()]['Image']
                base_exp = pokemon_dict[name.title()]['Base_Exp']
                hp = pokemon_dict[name.title()]['HP']
                attack = pokemon_dict[name.title()]['Attack']
                defense = pokemon_dict[name.title()]['Defense']
                speed = pokemon_dict[name.title()]['Speed']
                ability = pokemon_dict[name.title()]['Ability']
            else:
                flash('That pokemon does not exist', 'danger')
                return redirect(url_for('pokedex.searchPokemon'))
            
            u1 = Pokemon.query.filter_by(name=name).first()
            if u1:
                flash('Pokemon already exists in Pokedex', 'danger')
            else:
                flash(f'Succesfully added {name} to Pokedex!', 'success')
                pokemon = Pokemon(name, ability, img_url, base_exp, hp, attack, defense, speed, current_user.id)
                pokemon.saveToDB()
                

    return render_template('search.html', form=form)

@pokedex.route('/pokedex')
def viewPokemon():
    pokemons = Pokemon.query.order_by(Pokemon.name).all()[::-1]
    return render_template('pokedex.html', pokemons=pokemons)

@pokedex.route('/add_to_team/<int:pokemon_id>')
@login_required
def addTeam(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        # print(current_user.pokemon_team.count())
        if current_user.my_team.count() == 5:
            flash('team full')
        else:
            current_user.addToTeam(pokemon)
            flash(f'Successfully added {pokemon.name} to {current_user.username}\'s team', 'success')
    else:
        flash(f'Cannot add pokemon that does not exist...', 'danger')
    return redirect(url_for('homePage'))

@pokedex.route('/remove_from_team/<int:pokemon_id>')
@login_required
def removeTeam(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        p = Pokedex.query.filter_by(pokemon_id=pokemon.id).first()
        current_user.removeFromTeam(p)
        flash(f'Successfully removed {pokemon.name} from {current_user.username}\'s team', 'success')
    else:
        flash(f'Cannot remove pokemon that does not exist...', 'danger')

    return redirect(url_for('homePage'))