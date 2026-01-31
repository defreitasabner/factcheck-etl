import logging

from src.load import meta_ads as load_meta_ads
from src.transform.meta_ads import transform


logger = logging.getLogger(__name__)


def run_meta_ads_to_silver(meta_ads_bronze_tier_data_path: str, meta_ads_bronze_tier_metadata_path: str) -> str:
    logger.info('Starting Meta ads Silver pipeline')
    meta_ads_bronze_tier_data, meta_ads_bronze_tier_metadata = \
        load_meta_ads.load_from_bronze(meta_ads_bronze_tier_data_path, meta_ads_bronze_tier_metadata_path)
    transformed_data, transform_params = transform(meta_ads_bronze_tier_data)
    load_meta_ads.save_to_silver(transformed_data, meta_ads_bronze_tier_metadata, transform_params)
    logger.info('Pipeline completed successfully')
