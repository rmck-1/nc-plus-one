resource "aws_instance" "demo_instance" {
    ami = "resolve:ssm:/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
    lifecycle {
        ignore_changes = [ami]
    }
    instance_type = "t3.micro"
    tags = {
        Name = "NC-PLUS-ONE-API-SERVER"
  }
    # iam_instance_profile = aws_iam_instance_profile.ec2_secrets_profile.name
    vpc_security_group_ids = [aws_security_group.allow_ssh.id]
    key_name = var.key_name

    # user_data = file("${path.module}/script.sh")
    # user_data_replace_on_change = true
}

output "instance_ip" {
    value = aws_instance.demo_instance.public_ip
}