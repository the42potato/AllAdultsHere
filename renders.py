from jsonschema import validate, ValidationError
from flask import render_template, abort, current_app
import json
import os

def render_validated_json_template(template_path, data, schema):
    try:
        if isinstance(data, (str, os.PathLike)):
            with open(data, 'r', encoding='utf-8') as f:
                parsed_data = json.load(f)
        else:
            parsed_data = data
        
        validate(instance=parsed_data, schema=schema)
        return render_template(template_path, data=parsed_data)
    except ValidationError as e:
        print(e)
        abort(500, current_app.global_config["ERRORS"]["messages"]["invalid_json_schema"])