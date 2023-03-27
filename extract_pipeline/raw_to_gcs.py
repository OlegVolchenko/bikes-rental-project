import argparse
import os
import re
import time
from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from selenium import webdriver


@task(name='Get urls')
def get_urls(date_from: str, date_to: str) -> list:
    """
    Gets usage statistics data from the 'https://cycling.data.tfl.gov.uk/'
    Source
    :param date_from: str that represents
    :param date_to:
    :return: None
    """
    # The page generates urls using javascript so in order to get them after generation we need to use webdriver
    # TODO: fix this path for Docker
    driver = webdriver.Chrome(executable_path='/Users/oleg.volchenko/Downloads/chromedriver_mac_arm64/chromedriver')
    driver.get('https://cycling.data.tfl.gov.uk/')
    # wait sometime so page can generate the urls otherwise it can return incomplete list of links
    time.sleep(10)
    # Parse a payload
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls = []
    for url in soup.find_all('a'):
        if re.search(r'usage-stats/.+.csv', url.get('href')):
            url = process_url(url.get('href'), date_from, date_to)
            # if url is valid append it to urls list
            if url:
                urls.append(url)
    return urls


def process_url(url: str, date_from: str, date_to: str) -> str:
    """
    Pick valid url for extraction base on data source and extraction date period
    :param url: url string
    :return: valid url for extraction
    """

    def format_to_date(url_period: str):
        """
        Source has multiple date formats in the file names, function converts it to date based on multiple formats
        :param url_period: url string
        :return: date
        """
        if re.search(r'^[0-9]{1,2}[a-zA-Z]{3}[0-9]{4}$', url_period):
            format = "%d%b%Y"
        elif re.search(r'^[0-9]{1,2}[a-zA-Z]{4,9}[0-9]{2}$', url_period):
            format = "%d%B%y"
        elif re.search(r'^[0-9]{1,2}[a-zA-Z]{4,9}[0-9]{4}$', url_period):
            format = "%d%B%Y"
        else:
            format = "%d%b%y"

        return datetime.strptime(url_period, format).date()

    if re.search(r'usage-stats/.+.csv', url):
        # ideally it should return two values but in some cases there might be a typo in period name
        # so it makes it impossible to convert to datetime, the only solutuon for now is to load using any period
        url_periods = re.findall(r'[0-9]{1,2}[a-zA-Z]{3,9}[0-9]{2,4}', url)
        print(url, url_periods)
        url_periods = [format_to_date(period) for period in url_periods]
        if (datetime.strptime(date_from, "%Y-%m-%d").date() <= url_periods[0]) \
                and (datetime.strptime(date_to, "%Y-%m-%d").date() >= url_periods[0]):
            print('url is selected for extract')
            return url


def read_file(url: str) -> pd.DataFrame:
    """
    Source server rejects requests with default oython header, function uses different header in order to get a file
    :param url:
    :return:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    data = requests.get(url, headers=headers).text
    df = pd.read_csv(StringIO(data))
    try:
        df['EndStation Id'] = df['EndStation Id'].astype(str)
        df['StartStation Id'] = df['StartStation Id'].astype(str)
    except KeyError:
        pass
    try:
        df['Start station number'] = df['Start station number'].astype(str)
        df['End station number'] = df['End station number'].astype(str)
    except KeyError:
        pass
    return df


@task(name='write result to local', log_prints=True)
def write_local(df: pd.DataFrame, url) -> Path:
    """Writes DataFrame as parquet file"""
    if not os.path.isdir('data'):
        os.makedirs('data')
    filename = url.split('/')[-1]
    path = Path(f"data/{filename.replace('.csv', '.parquet')}")
    df.to_parquet(path, compression='gzip')
    print(f'loaded {len(df)} rows into a parquet file')
    return path


@task(name='Write result to gcs')
def write_gcs(path: Path) -> None:
    """Upload parquet file to gcs"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("bike-rental-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)


@flow(name='Load to data lake')
def load_to_datalake(date_from: str, date_to: str) -> None:
    """
    Loads source data for requested period into data lake
    :param date_from: str
    :param date_to: str
    :return: None
    """

    urls = get_urls(date_from, date_to)

    for url in urls:
        df = read_file(url)
        path = write_local(df, url)
        write_gcs(path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--From", help="Date of extract start in %Y-%m-%d format")
    parser.add_argument("-t", "--To", help="Date of extract start in %Y-%m-%d format")

    # Read arguments from command line
    args = parser.parse_args()
    load_to_datalake('2022-10-24','2023-10-30')
    # load_to_datalake(args.date_from, args.date_to)

