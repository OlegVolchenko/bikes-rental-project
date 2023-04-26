from prefect.deployments import Deployment

from workflows.flows.extract_pipeline.raw_to_gcs import load_to_datalake

# gcs_block = GCS.load("deployments")
deployment = Deployment.build_from_flow(
    flow=load_to_datalake,
    name="load_to_datalake_deployment",
    # storage=gcs_block,
    version=1,
    work_queue_name="main")
if __name__ == '__main__':
    deployment.apply()
