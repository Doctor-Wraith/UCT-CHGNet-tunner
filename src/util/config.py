import json
import os.path

DEFUALT = {
    "chgnet": {
        "epoch": 50,
        "learn": "1e-4"
    },
    "ratio": [
        80,
        20
    ]
}
path = "./config.json"
if os.path.isfile(path):
    with open(path, "r") as file:
        configuration = json.load(file)
else:
    with open(path, "w") as file:
        configuration = json.loads(str(DEFUALT).replace("'", '"'))
        json.dump(configuration, file)
