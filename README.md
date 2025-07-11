# harness-ccm-external-data

tools to help manage ingesting external data in harness ccm

the project is split into several parts:
- converting external data formats to a compatible format for harness (focus)
- uploading the converted data to the harness platform

## loading data

when loading in a billing export we can apply a few modifications of the data to prepare it for ingestion into harness.

first, we convert any non-focus fields to their focus equivalent. this is done by providing a map of focus fields to their corresponding non-focus fields.

```python
mapping = {
    "BillingAccountId": "Organization ID",
    "BillingAccountName": "Organization Name",
    ...
}
```

if only a subset of fields need remapping you can specify only those which need changed.

next we create a `Focus` object, specifying the platform, local billing export file, field mappings (if needed) and any data modifications needed:

```python
from harness_ccm_external_data import Focus

my_data = Focus(
    # name of the provider where the billing data came from
    provider="CloudABC",
    # name of this particular data source from the above provider
    datasource="ABC Payer Account 1",
    # csv with focus data
    filename="abc_billing_export.csv",
    # focus to non focus mappings (if they exist)
    mappings={
        "BillingAccountId": "Organization ID",
        "BillingAccountName": "Organization Name",
        ...
    }
    # skip the first n rows of the billing data
    skip_rows=100,
    # you can also specify specific rows to skip
    # skip_rows=[0, 2, 4, 6, 8],
    # apply a multiplier to the cost (account for discounts not shown in the export?)
    cost_multiplier=0.95
    # if the csv is in a non-standard format
    separator=";"
    # apply a function to any column value
    converters={
        "ChargeCategory": lambda x: lower(x)
    },
    # for data upload to harness
    harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
    harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
)
```

now we can render the data to the harness platform format to be uploaded by hand in the UI:

```
my_data.render_file("harness_focus_my_billing_export.csv")
```

## uploading data

uploading the data to harness is as simple as executing the upload function, there is no need to render the data to a file before doing so:

```python
my_data.upload()
```

this will auto-detect the invoice period from the data, upload it, and trigger ingestion

## docker

there is a docker image available to enable running the automation via docker or a plugin in a harness pipeline:

```
docker run --rm -it \
  -v ${PWD}/focus_sample.csv:/focus_sample.csv \
  -v ${PWD}:/output \
  -e CSV_FILE=/focus_sample.csv \
  -e PROVIDER=CloudABC \
  -e DATA_SOURCE="ABC Payer Account 1" \
  -e RENDER_FILE=/output/docker_focus.csv # optional \
  -e UPLOAD=true # optional \
  harnesscommunity/harness-ccm-external-data
```

### drone plugin

the container can also be used as a drone/harness plugin:

```yaml
- step:
    type: Plugin
    name: upload
    identifier: upload
    spec:
        connectorRef: account.buildfarm_container_registry_cloud
        image: harnesscommunity/harness-ccm-external-data
        settings:
            PROVIDER: CloudABC
            DATA_SOURCE: ABC Payer Account 1
            CSV_FILE: /harness/focus_sample.csv
            HARNESS_ACCOUNT_ID: <+account.identifier>
            HARNESS_PLATFORM_API_KEY: <+secrets.getValue("account.account_admin")>
            UPLOAD: "true" # optional
            RENDER_FILE: /harness/harness_focus_sample.csv # optional
```

## modules

there are patterns provided for extracting, transforming, and loading external data into harness under the `modules` folder:

- aws: s3+lambda function

### data loading settings

- `RENDER_FILE`: file path to render harness-focus data to
- `PROVIDER`: 
- `CSV_FILE`: 
- `MAPPING`: 
- `SKIP_ROWS`: 
- `COST_MULTIPLIER`: 
- `VALIDATE`: 

## development

pull the example focus csv: `curl -LO https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS-Sample-Data/refs/heads/main/FOCUS-1.0/focus_sample.csv`

install [poetry](https://python-poetry.org/docs/#installation)

testing: `make test`
