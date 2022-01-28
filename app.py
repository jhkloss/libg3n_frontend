import json

from flask import Flask, render_template, abort, request, jsonify
from logic.home import get_libraries
from logic.config_generator import ConfigGenerator
from libg3n.modules.java.java_library import JavaLibrary
from libg3n.modules.python.python_library import PythonLibrary

app = Flask(__name__)

LIBRARY_BASE_PATH = app.root_path + '/lib/'

MODULES = {
    'java': JavaLibrary,
    'python': PythonLibrary
}

# Get libraries
libraries = get_libraries(LIBRARY_BASE_PATH)

generator = ConfigGenerator()

@app.route('/')
def home():  # put application's code here
    libraries = []
    libraries = get_libraries(LIBRARY_BASE_PATH)
    return render_template('home.html', libraries=libraries.values())


@app.route('/lib/<lib_name>/')
@app.route('/lib/<lib_name>/<path:scope>/')
def library(lib_name: str, scope: str = ''):  # put application's code here

    if lib_name in libraries:
        lib = libraries[lib_name]
        directories, files = lib.get_file_tree(lib.path + '/' + scope)

        return render_template('library_detail.html', library=lib, scope=scope, directories=directories, files=files)
    else:
        abort(404)


@app.route('/lib/<lib_id>/download/')
def download_lib(lib_id: str):
    abort(404)


@app.route('/lib/<lib_id>/generate/')
def generate_lib(lib_id: str):
    if lib_id in libraries:
        lib = libraries[lib_id]
        return render_template('library_generation.html', library=lib)

    abort(404)


@app.route('/lib/<lib_id>/generate/gen/', methods=['POST'])
def generate_lib_execute(lib_id: str):

    if lib_id in libraries:
        lib = libraries[lib_id]
        config_content = generator.parse(lib, request.form)
        return config_content

    abort(404)


@app.route('/property/<fieldset_id>/add/', methods=['POST'])
def add_property(fieldset_id: str):
    name = request.form['property']
    template = render_template('form_elements/property.html', name=name)
    return jsonify({'fieldset_id': fieldset_id, 'template': template})


if __name__ == '__main__':
    app.run()