from flask import Flask, render_template, send_from_directory, request, abort
import json
import os
import glob
import random
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException
from util import validate_json_schema, get_json_file_based_on_date
from errors import raise_joke_http_error, JokeError
from renders import render_validated_json_template, render_http_error, render_recipe_page


app = Flask(__name__)
app.template_folder = 'templates'
boot_date = datetime.now(timezone.utc)

# create global config data on boot
with app.app_context():
    config_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'config.json')
    config_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'configuration.json')
    with open(config_path) as d, open(config_schema_path) as s:
        config = json.load(d)
        config_schema = json.load(s)
    if validate_json_schema(config, config_schema):
        # inject generated information into config
        config["RECIPE_OF_THE_DAY"] = get_json_file_based_on_date("recipes")
        config["LAST_REBOOT"] = boot_date
        js_path = os.path.join(app.static_folder, 'dist', 'src', 'js')

        # find all valid JS files and remove invalid IMPORT_JS contents
        valid_js = []
        for file in os.listdir(js_path):
            if file.endswith("js"):
                file_name = os.path.splitext(os.path.basename(file))[0]
                valid_js.append(file_name)
        config["IMPORT_JS"] = set(valid_js) & set(config["IMPORT_JS"])
    else:
        config = None
    app.global_config = config

@app.context_processor
def inject_global_data():
    if app.global_config != None:
        return app.global_config
    else:
        raise FileNotFoundError("Invalid Schema")

recipes_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'recipes.json')
cardlist_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'cardlist.json')
with open(recipes_schema_path) as r, open(cardlist_schema_path) as c:
        recipe_schema = json.load(r)
        cardlist_schema = json.load(c)

@app.route('/')
def index():
    return render_template('/sections/general/index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/recipes')
def recipes():
    recipes_folder_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'recipes')

    search_query = request.args.get("query", "").lower()
    selected_meals = request.args.getlist("meal")

    recipes_data = []
    invalid_file_cnt = 0
    recipe_files = glob.glob(os.path.join(recipes_folder_path, '*.json'))
    for recipe_file in recipe_files:
        recipe_link = os.path.splitext(os.path.basename(recipe_file))[0]
        with open(recipe_file) as f:
            recipe = json.load(f)
            if validate_json_schema(recipe, recipe_schema):
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

@app.route('/recipe_substitutions')
def recipe_substitutions():
    substitutions_file = os.path.join(app.static_folder, 'dist', 'src', 'json', 'static', "recipe_substitutions.json")
    return render_validated_json_template('/sections/general/index_card_list.html', substitutions_file, cardlist_schema)

@app.route('/recipes/<path:recipe_name>')
def recipe_detail(recipe_name):
    return render_recipe_page(recipe_name, recipe_schema)

@app.route('/recipes/review/<path:recipe_name>')
def recipe_review(recipe_name):
    return render_recipe_page(recipe_name, recipe_schema, True)

@app.route('/recipes/submitreview/<path:recipe_name>')
def submit_recipe_review(recipe_name):
    return raise_joke_http_error("advice_ignored", app.global_config["ERRORS"]["custom_codes"]["advice_ignored"]["description"])

@app.route('/sex_positions')
def sex_positions():
    sex_positions_file = os.path.join(app.static_folder, 'dist', 'src', 'json', 'static', 'sex_positions.json')
    return render_validated_json_template('/sections/general/index_card_list.html', sex_positions_file, cardlist_schema)

@app.errorhandler(JokeError)
def handle_joke_error(e):
    print(418)
    return render_http_error(e, True)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    print("def")
    return render_http_error(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1212, debug=True)