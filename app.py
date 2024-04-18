from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
CORS(app)

DATA_DIR = './data'
routes = {}
patterns = {}

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.mok'):
            print(f"Detected change in file: {event.src_path}")
            load_routes()

def convert_route_to_flask(route):
    return re.sub(r'\{([^}]+)\}', r'<\1>', route)

def load_routes():
    global routes, patterns
    routes.clear()
    patterns.clear()
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.mok'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                parts = first_line[2:].split()
                route = parts[0]
                http_method = parts[1] if len(parts) > 1 else 'GET'
                status_code = int(parts[2]) if len(parts) > 2 else 200

                flask_route = convert_route_to_flask(route)
                flask_route_with_method = f"{flask_route} {http_method.upper()}"

                content = json.load(file)
                routes[flask_route_with_method] = (content, http_method.upper(), status_code)

                regex_route = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', flask_route)
                patterns[regex_route] = flask_route  # Only store flask_route here


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def dynamic_route(path):
    full_path = '/' + path
    request_method = request.method
    for pattern, flask_route in patterns.items():
        match = re.match(pattern, full_path)
        if match:
            flask_route_with_method = f"{flask_route} {request_method}"
            if flask_route_with_method in routes:
                content, method, status_code = routes[flask_route_with_method]
                if request.method == method:
                    return jsonify(content), status_code
                else:
                    return jsonify({"error": "Method Not Allowed"}), 405
            return jsonify({"error": "Method Not Allowed"}), 405
    return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DATA_DIR, recursive=False)
    observer.start()

    load_routes()  
    app.run(debug=True, port=port, use_reloader=False)

    observer.stop()
    observer.join()
