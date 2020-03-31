from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route('/', methods=['POST', 'GET'])
def health():
    return jsonify(text="Healthy")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
