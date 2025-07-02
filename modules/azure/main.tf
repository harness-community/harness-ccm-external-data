# Azure Storage + Function App module

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "this" {
  name = var.resource_group_name
}

resource "azurerm_storage_account" "this" {
  name                     = var.storage_account_name != null ? var.storage_account_name : var.name
  resource_group_name      = data.azurerm_resource_group.this.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "this" {
  name                  = var.container_name != null ? var.container_name : var.name
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}

# Render the function.json template for the Azure Function Blob Trigger
resource "local_file" "function_json" {
  content = templatefile("${path.module}/templates/function.json.tmpl", {
    container_name = azurerm_storage_container.this.name
  })
  filename = "${path.module}/function/function.json"
}

resource "azurerm_service_plan" "this" {
  name                = "${var.name}-plan"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.this.name
  os_type             = "Linux"
  sku_name            = "B1"
}
# Note: azurerm_service_plan replaces azurerm_app_service_plan. 'kind' and 'reserved' are not required; use 'os_type'. 'sku' block is replaced by 'sku_name'.

resource "azurerm_user_assigned_identity" "this" {
  name                = "${var.name}-identity"
  resource_group_name = data.azurerm_resource_group.this.name
  location            = var.location
}

resource "azurerm_linux_function_app" "this" {
  name                       = var.function_app_name != null ? var.function_app_name : var.name
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.this.name
  service_plan_id            = azurerm_service_plan.this.id
  storage_account_name       = azurerm_storage_account.this.name
  storage_account_access_key = azurerm_storage_account.this.primary_access_key
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.this.id]
  }
  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
  app_settings = {
    AzureWebJobsStorage      = azurerm_storage_account.this.primary_connection_string
    FUNCTIONS_WORKER_RUNTIME = "python"
    BLOB_CONTAINER           = azurerm_storage_container.this.name
    STORAGE_ACCOUNT          = azurerm_storage_account.this.name
  }
  depends_on = [azurerm_user_assigned_identity.this]
}

resource "azurerm_role_assignment" "this" {
  scope                = azurerm_storage_account.this.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.this.principal_id
}
