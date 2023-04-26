import os

import pandas as pd
from prefect import flow
from prefect_gcp import GcpCredentials


@flow(name='Load geospatial', log_prints=True)
def load_geospatial() -> None:
    """Load DataFrame to bq"""
    df = pd.read_csv('static_data/dim_geo.csv')
    gcp_cred_block = GcpCredentials.load('default-credentials')
    # ingest to bq, schema is optional but improves robustness
    df.to_gbq(
        destination_table=f'br_staged.dim_geospatial',
        project_id=os.environ['PROJECT'],
        credentials=gcp_cred_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists='replace',
        table_schema=[{'name': 'District', 'type': 'STRING'}, {'name': 'Geometry', 'type': 'STRING'}]
    )
    print('DataFrame has been ingested to bq table ')


if __name__ == '__main__':
    load_geospatial()
