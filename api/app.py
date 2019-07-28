import os
from flask import Flask, request, json, Response

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    response = Response("pong",
        status=200,
        mimetype="application/json"
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app.run(debug=True)