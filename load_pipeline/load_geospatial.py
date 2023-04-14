import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials, GcsBucket


@flow(name='Load geospatial to bq', log_prints=True)
def load_to_bq() -> None:
    """Load DataFrame to bq"""
    df = pd.read_csv('../static_data/dim_geo.csv')
    gcp_cred_block = GcpCredentials.load('bootcamp-gcp-account')
    # ingest to bq, schema is optional but improves robustness
    df.to_gbq(
        destination_table=f'br_staged.dim_geospatial',
        project_id='zoomcamp-olvol3',
        credentials=gcp_cred_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists='replace'
    )
    print('DataFrame has been ingested to bq table ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--From", help="Date of extract start in %Y-%m-%d format")
    parser.add_argument("-t", "--To", help="Date of extract start in %Y-%m-%d format")

    # Read arguments from command line
    args = parser.parse_args()
    load_to_bq()

