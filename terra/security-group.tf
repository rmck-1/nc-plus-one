data "http" "myip" {
    url = "https://ipv4.icanhazip.com"
}

data "aws_vpc" "default" {
    default = true
}

resource "aws_security_group" "allow_ssh" {
    name_prefix = "ssh-sg-"
    description = "Security group to enable SSH and HTTP on EC2."
    vpc_id = data.aws_vpc.default.id
    tags = {
        name = "web_server"
        purpose = "security group for SSH and HTTP access for my IP access"
    }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ingress" {
    security_group_id = aws_security_group.allow_ssh.id
    ip_protocol = "tcp"
    from_port = 22
    to_port = 22
    cidr_ipv4 = "${chomp(data.http.myip.response_body)}/32"
    tags = {
        name = "allow_ssh"
    }
}

# resource "aws_vpc_security_group_ingress_rule" "allow_http_ingress" {
#     security_group_id = aws_security_group.allow_ssh.id
#     ip_protocol = "tcp"
#     from_port = 80
#     to_port = 80
#     cidr_ipv4 = "${chomp(data.http.myip.response_body)}/32"
#     tags = {
#         name = "allow_http"
#     }
# }

resource "aws_vpc_security_group_egress_rule" "allow_egress" {
    security_group_id = aws_security_group.allow_ssh.id
    ip_protocol = "-1"
    cidr_ipv4 = "0.0.0.0/0"
    tags = {
        name = "egress_rule"
    }

}