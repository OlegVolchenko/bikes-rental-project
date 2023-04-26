import re
import time

from bs4 import BeautifulSoup
from prefect import flow, task
from selenium import webdriver


@task(name='Get urls')
def get_urls() -> list:
    """
    Gets usage statistics data from the 'https://cycling.data.tfl.gov.uk/'
    Source
    :return: List of urls
    """
    # The page generates urls using javascript so in order to get them after generation we need to use webdriver
    driver = webdriver.Chrome(executable_path='/driver/chromedriver')
    driver.get('https://cycling.data.tfl.gov.uk/')
    # wait sometime so page can generate the urls otherwise it can return incomplete list of links
    time.sleep(15)
    # Parse a payload
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls = []
    for url in soup.find_all('a'):
        if re.search(r'usage-stats/.+.csv', url.get('href')):
            urls.append(url.get('href'))
    return urls


@flow(name='Save urls', log_prints=True)
def save_urls() -> None:
    """
    Saves urls from web page to local txt file
    :return: None
    """

    urls = get_urls()
    # create schema object that contains date period and information about columns and dtypes

    with open('workflows/flows/extract_pipeline/load_urls.txt', 'w') as f:
        for url in urls:
            f.write("%s\n" % url)


if __name__ == '__main__':
    save_urls()
