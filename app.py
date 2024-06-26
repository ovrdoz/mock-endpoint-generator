from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
import re

app = Flask(__name__)
CORS(app)

DATA_DIR = './data'

def convert_route_to_flask(route):
    return re.sub(r'\{([^}]+)\}', r'<\1>', route)

def load_routes():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.mok'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                parts = first_line[2:].split()
                route = parts[0]
                http_method = parts[1] if len(parts) > 1 else 'GET'
                status_code = int(parts[2]) if len(parts) > 2 else 200

                # Convert route variables from {var} to <var>
                flask_route = convert_route_to_flask(route)

                content = json.load(file)
                register_route(flask_route, http_method, content, status_code)

def register_route(route, method, content, status_code):
    def route_view_function(**kwargs):
        return jsonify(content), status_code
    endpoint = f"{route.replace('/', '_')}_{method.lower()}"
    app.add_url_rule(route, endpoint, route_view_function, methods=[method])

if __name__ == '__main__':
    load_routes()
    
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, port=port, use_reloader=False)

