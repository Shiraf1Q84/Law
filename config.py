import json
import os

CONFIG_FILE = 'config.json'

def save_api_key(api_key: str):
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    config['api_key'] = api_key
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('api_key', '')
    return ''

def clear_api_key():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)