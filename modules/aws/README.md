# aws module

terraform to create a bucket, trigger, and function to load, transform, and upload external billing data to harness

![image](https://github.com/user-attachments/assets/9d59b711-eef4-488f-86ba-f742947e06b9)

example input:
```
name          = "harness-external-data"
prefix        = "ccm-external-data"
provider_name = "CloudABC"
data_source   = "ABC Payer Account 1"
environment_variables = {
  HARNESS_ACCOUNT_ID       = "wlgELJ0TTre5aZhzpt8gVA"
  HARNESS_PLATFORM_API_KEY = "sat.wlgELJ0TTre5aZhzpt8gVA.xxx"
}
```

## Requirements

| Name | Version |
|------|---------|
| aws | ~> 5.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| lambda\_function | terraform-aws-modules/lambda/aws | ~> 4.0 |
| s3\_bucket | terraform-aws-modules/s3-bucket/aws | ~> 3.0 |
| s3\_notification | terraform-aws-modules/s3-bucket/aws//modules/notification | ~> 3.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| bucket\_name | Name of the s3 bucket | `string` | `null` | no |
| bucket\_prefix | Prefix for the s3 bucket | `string` | `"ccm-external-data"` | no |
| data\_source | Instance of the cloud platform to upload data store | `string` | n/a | yes |
| environment\_variables | Environment variables to pass to the lambda function | `map(string)` | `{}` | no |
| lambda\_name | Name of the lambda function | `string` | `null` | no |
| mapping | Mapping of focus fields to harness fields | `map(string)` | `{}` | no |
| name | Name of the resources in AWS | `string` | `null` | no |
| provider\_name | Cloud platform to upload data store | `string` | n/a | yes |

## Outputs

No outputs.
