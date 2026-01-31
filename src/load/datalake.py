import os
import json

import pandas as pd


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


def save_to_silver(filepath: str, data: list[dict] | str) -> None:
    if filepath.endswith('.json'):
        filepath = os.path.join(SILVER_PATH, filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok = True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        df = pd.DataFrame(data)
        filepath = os.path.join(SILVER_PATH, filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok = True)
        df.to_parquet(
            filepath,
            engine = 'pyarrow',
            compression = 'snappy', 
            index = False
        )


def save_metadata_to_silver(filepath: str, metadata: dict) -> None:
    filepath = os.path.join(SILVER_PATH, filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok = True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii = False, indent = 4)


def load_from_silver(filepath: str) -> list[dict]:
    filepath = os.path.join(SILVER_PATH, filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        return json.loads(content)
