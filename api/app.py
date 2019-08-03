import os
import requests

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

@app.route("/logic", methods=["POST"])
def endpoint_logic():
    logic_endpoint_request = request.json
    logic_endpoint_response = requests.post(
        url="{}/submit_data".format("http://localhost:5001"),
        data=json.dumps(logic_endpoint_request),
        headers={"content-type": "application/json"},
        verify=False,
        timeout=10
    )
    logic_endpoint_response = json.loads(logic_endpoint_response.content.decode("utf-8"))
    response = Response(json.dumps(logic_endpoint_response),
        status=200,
        mimetype="application/json"
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT)