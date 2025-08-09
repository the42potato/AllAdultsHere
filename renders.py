from jsonschema import validate, ValidationError
from flask import render_template, abort, current_app
import random
import json
import os

def render_validated_json_template(template_path, data, schema, additional_data=None):
    try:
        if isinstance(data, (str, os.PathLike)):
            with open(data, 'r', encoding='utf-8') as f:
                parsed_data = json.load(f)
        else:
            parsed_data = data
        
        validate(instance=parsed_data, schema=schema)
        return render_template(template_path, data=parsed_data, additional_data=additional_data)
    except ValidationError as e:
        print(e)
        abort(500, current_app.global_config["ERRORS"]["messages"]["invalid_json_schema"])

def render_http_error(err, is_custom = False):
    filter_index = err.description.find('.')
    if filter_index != -1:
        filtered_description = err.description[:filter_index + 1]
    else:
        filtered_description = err.description

    if is_custom:
        error_code = str(err.custom_code)
        error_data = current_app.global_config["ERRORS"]["custom_codes"][error_code]
    else:
        error_code = str(err.code)
        error_data = current_app.global_config["ERRORS"]["codes"][error_code]

    constructed_error = {"code": err.code, "description": filtered_description, "splash": random.choice(error_data["splashes"]), "image": error_data['image']}
    print(constructed_error)
    return render_template("sections/general/error.html", error = constructed_error), err.code

def render_recipe_page(recipe_name, recipe_schema, is_review = False):
    recipes_folder_path = os.path.join(current_app.static_folder, 'dist', 'src', 'json', 'recipes', recipe_name + '.json')

    if not os.path.exists(recipes_folder_path):
        abort(404, current_app.global_config["ERRORS"]["messages"]["recipe_not_found"])
    
    with open(recipes_folder_path, 'r') as file:
        recipe = json.load(file)
    
    if recipe and is_review:
        return render_validated_json_template('/sections/recipes/review.html', recipe, recipe_schema, additional_data={"recipe_name": recipe_name})
    elif recipe:
        return render_validated_json_template('/sections/recipes/view.html', recipe, recipe_schema, additional_data={"recipe_name": recipe_name})
    else:
        abort(404, current_app.global_config["ERRORS"]["messages"]["recipe_not_found"])