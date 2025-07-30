from flask import Flask, render_template, send_from_directory, request, redirect
import json
import os
import glob
from jsonschema import validate, ValidationError
from util import validate_json_schema, render_validated_json_template


app = Flask(__name__)
app.template_folder = 'templates'

@app.context_processor
def inject_global_data():
    config_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'config.json')
    config_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'configuration.json')
    with open(config_path) as d, open(config_schema_path) as s:
        config = json.load(d)
        config_schema = json.load(s)
    if validate_json_schema(config, config_schema):
        return config
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
                print(f"❌ {f}: Invalid file schema")

    return render_template('/sections/recipes/browse.html', recipes=recipes_data)

@app.route('/recipe_substitutions')
def recipe_substitutions():
    substitutions_file = os.path.join(app.static_folder, 'dist', 'src', 'json', 'static', "recipe_substitutions.json")
    return render_validated_json_template('/sections/general/index_card_list.html', substitutions_file, cardlist_schema)

@app.route('/recipes/<path:recipe_name>')
def recipe_detail(recipe_name):
    recipes_folder_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'recipes', recipe_name + '.json')
    print(recipes_folder_path)

    if not os.path.exists(recipes_folder_path):
        return "Recipe not found", 404
    
    with open(recipes_folder_path, 'r') as file:
        recipe = json.load(file)
    
    if recipe:
        return render_validated_json_template('/sections/recipes/view.html', recipe, recipe_schema)
    else:
        return "Recipe not found", 404

@app.route('/sex_positions')
def sex_positions():
    sex_positions_file = os.path.join(app.static_folder, 'dist', 'src', 'json', 'static', 'sex_positions.json')
    return render_validated_json_template('/sections/general/index_card_list.html', sex_positions_file, cardlist_schema)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1212, debug=True)