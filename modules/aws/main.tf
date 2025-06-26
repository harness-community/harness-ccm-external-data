module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = var.bucket_name != null ? var.bucket_name : var.name
}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"

  function_name = var.lambda_name != null ? var.lambda_name : var.name
  description   = "Upload new FOCUS exports to Harness CCM"
  handler       = "index.lambda_handler"
  runtime       = "python3.13"
  timeout       = "300"
  publish       = true

  source_path = [
    # "${path.module}/lambda",
    {
      path = "${path.module}/lambda",
      commands = [
        "python3 -m pip install --no-compile --target=. --requirement=requirements.txt",
        "rm -rf numpy* pandas*",
        ":zip"
      ],
    }
  ]

  layers = ["arn:aws:lambda:us-west-2:336392948345:layer:AWSSDKPandas-Python313:2"]

  allowed_triggers = {
    AllowExecutionFromS3Bucket = {
      service    = "s3"
      source_arn = module.s3_bucket.s3_bucket_arn
    }
  }

  attach_policy_json = true
  policy_json = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "s3:GetObject",
        Resource = "${module.s3_bucket.s3_bucket_arn}/*"
      }
    ]
  })

  environment_variables = {
    MAPPING  = jsonencode(var.mapping),
    PROVIDER = var.data_provider
  }
}

module "s3_notification" {
  source  = "terraform-aws-modules/s3-bucket/aws//modules/notification"
  version = "~> 3.0"

  bucket = module.s3_bucket.s3_bucket_id

  eventbridge = true

  lambda_notifications = {
    lambda = {
      function_arn  = module.lambda_function.lambda_function_arn
      function_name = module.lambda_function.lambda_function_name
      events        = ["s3:ObjectCreated:*"]
      filter_prefix = var.bucket_prefix
      filter_suffix = ".csv"
    }
  }
}
