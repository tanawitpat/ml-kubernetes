import requests
import json

from config import logic_config

def is_request_valid(request: dict) -> bool:
    """Check if API request is valid"""
    if request["logic_id"] not in logic_config:
        return False
    return True

def calculate_score(path: str, data: dict) -> dict:
    """Calculate probability of survival by submit data to logic endpoint

    Usage::

        >>> from utils import calculate_score
        >>> data = {
        >>>     "request_id": "16fd2706-8baf-433b-82eb-8c7fada847da",
        >>>     "logic_id": "MD_00001",
        >>>     "data": [
        >>>         {
        >>>             "passenger_id": "A00001",
        >>>             "sex": "male",
        >>>             "sib_sp": 0,
        >>>             "parch": 0,
        >>>             "fare": 15.0,
        >>>             "embarked": "S",
        >>>             "p_class": "2"
        >>>         },{
        >>>             "passenger_id": "A00002",
        >>>             "sex": "female",
        >>>             "sib_sp": 2,
        >>>             "parch": 1,
        >>>             "fare": 30.0,
        >>>             "embarked": "S",
        >>>             "p_class": "1"
        >>>         }
        >>>     ] 
        >>> }
        >>> response = calculate_score(
        >>>     path="http://ml-kubernetes-logic-md00001:5000", 
        >>>     data=data
        >>> )

    """

    response = requests.post(
        url="{}/submit_data".format(path),
        data=json.dumps(data),
        headers={"content-type": "application/json"},
        verify=False,
        timeout=10
    )
    response = json.loads(response.content.decode("utf-8"))
    return response