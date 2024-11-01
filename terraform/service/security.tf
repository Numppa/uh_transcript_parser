resource "aws_security_group" "lb" {
    name        = "${var.app_name}-lb-sg"
    description = "controls access to the ALB"
    vpc_id      = aws_vpc.default.id

    ingress {
        protocol    = "tcp"
        from_port   = 80
        to_port     = 80
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        protocol    = "tcp"
        from_port   = 443
        to_port     = 443
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        protocol    = "-1"
        from_port   = 0
        to_port     = 0
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_security_group" "ecs_tasks" {
    name        = "${var.app_name}-ecs-tasks-sg"
    description = "allow inbound access from the ALB only"
    vpc_id      = aws_vpc.default.id

    ingress {
        protocol  = "tcp"
        from_port = 80
        to_port   = 80
        security_groups = [aws_security_group.lb.id]
    }

    ingress {
        protocol  = "tcp"
        from_port = 5000
        to_port   = 5000
        security_groups = [aws_security_group.lb.id]
    }

    egress {
        protocol    = "-1"
        from_port   = 0
        to_port     = 0
        cidr_blocks = ["0.0.0.0/0"]
    }
}