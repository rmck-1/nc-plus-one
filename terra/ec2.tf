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

    user_data = file("${path.module}/api_launch.sh")
    user_data_replace_on_change = true
}

output "instance_ip" {
    value = aws_instance.demo_instance.public_ip
}

output "instance_public_dns" {
    value = aws_instance.demo_instance.public_dns
}