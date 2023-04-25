import os

from prefect_gcp import GcpCredentials, GcsBucket

gcp_credentials = GcpCredentials.load("default-credentials")

project = os.environ['PROJECT']
gcs_bucket = GcsBucket(
    bucket=f"prefect-deployments_{project}",
    gcp_credentials=gcp_credentials,
)
gcs_bucket.save("prefect-deployments", overwrite=True)
