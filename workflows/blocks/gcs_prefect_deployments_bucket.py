import os

from prefect_gcp import GcpCredentials

gcp_credentials = GcpCredentials.load("default-credentials")

from prefect.filesystems import GCS

block = GCS(
    bucket_path=f"prefect-deployments_{os.environ['PROJECT']}",
    service_account_info=gcp_credentials,
    project=os.environ["PROJECT"]
)

block.save("deployments")
