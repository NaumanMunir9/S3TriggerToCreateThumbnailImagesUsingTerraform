output "iam_arn" {
  description = "Lambda S3 Policy ARN"
  value       = aws_iam_policy.lambda_s3_policy.arn
}

output "function_name" {
  description = "Lambda Function Name"
  value       = aws_lambda_function.create_thumbnail_lambda_function.function_name
}

output "cloud_watch_arn" {
  description = "CloudWatch ARN"
  value       = aws_cloudwatch_log_group.create_thumbnail_lambda_function_cloudwatch.arn
}
