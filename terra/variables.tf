variable "key_name" {
    description = "The name of the AWS key pair to use for SSH access to the EC2 instance"
    type = string
}

variable "db_username" {
    description = "The username to be used in the RDS database"
}

variable "db_password" {
    description = "The password to be used in the RDS database"
}

variable "jwt_secret" {
    description = "The JWT secret"
}