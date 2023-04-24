### Set enironmental variables

```shell
export PROJECT="de-hires-project"
```

### Google Cloud Platform

This codebase needs access to GCP services. GCP project must be created before running everything bellow. 

Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

1. If this is your first time using `gcloud` CLI, run `gcloud init` and follow the instructions.
2. Run `gcloud auth login`
3. Run `gcloud config set project @PROJECT`
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

### Terraform 

This project infrastructure is managed by terraform. In order to deploy infrastructure run:

```shell
terraform apply
```

### Running pipelines 

This block explains the project pipeline and how to run and deploy them 

Create Prefect cloud account https://app.prefect.cloud/

Loging to Prefect account 

```shell
prefect cloud login
```

Create service account key
Navigate to directory outside the repo. Do not save your credentials in the repo, make sure not to commit it to GitHub
```shell
gcloud iam service-accounts keys create service_account.json \
  --iam-account=prefect@$PROJECT.iam.gserviceaccount.com
```
export variable with a path to the sa key
```shell
export PREFECT_SA=/Users/oleg.volchenko/Documents/secret/service_account.json
```
navigate to project root and create dev block
```shell
python dev.py
```
#### Load data into a data lake 

This pipeline is orchestrated by Prefect. It loads data from bike rental data source and loads transformed parquet
files into a data lake. Parquet allows significantly decrease size of objects. 