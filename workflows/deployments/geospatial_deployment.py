from prefect.deployments import Deployment
from prefect.filesystems import GitHub

from workflows.flows.load_pipeline.load_geospatial import load_geospatial

github_block = GitHub.load("github")
deployment = Deployment.build_from_flow(
    flow=load_geospatial,
    name="load_geospatial",
    storage=github_block,
    version=1,
    work_queue_name="main")

if __name__ == '__main__':
    deployment.apply()
