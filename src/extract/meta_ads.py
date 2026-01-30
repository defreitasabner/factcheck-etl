import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.utils import text_helpers


logger = logging.getLogger(__name__)

WEBDRIVER_WAIT_TIMEOUT = 30
XPATH_RESULT_LENGTH = '//div[@role="heading"][@aria-level="3"]'
XPATH_GRID_ELEMENTS = '//*[hr]'
MAX_NO_NEW_ADS_ATTEMPTS = 3
WAIT_NEW_ADS_TIMEOUT = 5


def get_url(query: str, ad_type: str) -> str:
    return f'https://pt-br.facebook.com/ads/library/?active_status=active&ad_type={ad_type}&content_languages[0]=pt&country=BR&is_targeted_country=false&media_type=all&publisher_platforms[0]=instagram&publisher_platforms[1]=threads&publisher_platforms[2]=whatsapp&publisher_platforms[3]=facebook&publisher_platforms[4]=messenger&q={query}&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions&start_date[min]&start_date[max]'

def scrape_ads(driver: webdriver.Chrome, query: str, ad_type: str, limit: int = None) -> tuple[list[dict], dict]:
    try:
        url = get_url(query, ad_type)
        logger.info('Scraping URL: %s', url)
        driver.get(url)
        wait = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT)
        div = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_RESULT_LENGTH)))
        result_length = text_helpers.extract_int_from_text(div.text)
        logger.info('The search found about %d results', result_length)
        if limit:
            logger.info('Limit set to %d ads', limit)
        else:
            logger.info('No limit set. Will attempt to scrape all %d ads', result_length)
        scrape_params = {
            'url': url,
            'query': query,
            'ad_type': ad_type,
            'xpath_result_length': XPATH_RESULT_LENGTH,
            'xpath_grid_elements': XPATH_GRID_ELEMENTS,
            'webdriver_wait_timeout': WEBDRIVER_WAIT_TIMEOUT,
            'max_no_new_ads_attempts': MAX_NO_NEW_ADS_ATTEMPTS,
            'wait_new_ads_timeout': WAIT_NEW_ADS_TIMEOUT,
        }
        raw_ads = []
        processed_results_count = 0
        no_new_ads_attempts = 0
        while True:
            ads_divs = driver.find_elements(By.XPATH, XPATH_GRID_ELEMENTS)
            current_ads_divs_count = len(ads_divs)

            new_ads_found = False
            for i in range(processed_results_count, current_ads_divs_count):
                try:
                    raw_ad = {
                        'raw_text': ads_divs[i].text,
                        'raw_html': ads_divs[i].get_attribute('innerHTML'),
                        'scraped_at': datetime.now().isoformat()
                    }
                    raw_ads.append(raw_ad)
                    new_ads_found = True
                    if limit and len(raw_ads) >= limit:
                        break
                except Exception as e:
                    logger.error("Failed to extract data from one ad div: %s", e)
                finally:
                    processed_results_count += 1
            if limit:
                logger.info('Processed %d from %d ads (limit)', processed_results_count, limit)
            else:
                logger.info('Processed %d from %d ads', processed_results_count, result_length)
            
            # Check if we reached the limit
            if limit and processed_results_count >= limit:
                logger.info('Reached the limit of %d ads. Stopping.', limit)
                break
            
            # Check the number of attempts with no new ads found
            if not new_ads_found:
                no_new_ads_attempts += 1
                logger.info('No new ads found. Attempt %d/%d', no_new_ads_attempts, MAX_NO_NEW_ADS_ATTEMPTS)
                if no_new_ads_attempts >= MAX_NO_NEW_ADS_ATTEMPTS:
                    logger.info('No new ads found after %d attempts. Stopping.', MAX_NO_NEW_ADS_ATTEMPTS)
                    break
            else:
                no_new_ads_attempts = 0
            
            # Scroll down to load more ads
            logger.info('Scrolling to load more ads...')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new ads to load
            try:
                WebDriverWait(driver, WAIT_NEW_ADS_TIMEOUT).until(
                    lambda d: len(d.find_elements(By.XPATH, XPATH_GRID_ELEMENTS)) > current_ads_divs_count
                )
            except:
                pass

        logger.info('Scraping completed. Total ads successfully extracted: %d', len(raw_ads))
        return raw_ads, scrape_params
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        driver.quit()
