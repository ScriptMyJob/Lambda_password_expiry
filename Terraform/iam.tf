########################################
### IAM Policies #######################
########################################

resource "aws_iam_policy" "lambda_expiry_test" {
    name    = "lambda_expiry_test"
    path    = "/"
    policy  = <<POLICY
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
POLICY
}

########################################
### IAM Roles ##########################
########################################

resource "aws_iam_role" "lambda_expiry_test" {
  name = "lambda_expiry_test"

  assume_role_policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
POLICY
}

########################################
### IAM Policy Attachments #############
########################################

resource "aws_iam_policy_attachment" "expiry_attach" {
    name            = "expiry_attach"
    roles           = [
        "${aws_iam_role.lambda_expiry_test.name}"
    ]
    policy_arn      = "${aws_iam_policy.lambda_expiry_test.arn}"
}
