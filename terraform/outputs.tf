output "alb_dns_name" {
  value = aws_lb.app_alb.dns_name
}

output "app_instance_public_ip" {
  value = aws_instance.app.public_ip
}

output "db_endpoint" {
  value = aws_db_instance.postgres.address
}
