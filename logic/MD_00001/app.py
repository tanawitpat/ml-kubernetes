import os

from flask import Flask, request, json, Response

import logic

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5001))

app = Flask(__name__)

@app.route("/submit_data", methods=["POST"])
def submit_data():
    """ Request
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
    """
    """ Response
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
    request_input = request.json

    prediction_output = logic.predict(request_input["data"])

    response_struct = json.dumps({
        "request_id": request_input["request_id"],
        "logic_id": request_input["logic_id"],
        "prediction": prediction_output,
        "timestamp": "2010-04-20T20:08:21.634121"
    })
    response = Response(
        response_struct,
        status=200,
        mimetype="application/json"
    )
    return response

if __name__ == "__main__":
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT)