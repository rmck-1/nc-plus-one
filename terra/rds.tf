resource "aws_db_instance" "api_db" {
    identifier = "api-postgres-db"
    instance_class = "db.t3.micro"
    engine = "postgres"
    engine_version = "14"
    allocated_storage = 20
    username = var.db_username
    password = var.db_password
    publicly_accessible = false
    skip_final_snapshot = true
    vpc_security_group_ids = [aws_security_group.rds_sg.id]
}

output "rds_instance_address" {
    value = aws_db_instance.api_db.address
}

output "rds_instance_ports" {
    value = aws_db_instance.api_db.port
}