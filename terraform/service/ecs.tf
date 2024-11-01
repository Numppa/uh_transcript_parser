data "aws_ecr_repository" "backend" {
  name = "${var.app_name}-backend"
}

data "aws_ecr_repository" "frontend" {
  name = "${var.app_name}-frontend"
}

resource "aws_ecs_cluster" "default" {
  name = "${var.app_name}-cluster"
}


resource "aws_ecs_task_definition" "default" {
  family             = "${var.app_name}-app-task"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  network_mode       = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                = 512
  memory             = 1024
  container_definitions = jsonencode(
    [
      {
        name = "frontend"
        image = "${data.aws_ecr_repository.frontend.repository_url}:latest"
        cpu = 256
        memory = 512
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group = "/ecs/${var.app_name}"
            awslogs-region = var.region
            awslogs-stream-prefix = "ecs"
          }
        },
        portMappings = [
          {
            containerPort = 80
            hostPort = 80
          }
        ]
        dependsOn = [
          {
            containerName = "backend"
            condition = "START"
          }
        ]

      },
      {
        name = "backend"
        image = "${data.aws_ecr_repository.backend.repository_url}:latest"
        cpu = 256
        memory = 512
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group = "/ecs/${var.app_name}"
            awslogs-region = var.region
            awslogs-stream-prefix = "ecs"
          }
        }
        portMappings = [
          {
            containerPort = 5000
            hostPort = 5000
          }
        ]
      }
    ]
  )
}

resource "aws_ecs_service" "default" {
    name            = "${var.app_name}-service"
    cluster         = aws_ecs_cluster.default.id
    task_definition = aws_ecs_task_definition.default.arn
    desired_count   = 1
    launch_type     = "FARGATE"

    network_configuration {
        security_groups  = [aws_security_group.ecs_tasks.id]
        subnets          = aws_subnet.private.*.id
        assign_public_ip = true
    }

    load_balancer {
        target_group_arn = aws_alb_target_group.app.id
        container_name   = "frontend"
        container_port   = 80
    }

    depends_on = [aws_alb_listener.front_end, aws_iam_role_policy_attachment.ecs-task-execution-role-policy-attachment]
}