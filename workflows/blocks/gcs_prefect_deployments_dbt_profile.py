from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile
from prefect_gcp.credentials import GcpCredentials

credentials = GcpCredentials.load("default-credentials")
target_configs = BigQueryTargetConfigs(
    schema="br_intermediate",  # also known as dataset
    credentials=credentials,
)
target_configs.save("dev-target", overwrite=True)

dbt_cli_profile = DbtCliProfile(
    name="dev-profile",
    target="dev-target",
    target_configs=target_configs,
)
dbt_cli_profile.save("dev-profile", overwrite=True)
