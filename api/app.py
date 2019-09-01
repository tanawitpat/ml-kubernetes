import os

import requests
from flask import Flask, request, json, Response

from config import logic_config
from utils import calculate_score, is_request_valid

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

app = Flask(__name__)

print("Logic config: {}".format(logic_config))

@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint"""
    response = Response("pong",
        status=200,
        mimetype="application/json"
    )
    return response

@app.route("/logic", methods=["POST"])
def endpoint_logic():
    """Validate API request, submit the data to logic API, and return probability of survival.
    Request:
        {
            "request_id": "16fd2706-8baf-433b-82eb-8c7fada847da",
            "logic_id": "MD_00001",
            "data": [
                {
                    "passenger_id": "A00001",
                    "sex": "male",
                    "sib_sp": 0,
                    "parch": 0,
                    "fare": 15.0,
                    "embarked": "S",
                    "p_class": "2"
                },{
                    "passenger_id": "A00002",
                    "sex": "female",
                    "sib_sp": 2,
                    "parch": 1,
                    "fare": 30.0,
                    "embarked": "S",
                    "p_class": "1"
                }
            ] 
        }

    Response:
        {
            "request_id": "16fd2706-8baf-433b-82eb-8c7fada847da",
            "logic_id": "MD_00001",
            "prediction": [
                {
                    "passenger_id": "A00001",
                    "score": 0.9132
                },{
                    "passenger_id": "A00002",
                    "score": 0.1251
                }
            ],
            "timestamp": "2010-04-20T20:08:21.634121"
        }
    """

    api_request = request.json
    if not is_request_valid(api_request):
        response = Response({},
            status=400,
            mimetype="application/json"
        )
        return response

    calculate_score_response = calculate_score(
        path=logic_config[api_request["logic_id"]]["endpoint"], 
        data=request.json
    )

    response = Response(json.dumps(calculate_score_response),
        status=200,
        mimetype="application/json"
    )
    return response

if __name__ == "__main__":
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT)