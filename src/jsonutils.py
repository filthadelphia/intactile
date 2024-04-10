import json
from types import SimpleNamespace

def load_config():
    with open('conf.json', 'r') as f:
        return json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def update_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)