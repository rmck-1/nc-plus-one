# 1. Create the IAM Role that EC2 can assume
resource "aws_iam_role" "ec2_secrets_role" {
  name = "ec2_secrets_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# 2. Create the Policy granting permission to read the token
resource "aws_iam_policy" "secrets_policy" {
  name        = "ec2_read_github_token"
  description = "Allow EC2 to read GithubToken from Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "secretsmanager:GetSecretValue"
        Resource = "*"
      }
    ]
  })
}

# 3. Attach the Policy to the Role
resource "aws_iam_role_policy_attachment" "attach_secrets_policy" {
  role       = aws_iam_role.ec2_secrets_role.name
  policy_arn = aws_iam_policy.secrets_policy.arn
}

# 4. Create the Instance Profile (This is what actually attaches to the EC2 server)
resource "aws_iam_instance_profile" "ec2_secrets_profile" {
  name = "ec2_secrets_profile"
  role = aws_iam_role.ec2_secrets_role.name
}