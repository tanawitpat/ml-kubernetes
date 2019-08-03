import os

import requests
import yaml

from flask import Flask, request, json, Response

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

app = Flask(__name__)

logic_config = yaml.load(open("configs/logic.yml"), Loader=yaml.FullLoader)

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
    api_request = request.json
    if api_request["logic_id"] not in logic_config:
        response = Response({},
            status=400,
            mimetype="application/json"
        )
        return response
    logic_endpoint_path = logic_config[api_request["logic_id"]]["endpoint"]

    logic_endpoint_request = request.json
    logic_endpoint_response = requests.post(
        url="{}/submit_data".format(logic_endpoint_path),
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