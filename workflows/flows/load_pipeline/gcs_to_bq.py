import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials, GcsBucket


def cloud_storage_flow():
    gcp_credentials = GcpCredentials.load('default-credentials')
    gcs_bucket = GcsBucket(
        bucket=f"bike_rental_extract_{os.environ['PROJECT']}",
        gcp_credentials=gcp_credentials
    )

    downloaded_file_path = gcs_bucket.download_object_to_path(
        Path('data/info.json'), 'info.json'
    )
    return downloaded_file_path.read_text()


def get_ids(date_from: str, date_to: str) -> List:
    """

    :param date_from:
    :param date_to:
    :return:
    """
    info = cloud_storage_flow()
    info = json.loads(info)
    ids = [key for key in info.keys() if (datetime.strptime(date_from, "%Y-%m-%d").date() <= datetime.strptime(info[key]['date_from'], "%Y-%m-%d").date() and (datetime.strptime(date_to, "%Y-%m-%d").date() >= datetime.strptime(info[key]['date_from'], "%Y-%m-%d").date()))]
    return ids


@task(name='Extract from gcs', retries=3)
def extract_from_gcs(id: str) -> Path:
    """Download data from gcs"""
    gcs_path = f'data/{id}.parquet'
    gcs_block = GcsBucket.load("bike-rental-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"data/")
    return Path(f"data/{gcs_path}")


@task(name='Transform df', log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    """Fix dtype issues"""
    print(f'transforming {path}')
    df = pd.read_parquet(path)
    # rename columns
    columns_mapping = {'rental id': 'rental_id',
                       'number': 'rental_id',
                       'end date': 'end_date',
                       'endstation name': 'endstation_name',
                       'start date': 'start_date',
                       'startstation name': 'startstation_name',
                       'start station': 'startstation_name',
                       'end station': 'endstation_name',
                       'end station name': 'endstation_name',
                       'start station name': 'startstation_name'}
    df = df.rename(columns=columns_mapping)
    # select columns that are needed for modeling
    df = df[['rental_id', 'start_date', 'end_date', 'startstation_name', 'endstation_name']]
    # since there are multpiple files, makes sure that type is correct
    df['export_id'] = str(path).split('/')[-1]
    df['rental_id'] = df['rental_id'].astype(int)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['startstation_name'] = df['startstation_name'].astype(str)
    df['endstation_name'] = df['endstation_name'].astype(str)
    df.dropna(subset=['start_date', 'end_date'], inplace=True)
    return df


@task(name='Load to bq', log_prints=True)
def load_to_bq(df: pd.DataFrame, id: int) -> None:
    """Load DataFrame to bq"""

    gcp_cred_block = GcpCredentials.load('bootcamp-gcp-account')
    print(f'Ingesting {id} id to bq')
    # ingest to bq, schema is optional but improves robustness
    df.to_gbq(
        destination_table=f'br_staged.trips_export',
        project_id=os.environ['PROJECT'],
        credentials=gcp_cred_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists='append',
        table_schema=[{'name': 'export_id', 'type': 'STRING'}, {'name': 'rental_id', 'type': 'INT64'},
                      {'name': 'star_date', 'type': 'DATETIME'},
                      {'name': 'end_date', 'type': 'DATETIME'}, {'name': 'startstation_id', 'type': 'STRING'},
                      {'name': 'startstation_name', 'type': 'STRING'}, {'name': 'endstation_id', 'type': 'STRING'},
                      {'name': 'endstation_name', 'type': 'STRING'}]
    )
    print('DataFrame has been ingested to bq table ')


@flow(name='ingest_data_to_bg', log_prints=True)
def load_to_dw(date_from: str, date_to: str) -> None:
    """Main etl flow to load data into bq"""
    ids = get_ids(date_from, date_to)
    for id in ids:
        try:
            path = extract_from_gcs(id)
            df = transform(path)
            load_to_bq(df, id)
        except Exception as e:
            print(f'{id} failed ingestion reason {e}')
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--From", help="Date of extract start in %Y-%m-%d format")
    parser.add_argument("-t", "--To", help="Date of extract start in %Y-%m-%d format")

    # Read arguments from command line
    args = parser.parse_args()
    load_to_dw(args.From, args.To)

