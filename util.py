from flask import render_template
import json
import os
from jsonschema import validate, ValidationError


# TODO add JSON schema validation method for use in main.py

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
        return "Invalid Schema", 500

def validate_json_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        return False