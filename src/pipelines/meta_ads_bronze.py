import logging

from src.common import webscrape, log
from src.extract import meta_ads
from src.load import meta_ads as load_meta_ads


logger = logging.getLogger(__name__)


def run_meta_ads_to_bronze(query: str, ad_type: str, limit: int = None):
    logger.info('Starting Meta ads Bronze pipeline')
    driver = webscrape.get_webdriver(show_browser = False)
    raw_ads, scrape_params = meta_ads.scrape_ads(driver, query, ad_type, limit)
    load_meta_ads.save_to_bronze(raw_ads, scrape_params)
    logger.info('Pipeline completed successfully')
