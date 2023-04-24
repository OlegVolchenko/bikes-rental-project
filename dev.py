from prefect.filesystems import GCS
import os

with open(os.environ['PREFECT_SA']) as f:
    service_account = f.read()

project = os.environ['PROJECT']
block = GCS(
    bucket_path=f"prefect-deployments_{project}/dev/",
    service_account_info=service_account,
    project="project"
)

block.save("dev")