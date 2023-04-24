import os

from prefect_gcp import GcpCredentials

with open(os.environ['PREFECT_SA']) as f:
    service_account = f.read()

project = os.environ['PROJECT']

credentials = GcpCredentials(
    service_account_info=service_account,
    project=project
)

credentials.save("default-credentials", overwrite=True)
