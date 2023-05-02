import os

from prefect import flow
from prefect_dbt.cli import DbtCliProfile, DbtCoreOperation


@flow
def trigger_dbt_flow():
    dbt_path = f"{os.getcwd()}/dbt"
    dbt_cli_profile = DbtCliProfile.load("dev-profile")
    with DbtCoreOperation(
            commands=["dbt build"],
            project_dir=dbt_path,
            profiles_dir=dbt_path,
            dbt_cli_profile=dbt_cli_profile,
            overwrite_profiles=True,
    ) as dbt_operation:
        dbt_process = dbt_operation.trigger()
        # do other things before waiting for completion
        dbt_process.wait_for_completion()
        result = dbt_process.fetch_result()
    return result


if __name__ == "__main__":
    trigger_dbt_flow()
