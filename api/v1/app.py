#!/usr/bin/python3
"""Flask app"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={"/": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def handle_error_page(error):
    """JSONify not found error page"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'Task Management Restful API',
    'version': 1
}

Swagger(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
