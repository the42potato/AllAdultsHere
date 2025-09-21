from flask import Flask, render_template, send_from_directory, request
import json
import os
import math
from datetime import datetime
from werkzeug.exceptions import HTTPException
from util import validate_json_schema, get_json_file_based_on_date
from errors import JokeError
from renders import render_http_error
from bp_fixed import fixed_bp
from bp_generated import generated_bp


app = Flask(__name__)
app.template_folder = 'templates'
app.register_blueprint(fixed_bp)
app.register_blueprint(generated_bp)
boot_date = datetime.now()

# create global config data on boot
with app.app_context():
    # open and load the json schema
    config_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'config.json')
    config_schema_path = os.path.join(app.static_folder, 'dist', 'src', 'json', 'schema', 'configuration.json')
    with open(config_path) as d, open(config_schema_path) as s:
        config = json.load(d)
        config_schema = json.load(s)
    
    # if config is valid, validate contained data and add variable data
    if validate_json_schema(config, config_schema):
        # inject static information into config
        js_path = os.path.join(app.static_folder, 'dist', 'src', 'js')

        # find all valid JS files and remove invalid IMPORT_JS contents
        valid_js = []
        for file in os.listdir(js_path):
            if file.endswith("js"):
                file_name = os.path.splitext(os.path.basename(file))[0]
                valid_js.append(file_name)
        config["IMPORT_JS"] = list(set(valid_js) & set(config["IMPORT_JS"]))
    else:
        config = None
    app.global_config = config

@app.context_processor
def inject_global_data():
    # If config doesn't exist, raise an exception
    if app.global_config != None:
        # build dynamic global data
        date_diff = datetime.now() - boot_date
        print(date_diff)
        days = math.floor(date_diff.total_seconds() / 86400)
        hours = math.ceil(date_diff.total_seconds() / 3600)
        app.global_data = {
            "RECIPE_OF_THE_DAY": get_json_file_based_on_date("recipes"),
            "LAST_REBOOT": {"days": days, "hours": hours}
        }
        return {**app.global_config, **app.global_data} # merge dictionaries for return
    else:
        raise FileNotFoundError("Invalid Schema")


@app.route('/')
def index():
    return render_template('/sections/general/index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

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