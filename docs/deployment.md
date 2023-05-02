
### Google Cloud Platform

This codebase needs access to GCP services. GCP project must be created before running everything bellow. 

Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

1. If this is your first time using `gcloud` CLI, run `gcloud init` and follow the instructions.
2. Run `gcloud auth login`
3. Run `gcloud config set project <PROJECT_ID>`
4. Run `gcloud auth application-default login`

### Installing requirements 

Make sure that you have development environment of your choice. For example Linux/Mac: 

```shell
python -m venv .venv
```
```shell
source .venv/bin/activate
```
```shell
pip install -r requirements.txt
```

### Prefect deployment

This block explains the project pipeline and how to run and deploy them

Create Prefect cloud account https://app.prefect.cloud/

Loging to Prefect account

```shell
prefect cloud login
```

Generate an API key in prefect cloud and save it somewhere

Create a key in secret manager for Prefect api

```shell
gcloud secrets create prefect-key \
    --replication-policy="automatic"
```

```shell
gcloud secrets create prefect-workspace \
    --replication-policy="automatic"
```
Add the key version to Secret Manager

```shell
echo -n "<prefect cloud key>" | \   
    gcloud secrets versions add prefect-key --data-file=- 
```

```shell
echo -n "<prefect cloud workspace>" | \   
    gcloud secrets versions add prefect-workspace --data-file=- 
```
export project name as variable

```shell
export PROJECT="<PROJECT_ID>"
```

Create service account key
Navigate to directory outside the repo. Do not save your credentials in the repo, make sure not to commit it to GitHub

```shell
gcloud iam service-accounts keys create service_account.json \
  --iam-account=prefect@$PROJECT.iam.gserviceaccount.com
```

export variable with a path to the sa key

```shell
export PREFECT_SA="<PREFECT_SA>"
```

### Terraform

This project infrastructure is managed by terraform. Update `infra/variables.tf` with details of your project and run:

```shell
cd infra
terraform apply
```

Terraform also manages google api, there might be an issue running that altogether so if there are errors on terraform
side, enable api manually in gcp project or by running gcloud cli commands.

### Deploy prefect blocks and flows

```shell
bash workflows/prefect_deployment.sh
```

Now all the deployed workflows can be triggered from prefect cloud ui
