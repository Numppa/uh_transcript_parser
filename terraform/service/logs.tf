resource "aws_cloudwatch_log_group" "default" {
  name              = "/ecs/${var.app_name}"
  retention_in_days = 30

  tags = {
    Name = "${var.app_name}-log-group"
  }
}

resource "aws_cloudwatch_log_stream" "default" {
  name           = "${var.app_name}-log-stream"
  log_group_name = aws_cloudwatch_log_group.default.name
}