import logging

from src.extract.lupa import extract
from src.load.lupa import save_to_bronze


logger = logging.getLogger(__name__)


def bronze(
    query: str = None,
    page: int = 1, 
    order: str = 'DESC', 
    category: str = 'Verificação',
    limit: int = None
):
    raw_news, scrape_params = extract(query, page, order, category, limit)
    data_filepath, metadata_filepath = save_to_bronze(raw_news, scrape_params)
    return data_filepath, metadata_filepath


def silver(bronze_data_filepath: str, bronze_metadata_filepath: str):
    pass