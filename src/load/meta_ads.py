import os
import json
from datetime import datetime
import logging

from src.load import datalake


logger = logging.getLogger(__name__)

SOURCE_NAME = 'meta_ads'
META_ADS_SUBFOLDER = f'source={SOURCE_NAME}'


def build_filename(query: str, ad_type: str, datetime: datetime, format: str = 'json') -> str:
    return f'{SOURCE_NAME}_{ad_type}_{query}_{datetime.strftime("%Y%m%d_%H%M%S")}.{format}'


def save_to_bronze(raw_ads: list, scrape_params: dict) -> tuple[str, str]:
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
    return raw_ads_filepath, metadata_filepath


def load_from_bronze(bronze_tier_data_path: str, bronze_tier_metadata_path: str) -> tuple[list[dict], dict]:
    meta_ads_data = datalake.load_from_bronze(bronze_tier_data_path)
    meta_ads_metadata = datalake.load_from_bronze(bronze_tier_metadata_path)
    logger.info('Loaded %d ads from bronze layer at: %s', len(meta_ads_data), bronze_tier_data_path)
    return meta_ads_data, meta_ads_metadata


def save_to_silver(transformed_data: list[dict], bronze_tier_metadata: dict, transform_params: dict) -> tuple[str, str]:
    now = datetime.now()
    ad_type_subfolder = f'ad_type={bronze_tier_metadata["scrape_params"]["ad_type"]}'
    query_subfolder = f'query={bronze_tier_metadata["scrape_params"]["query"]}'
    transformed_filename = build_filename(
        bronze_tier_metadata["scrape_params"]["query"],
        bronze_tier_metadata["scrape_params"]["ad_type"],
        now,
        format = 'parquet'
    )
    transformed_filepath = os.path.join(META_ADS_SUBFOLDER, ad_type_subfolder, query_subfolder, transformed_filename)
    datalake.save_to_silver(transformed_filepath, transformed_data)
    logger.info('Saved transformed ads to silver layer at: %s', transformed_filepath)
    transform_metadata = {
        'transformed_at': now.isoformat(),
        'record_count': len(transformed_data),
        'file_info': {
            'filename': transformed_filename,
            'filepath': transformed_filepath,
            'encoding': 'utf-8',
            'format': 'parquet',
        },
        'transform_params': transform_params,
        'source_metadata': bronze_tier_metadata
    }
    transform_metadata_filename = transformed_filename.replace('.parquet', '_metadata.json')
    transform_metadata_filepath = os.path.join(META_ADS_SUBFOLDER, ad_type_subfolder, query_subfolder, transform_metadata_filename)
    transform_metadata_content = json.dumps(transform_metadata, ensure_ascii = False, indent = 4)
    datalake.save_to_silver(transform_metadata_filepath, transform_metadata_content)
    logger.info('Saved transform metadata to silver layer at: %s', transform_metadata_filepath)
    return transformed_filepath, transform_metadata_filepath
