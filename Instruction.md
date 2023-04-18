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

### Terraform 

This project infrastructure is managed by terraform. In order to deploy infrastructure run:

```shell
terraform apply
```

### Running pipelines 

This block explains the project pipeline and how to run and deploy them 

#### Load data into a data lake 

This pipeline is orchestrated by Prefect. It loads data from bike rental data source and loads transformed parquet
files into a data lake. Parquet allows significantly decrease size of objects. 