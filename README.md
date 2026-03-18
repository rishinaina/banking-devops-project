# Banking API DevOps Take-Home Project

This project provides a simple but complete answer for the take-home assignment:
- Flask REST API for banking account operations
- PostgreSQL database
- AWS infrastructure using Terraform
- GitHub Actions CI/CD pipeline
- Basic security, logging, and monitoring guidance

## 1. Architecture

```text
Internet
   |
Application Load Balancer
   |
EC2 instance running Dockerized Flask API
   |
Amazon RDS PostgreSQL (private subnet)
```

### Why this design?
- **ALB** gives a clean public entry point.
- **EC2** keeps deployment simple for a take-home task.
- **RDS PostgreSQL** provides managed storage.
- **Terraform** automates provisioning.
- **GitHub Actions** automates deployment.

## 2. API Endpoints

### Health Check
```bash
GET /health
```

### Initialize Database
```bash
POST /init
```

### Get Balance
```bash
GET /balance/1
```

### Deposit Money
```bash
POST /deposit/1
Content-Type: application/json
{
  "amount": 250
}
```

### Withdraw Money
```bash
POST /withdraw/1
Content-Type: application/json
{
  "amount": 100
}
```

## 3. Local Run

From the `app` folder:

```bash
docker-compose up --build
```

Then initialize the database:

```bash
curl -X POST http://localhost:5000/init
```

Test balance:

```bash
curl http://localhost:5000/balance/1
```

## 4. Terraform Deployment Steps

From the `terraform` folder:

```bash
terraform init
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars
terraform plan
terraform apply
```

After apply, Terraform prints:
- ALB DNS name
- EC2 public IP
- RDS endpoint

## 5. Deploy App to EC2

1. SSH into EC2.
2. Copy the `app/` folder to the server.
3. Build and run Docker image.
4. Use the RDS endpoint as `DB_HOST`.

Example:

```bash
docker build -t banking-api .
docker run -d --name banking-api -p 5000:5000 \
  -e DB_HOST=<RDS_ENDPOINT> \
  -e DB_PORT=5432 \
  -e DB_NAME=bankdb \
  -e DB_USER=bankuser \
  -e DB_PASSWORD=<PASSWORD> \
  banking-api
```

Then initialize:

```bash
curl -X POST http://localhost:5000/init
```

## 6. GitHub Actions Secrets Needed

Set these in GitHub repository secrets:
- `EC2_HOST`
- `EC2_SSH_KEY`
- `DB_HOST`
- `DB_PASSWORD`

## 7. Security Measures

- Security groups restrict access.
- RDS is placed in private subnets.
- RDS storage encryption is enabled.
- Only ALB can reach the app on port 5000.
- Only the app server can reach the database on port 5432.
- HTTPS can be added by attaching an ACM certificate to the ALB listener.

## 8. Monitoring and Logging

Recommended for submission:
- Send application logs to CloudWatch.
- Enable EC2 and ALB metrics in CloudWatch.
- Create alarms for CPU, unhealthy hosts, and DB storage.
- Enable RDS monitoring and backups.

## 9. What to Submit

- This source code
- Terraform files
- CI/CD workflow
- Architecture explanation
- Screenshots of deployed resources and test API calls

## 10. Interview Summary

This solution is intentionally simple and practical for a take-home task. It focuses on:
- correctness
- clean infrastructure structure
- secure network separation
- automation with Terraform
- easy deployment with GitHub Actions

## 11. Suggested Improvements

If you want to make it stronger later:
- Use Auto Scaling Group instead of one EC2 instance
- Use ECR to store Docker images
- Use SSM Parameter Store / Secrets Manager for DB secrets
- Add HTTPS listener with ACM
- Add CloudWatch agent and dashboards
- Add unit tests and health probes
