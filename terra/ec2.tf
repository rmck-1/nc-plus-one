resource "aws_instance" "demo_instance" {
    ami = "resolve:ssm:/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
    lifecycle {
        ignore_changes = [ami]
    }
    instance_type = "t3.micro"
    tags = {
        Name = "NC-PLUS-ONE-API-SERVER"
  }

    vpc_security_group_ids = [aws_security_group.allow_http_ssh.id]
    key_name = var.key_name

    user_data = templatefile("${path.module}/api_launch.sh", {
        db_password = var.db_password
        db_username = var.db_username
        db_name = "postgres"
        db_address = aws_db_instance.api_db.address
        db_port = 5432
        jwt_secret = var.jwt_secret
    })
    user_data_replace_on_change = true
}

output "instance_ip" {
    value = aws_instance.demo_instance.public_ip
}

output "instance_public_dns" {
    value = aws_instance.demo_instance.public_dns
}