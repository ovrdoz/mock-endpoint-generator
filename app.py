from flask import Flask, jsonify, request
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

DATA_DIR = './data'
routes = {}

class ChangeHandler(FileSystemEventHandler):
    """ Handler para mudanças no sistema de arquivos. """
    def on_modified(self, event):
        if event.src_path.endswith('.mok'):
            print(f"Detected change in file: {event.src_path}")
            load_routes()

def load_routes():
    """ Carrega rotas dos arquivos .mok no diretório especificado. """
    global routes
    routes.clear()
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.mok'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                route = file.readline().strip()[2:]
                content = json.load(file)
                routes[route] = content

@app.route('/<path:path>', methods=['GET'])
def dynamic_route(path):
    full_path = f'/{path}'
    if full_path in routes:
        return jsonify(routes[full_path])
    else:
        return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DATA_DIR, recursive=False)
    observer.start()
    
    load_routes()  
    app.run(debug=True, port=port, use_reloader=False)

    observer.stop()
    observer.join()
