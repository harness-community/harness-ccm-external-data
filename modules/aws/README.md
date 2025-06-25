# aws module

terraform to create a bucket, trigger, and function to load, transform, and upload external billing data to harness

![image](https://github.com/user-attachments/assets/8abae462-b723-4899-9b52-46acce664189)

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
| bucket\_prefix | n/a | `string` | `"ccm-external-data"` | no |
| data\_provider | n/a | `string` | n/a | yes |
| lambda\_name | Name of the lambda function | `string` | `null` | no |
| mapping | n/a | `map(string)` | `{}` | no |
| name | Name of the resources in AWS | `string` | `null` | no |

## Outputs

No outputs.
