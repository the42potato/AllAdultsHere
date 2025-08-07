from flask import render_template, current_app, abort
import json
import os
import math
from datetime import date, datetime, timedelta
from jsonschema import validate, ValidationError


def validate_json_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        return False

def get_json_file_based_on_date(dir):
    json_path = os.path.join(current_app.static_folder, 'dist', 'src', 'json', dir)
    try:
        items = os.listdir(json_path)
        if items:
            trunc = len(items) + 1
            dte = date.today()
            dt_midnight = datetime.combine(dte, datetime.min.time())
            # need to fix modulo. often results in same number. perhaps moduloing by a large prime will help
            selected_file = items[math.floor(dt_midnight.timestamp() % trunc)] 
            file_path = os.path.join(json_path, selected_file)
            with open(file_path) as f:
                file = json.load(f)
            return {
                "link": selected_file[:-5:],
                "display_text": file["title"]
            }
        else:
            return None
    except Exception as e:
        print(e)
        return None