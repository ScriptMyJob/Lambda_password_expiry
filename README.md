# AWS expiry notification

This is a simple python lambda function to run a report on users who are about to have their iam password expire:

# Configuration Steps:

Install HashiCorp Terraform
```
brew install terraform
```

Run Terraform on the `Terraform/` directory:
```
terraform apply Terraform/
```

This will run at 8 AM CST everyday, and can be modified in cron.tf

You can subscribe directly to the SNS Topic `Password_Expiration` in us-west-2:

https://us-west-2.console.aws.amazon.com/sns/v2/home?region=us-west-2#/topics
