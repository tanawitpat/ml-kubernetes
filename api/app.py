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

@app.route("/get_logic_output", methods=["GET"])
def get_logic_output():
    logic_endpoint_request = json.dumps({
        "data": [
            {
                "embarked": "S", 
                "fare": 15.0, 
                "p_class": "2", 
                "parch": 0, 
                "passenger_id": "A00001", 
                "sex": "male", 
                "sib_sp": 0
            },{
                "embarked": "S", 
                "fare": 30.0, 
                "p_class": "1", 
                "parch": 1, 
                "passenger_id": "A00002", 
                "sex": "female", 
                "sib_sp": 2
            }
        ], 
        "logic_id": "MD_00001", 
        "request_id": "16fd2706-8baf-433b-82eb-8c7fada847da"
    })
    logic_endpoint_response = requests.post(
        url="{}/submit_data".format("http://localhost:5001"),
        data=logic_endpoint_request,
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