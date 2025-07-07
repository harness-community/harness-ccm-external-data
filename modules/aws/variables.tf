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
  description = "Prefix for the s3 bucket"
}

variable "mapping" {
  type        = map(string)
  default     = {}
  description = "Mapping of focus fields to harness fields"
}

variable "provider_name" {
  type        = string
  description = "Cloud platform to upload data store"
}

variable "data_source" {
  type        = string
  description = "Instance of the cloud platform to upload data store"
}

variable "environment_variables" {
  type        = map(string)
  default     = {}
  description = "Environment variables to pass to the lambda function"
}