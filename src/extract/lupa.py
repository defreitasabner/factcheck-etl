import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from src.common.webscrape import get_webdriver


logger = logging.getLogger(__name__)

BASE_URL = 'https://www.agencialupa.org'
LUPA_MAPA_CATEGORIAS = {
    'todas': 0,
    'Verificação': 142
}
LUPA_RESULTADOS_POR_PAGINA = 10
WEBDRIVER_WAIT_TIMEOUT = 30
WEBDRIVER_WAIT_MORE_SEARCH_RESULTS_TIMEOUT = 5
XPATHS = {
    'search_result__content': '//div[contains(@class, "archive-list-feed")]',
    'search_result__content__articles': './/article',
    'search_result__content__articles__url': './/a',
    'news__header': '//section[contains(@class, "single-header")]',
    'news__header__category': './/p[contains(@class, "post-hat-content")]',
    'news__header__title': './/h1[contains(@class, "single-head-title")]',
    'news__header__description': './/h2[contains(@class, "single-head-description")]',
    'news__header__authors': './/div[contains(@class, "addon-authors")]',
    'news__header__timestamp': './/time[contains(@class, "single-datetime")]',
    'news__content': '//article[@id="content"]//p'
}


def _get_url(
    query: str, 
    page: int, 
    order: str, 
    category: str
) -> str:
    category_id = LUPA_MAPA_CATEGORIAS.get(category, 0)
    page_param = f'page/{page}/' if page > 1 else ''
    return f'{BASE_URL}/{page_param}?s={query}&order={order}&cat-list={category_id}'


def _scrape_search_results(
    driver: webdriver.Chrome, 
    query: str,
    start_page: int, 
    order: str, 
    category: str,
    limit: int
) -> list[dict]:
    try:
        logger.info('Starting to scrape search results for query "%s", category "%s", order "%s", starting from page %d', query, category, order, start_page)
        current_page = start_page
        search_result_urls = []
        has_results = True
        while has_results:
            url = _get_url(
                query = query, 
                page = current_page, 
                order = order, 
                category = category
            )
            logger.info('Scraping URL: %s', url)
            driver.get(url)
            try:
                WebDriverWait(driver, WEBDRIVER_WAIT_MORE_SEARCH_RESULTS_TIMEOUT)\
                    .until(lambda d: d.find_element(By.XPATH, XPATHS['search_result__content']))
            except Exception:
                logger.warning('No search results found for URL: %s', url)
                has_results = False
                continue
            search_result = driver.find_element(By.XPATH, XPATHS['search_result__content'])
            results = search_result.find_elements(By.XPATH, XPATHS['search_result__content__articles'])
            urls = [
                result.find_element(By.XPATH, XPATHS['search_result__content__articles__url']).get_attribute('href') 
                    for result in results
            ]
            logger.info('Found %d search results on page %d', len(urls), current_page)
            search_result_urls.extend(urls)
            if limit and len(search_result_urls) >= limit:
                logger.info('Reached the limit of %d search results. Stopping.', limit)
                search_result_urls = search_result_urls[:limit]
                has_results = False
            elif len(results) < LUPA_RESULTADOS_POR_PAGINA:
                logger.info('Less than %d results found on page %d. Assuming this is the last page.', LUPA_RESULTADOS_POR_PAGINA, current_page)
                has_results = False
            else:
                current_page += 1
        return search_result_urls
    except Exception as e:
        logger.error('Error while scraping Lupa: %s', e)
        raise e


def _scrape_news(driver: webdriver.Chrome, search_result_urls: list[str]) -> list[dict]:
    logger.info('Starting to scrape news content from %d URLs', len(search_result_urls))
    news = []
    for url in search_result_urls:
        try:
            driver.get(url)
            WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT)\
                .until(lambda d: d.find_element(By.XPATH, XPATHS['news__header']))
            header = driver.find_element(By.XPATH, XPATHS['news__header'])
            category = header.find_element(By.XPATH, XPATHS['news__header__category']).text
            title = header.find_element(By.XPATH, XPATHS['news__header__title']).text
            description = header.find_element(By.XPATH, XPATHS['news__header__description']).text
            authors = header.find_element(By.XPATH, XPATHS['news__header__authors']).text
            timestamp = header.find_element(By.XPATH, XPATHS['news__header__timestamp']).get_attribute('datetime')
            content = driver.find_elements(By.XPATH, XPATHS['news__content'])
            news_content = "\n".join([c.text for c in content])
            raw_new = {
                'title': title,
                'category': category,
                'description': description,
                'authors': authors,
                'timestamp': timestamp,
                'url': url,
                'content': news_content,
                'raw_html': driver.find_element(By.XPATH, '//main').get_attribute('innerHTML'),
                'scraped_at': datetime.now().isoformat()
            }
            news.append(raw_new)
            logger.info('Scraped news content from %s', url)
        except Exception as e:
            logger.error('Error while scraping news content from %s: %s', url, e)
    return news


def extract(
    query: str,
    page: int, 
    order: str, 
    category: str,
    limit: int
) -> tuple[list[dict], dict]:
    try:
        driver = get_webdriver()
        scrape_params = {
            'query': query,
            'start_page': page,
            'order': order,
            'category': {
                'id': LUPA_MAPA_CATEGORIAS.get(category, 0),
                'name': category
            },
            'xpaths': XPATHS,
            'limit': limit,
            'webdriver_wait_timeout': WEBDRIVER_WAIT_TIMEOUT,
            'webdriver_wait_more_search_results_timeout': WEBDRIVER_WAIT_MORE_SEARCH_RESULTS_TIMEOUT
        }
        search_results = _scrape_search_results(
            driver = driver, 
            query = query, 
            start_page = page, 
            order = order, 
            category = category,
            limit = limit
        )
        raw_news = _scrape_news(driver, search_results)
        return raw_news, scrape_params
    except Exception as e:
        logger.error('Error while scraping Lupa news: %s', e)
    finally:
        driver.quit()
