#!/usr/bin/python3
"""Flask app"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={"/": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def handle_error_page(error):
    """JSONify not found error page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
