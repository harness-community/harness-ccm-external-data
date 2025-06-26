variable "name" {
  type        = string
  default     = null
  description = "Name of the resources in AWS"
}

variable "lambda_name" {
  type        = string
  default     = null
  description = "Name of the lambda function"
}

variable "bucket_name" {
  type        = string
  default     = null
  description = "Name of the s3 bucket"
}

variable "bucket_prefix" {
  type        = string
  default     = "ccm-external-data"
  description = ""
}

variable "mapping" {
  type    = map(string)
  default = {}
}

variable "data_provider" {
  type = string
}