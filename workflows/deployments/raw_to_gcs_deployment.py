from prefect.deployments import Deployment
from prefect.filesystems import GitHub

from workflows.flows.extract_pipeline.raw_to_gcs import load_to_datalake

github_block = GitHub.load("github")
deployment = Deployment.build_from_flow(
    flow=load_to_datalake,
    name="load_to_datalake_deployment",
    storage=github_block,
    version=1,
    work_queue_name="main")

if __name__ == '__main__':
    deployment.apply()
