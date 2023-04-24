import os

from prefect_gcp import GcpCredentials, GcsBucket

gcp_credentials = GcpCredentials.load("default-credentials")

project = os.environ['PROJECT']
gcs_bucket = GcsBucket(
    bucket=f"bike_rental_extract_{project}",
    gcp_credentials=gcp_credentials,
)
gcs_bucket.save("bike-rental-bucket", overwrite=True)
