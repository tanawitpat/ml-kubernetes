import os

import yaml

logic_config_local = yaml.load(open("configs/logic.yml"), Loader=yaml.FullLoader)["logic"]

logic_config = {
    "MD_00001": {
        "endpoint": os.getenv("LOGIC_MD_00001_ENDPOINT", logic_config_local["MD_00001"]["endpoint"])
    },
    "MD_00002": {
        "endpoint": os.getenv("LOGIC_MD_00002_ENDPOINT", logic_config_local["MD_00002"]["endpoint"])
    }
}