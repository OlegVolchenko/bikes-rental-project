from prefect.deployments import Deployment
from prefect.filesystems import GitHub

from workflows.flows.load_pipeline.dbt import trigger_dbt_flow

github_block = GitHub.load("github")
deployment = Deployment.build_from_flow(
    flow=trigger_dbt_flow,
    name="dbt flow",
    storage=github_block,
    version=1,
    work_queue_name="main")

if __name__ == '__main__':
    deployment.apply()
