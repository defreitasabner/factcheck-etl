import os
import json
from datetime import datetime
import logging

from src.load import datalake


logger = logging.getLogger(__name__)

SOURCE_NAME = 'meta_ads'
META_ADS_SUBFOLDER = f'source={SOURCE_NAME}'


def build_filename(query: str, ad_type: str, datetime: datetime) -> str:
    return f'{SOURCE_NAME}_{ad_type}_{query}_{datetime.strftime("%Y%m%d_%H%M%S")}.json'

def save_to_bronze(raw_ads: list, scrape_params: dict) -> None:
    now = datetime.now()
    ad_type_subfolder = f'ad_type={scrape_params["ad_type"]}'
    query_subfolder = f'query={scrape_params["query"]}'
    raw_ads_filename = build_filename(scrape_params["query"], scrape_params["ad_type"], now)
    raw_ads_filepath = os.path.join(META_ADS_SUBFOLDER, ad_type_subfolder, query_subfolder, raw_ads_filename)
    raw_ads_content = json.dumps(raw_ads, ensure_ascii = False, indent = 4)
    datalake.save_to_bronze(raw_ads_filepath, raw_ads_content)
    logger.info('Saved raw ads to bronze layer at: %s', raw_ads_filepath)
    metadata = {
        'scraped_at': now.isoformat(),
        'scrape_params': scrape_params,
        'record_count': len(raw_ads),
        'file_info': {
            'filename': raw_ads_filename,
            'filepath': raw_ads_filepath,
            'encoding': 'utf-8',
            'format': 'json',
        }
    }
    metadata_filename = build_filename(scrape_params["query"], scrape_params["ad_type"], now).replace('.json', '_metadata.json')
    metadata_filepath = os.path.join(META_ADS_SUBFOLDER, ad_type_subfolder, query_subfolder, metadata_filename)
    metadata_content = json.dumps(metadata, ensure_ascii = False, indent = 4)
    datalake.save_to_bronze(metadata_filepath, metadata_content)
    logger.info('Saved metadata to bronze layer at: %s', metadata_filepath)

def load_from_bronze(filepath: str) -> list[dict]:
    return datalake.load_from_bronze(filepath)
