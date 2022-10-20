from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from app.models  import Pokemon
from .forms import CreatePostForm

pokedex = Blueprint('pokedex', __name__, template_folder='pokedex_templates')

@pokedex.route('/pokedex/add', methods=["GET", "POST"])
@login_required
def searchPokemon():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data
            ability = form.ability.data
            img_url = form.img_url.data
            base_exp = form.base_exp.data

            pokemon = Pokemon(name, ability, img_url, base_exp, current_user.id)

            pokemon.saveToDB()

            return redirect(url_for('homePage'))

    return render_template('search.html', form=form)

@pokedex.route('/pokedex')
def viewPokemon():
    pokemons = Pokemon.query.order_by(Pokemon.date_created).all()[::-1]
    return render_template('pokedex.html', pokemons=pokemons)