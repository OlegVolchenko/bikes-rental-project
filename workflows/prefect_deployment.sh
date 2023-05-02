#!/bin/bash
#blocks
python blocks/gcp_prefect_deployments_credentials.py
python workflows/blocks/gcp_prefect_deployments_github.py
python workflows/blocks/gcs_prefect_deployments_storage.py
python workflows/blocks/gcs_prefect_deployments_dbt_profile.py
#flows
python workflows/deployments/gcs_to_bq_deployment.py
python workflows/deployments/geospatial_deployment.py
python workflows/deployments/raw_to_gcs_deployment.py
python workflows/deployments/dbt_deployment.py