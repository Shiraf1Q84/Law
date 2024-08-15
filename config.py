#config.py

import json
import os

CONFIG_FILE = 'config.json'

def save_api_keys(openai_api_key: str, llama_cloud_api_key: str):
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    config['openai_api_key'] = openai_api_key
    config['llama_cloud_api_key'] = llama_cloud_api_key
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_api_keys():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('openai_api_key', ''), config.get('llama_cloud_api_key', '')
    return '', ''

def clear_api_keys():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
