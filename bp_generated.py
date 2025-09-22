from flask import Blueprint, render_template, current_app, request, abort
import os
import glob
import json
from util import validate_json_schema
from errors import raise_joke_http_error
from renders import render_validated_json_template, render_recipe_page, render_human_validator

generated_bp = Blueprint("generated_bp", __name__)

@generated_bp.record_once
def on_load(setup_state):
    app = setup_state.app
    recipes_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'recipes.json')
    cardlist_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'cardlist.json')
    souls_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'souls.json')
    with open(recipes_schema_path) as r, open(cardlist_schema_path) as c, open(souls_schema_path) as s:
            generated_bp.recipe_schema = json.load(r)
            generated_bp.cardlist_schema = json.load(c)
            generated_bp.souls_schema = json.load(s)

@generated_bp.route('/recipes')
def recipes():
    recipes_folder_path = os.path.join(current_app.static_folder, 'dist', 'src', 'json', 'recipes')

    # get query from request, otherwise it is ""
    search_query = request.args.get("query", "").lower()
    selected_meals = request.args.getlist("meal")

    recipes_data = []
    invalid_file_cnt = 0
    recipe_files = glob.glob(os.path.join(recipes_folder_path, '*.json')) # get full paths to all JSON files in the recipes folder
    for recipe_file in recipe_files:
        recipe_link = os.path.splitext(os.path.basename(recipe_file))[0] # link used within site
        with open(recipe_file) as f:
            recipe = json.load(f)
            if validate_json_schema(recipe, generated_bp.recipe_schema): # if recipe matches schema, build data for use on page
                title = recipe.get("title", "").lower()
                recipe_meals = recipe.get("meal_type", [])
                if isinstance(recipe_meals, str):
                    recipe_meals = [recipe_meals.lower()]
                else:
                    recipe_meals = [m.lower() for m in recipe_meals]

                title_match = search_query in title if search_query else True
                meals_match = all(meal in recipe_meals for meal in selected_meals) if selected_meals else True

                if title_match and meals_match:
                    recipes_data.append(
                        {"link": f"recipes/{recipe_link}", "data": recipe}
                        )
            else:
                invalid_file_cnt += 1
                print(f"❌ {f}: Invalid file schema")

    return render_template('/sections/recipes/browse.html', recipes=recipes_data, invalid_count=invalid_file_cnt)

@generated_bp.route('/recipe_substitutions')
def recipe_substitutions():
    substitutions_file = os.path.join(current_app.static_folder, 'dist', 'src', 'json', 'static', "recipe_substitutions.json")
    return render_validated_json_template('/sections/general/index_card_list.html', substitutions_file, generated_bp.cardlist_schema)

@generated_bp.route('/recipes/<path:recipe_name>')
def recipe_detail(recipe_name):
    return render_recipe_page(recipe_name, generated_bp.recipe_schema)

@generated_bp.route('/recipes/review/<path:recipe_name>')
def recipe_review(recipe_name):
    return render_recipe_page(recipe_name, generated_bp.recipe_schema, True)

@generated_bp.route('/recipes/submitreview/<path:recipe_name>')
def submit_recipe_review(recipe_name):
    return raise_joke_http_error("advice_ignored", current_app.global_config["ERRORS"]["custom_codes"]["advice_ignored"]["description"])

@generated_bp.route('/sex_positions')
def sex_positions():
    sex_positions_file = os.path.join(current_app.static_folder, 'dist', 'src', 'json', 'static', 'sex_positions.json')

    cookie = request.cookies.get('sex_pos_validator')
    print(f"COOKIE : {cookie}")
    if cookie == "T":
        return render_validated_json_template('/sections/general/index_card_list.html', sex_positions_file, generated_bp.cardlist_schema)
    else:
        return render_human_validator('sex_pos_validator', request.path)
    
@generated_bp.route('/souls')
def souls_help_list():
    abort(503, "This section is currently under development. Please check back later.")

@generated_bp.route('/souls/<string:game_name>')
def souls_help(game_name):
    souls_file = os.path.join(current_app.static_folder, 'dist', 'src', 'json', 'souls', game_name + ".json")

    if not os.path.exists(souls_file):
        abort(404, current_app.global_config["ERRORS"]["messages"]["page_data_not_found"])
    
    with open(souls_file, 'r') as file:
        game_help = json.load(file)

    if game_help:
        return render_validated_json_template('/sections/souls/view.html', game_help, generated_bp.souls_schema)
    else:
        abort(404, current_app.global_config["ERRORS"]["messages"]["page_data_not_found"])