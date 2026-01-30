import os
import json


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(ROOT_PATH, 'data')
BRONZE_PATH = os.path.join(DATA_PATH, 'bronze')
SILVER_PATH = os.path.join(DATA_PATH, 'silver')
GOLD_PATH = os.path.join(DATA_PATH, 'gold')


def save_to_bronze(filepath: str, content: str) -> None:
    filepath = os.path.join(BRONZE_PATH, filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok = True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def load_from_bronze(filepath: str) -> list[dict]:
    filepath = os.path.join(BRONZE_PATH, filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        return json.loads(content)
