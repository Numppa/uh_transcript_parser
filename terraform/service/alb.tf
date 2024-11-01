resource "aws_alb" "default" {
    name        = "${var.app_name}-lb"
    subnets         = aws_subnet.public.*.id
    security_groups = [aws_security_group.lb.id]
}

resource "aws_alb_target_group" "app" {
    name        = "${var.app_name}-tg"
    port        = 80
    protocol    = "HTTP"
    vpc_id      = aws_vpc.default.id
    target_type = "ip"

    health_check {
        healthy_threshold   = "3"
        interval            = "300"
        protocol            = "HTTP"
        matcher             = "200"
        timeout             = "3"
        path                = "/"
        unhealthy_threshold = "2"
    }
}

data "aws_route53_zone" "default" {
  name         = var.domain-name
}

resource "aws_route53_record" "default" {
  name    = data.aws_route53_zone.default.name
  type    = "A"
  zone_id = data.aws_route53_zone.default.zone_id

  alias {
    name                   = aws_alb.default.dns_name
    zone_id                = aws_alb.default.zone_id
    evaluate_target_health = true
  }
}

resource "aws_alb_listener" "front_end" {
  load_balancer_arn = aws_alb.default.id
  port              = 443
  protocol          = "HTTPS"
  certificate_arn = data.aws_acm_certificate.default.arn

  default_action {
    target_group_arn = aws_alb_target_group.app.id
    type             = "forward"
  }
}

data "aws_acm_certificate" "default" {
    domain   = var.domain-name
    statuses = ["ISSUED"]
}

resource "aws_lb_listener_certificate" "default" {
  certificate_arn = data.aws_acm_certificate.default.arn
  listener_arn    = aws_alb_listener.front_end.arn
}
