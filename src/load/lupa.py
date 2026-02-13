
import logging
import os
import json
from datetime import datetime

from src.load import datalake


logger = logging.getLogger(__name__)

SOURCE_NAME = 'lupa'
LUPA_SUBFOLDER = f'source={SOURCE_NAME}'


def save_to_bronze(raw_news: list[dict], scrape_params: dict) -> tuple[str, str]:
    now = datetime.now()
    category_subfolder = f'category_id={scrape_params["category"]["id"]}'
    query_subfolder = f'query={scrape_params["query"]}'
    subfolder_dir = os.path.join(LUPA_SUBFOLDER, category_subfolder, query_subfolder)

    data_filename = f'data_{scrape_params["query"]}_{now.strftime("%Y%m%d_%H%M%S")}.json'
    data_filepath = os.path.join(subfolder_dir, data_filename)
    data_content = json.dumps(raw_news, ensure_ascii = False, indent = 4)
    datalake.save_to_bronze(data_filepath, data_content)
    logger.info('Saved raw Lupa news to bronze layer at: %s', data_filepath)
    
    metadata = {
        'extracted_at': now.isoformat(),
        'extract_params': scrape_params,
        'record_count': len(raw_news),
        'filepath': data_filepath
    }
    metadata_filename = f'metadata_{scrape_params["query"]}_{now.strftime("%Y%m%d_%H%M%S")}.json'
    metadata_filepath = os.path.join(subfolder_dir, metadata_filename)
    metadata_content = json.dumps(metadata, ensure_ascii = False, indent = 4)
    datalake.save_to_bronze(metadata_filepath, metadata_content)
    logger.info('Saved metadata to bronze layer at: %s', metadata_filepath)

    return data_filepath, metadata_filepath

