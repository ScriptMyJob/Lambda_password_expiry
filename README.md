# AWS expiry notification

This is a simple python lambda function to run a report on users who are about to have their sns password expire:

# Configuration Steps:


Name:
```
Password_Notification
```

Runtime:
```
Python 2.7
```

Handler:
```
lambda_function.lambda_execute_me
```

Role:
```
New Custom Role
```

Role name:
```
Lambda_Passowrd_Notification
```

Policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GenerateCredentialReport",
                "iam:GetCredentialReport"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "*"
        }
    ]
}
```
