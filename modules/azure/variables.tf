variable "resource_group_name" {
  description = "Name of the resource group."
  type        = string
}

variable "location" {
  description = "Location for resources."
  type        = string
}

variable "name" {
  description = "Base name for resources."
  type        = string
}

variable "storage_account_name" {
  description = "Storage account name (must be globally unique, 3-24 lowercase letters/numbers)."
  type        = string
  default     = null
}

variable "container_name" {
  description = "Blob container name."
  type        = string
  default     = null
}

variable "function_app_name" {
  description = "Function App name."
  type        = string
  default     = null
}
