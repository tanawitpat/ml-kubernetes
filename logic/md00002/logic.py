import random

def predict(input_data):
    prediction_output = []
    for passenger in input_data:
        prediction_output.append(
            {
                "passenger_id": passenger["passenger_id"],
                "score": random.random()
            }
        )
    return prediction_output