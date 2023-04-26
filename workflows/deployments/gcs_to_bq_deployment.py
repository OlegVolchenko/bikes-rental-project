from prefect.deployments import Deployment
from prefect.filesystems import GitHub

from workflows.flows.load_pipeline.gcs_to_bq import load_to_dw

github_block = GitHub.load("github")
deployment = Deployment.build_from_flow(
    flow=load_to_dw,
    name="load_to_dw",
    storage=github_block,
    version=1,
    work_queue_name="main")

if __name__ == '__main__':
    deployment.apply()
