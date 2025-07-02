# Azure Function Template Usage

This directory contains a `function.json.tmpl` file, which is a Terraform template for the Azure Function Blob Trigger.

## How to Render in Terraform

Add the following to your Terraform module to render the template:

```
data "template_file" "function_json" {
  template = file("${path.module}/function/function.json.tmpl")
  vars = {
    container_name = var.container_name
  }
}

resource "local_file" "function_json" {
  content  = data.template_file.function_json.rendered
  filename = "${path.module}/function/function.json"
}
```

- This will render `function.json` with the correct container name for your deployment package.
- Ensure `terraform-provider-template` is available if using `template_file` data source (for Terraform 0.12 and earlier). For Terraform 0.13+, use the `templatefile()` function instead.
