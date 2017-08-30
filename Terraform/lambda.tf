########################################
### Lambda Configs: ####################
########################################

# lambda_expiry
####################

data "archive_file" "zip_expiry_test" {
    type            = "zip"

    source_file     = "${path.module}/../Resources/expiry.py"
    output_path     = "${path.module}/../Resources/expiry.zip"
}

resource "aws_lambda_function" "expiry_test" {

    depends_on      = [
        "data.archive_file.zip_expiry_test"
    ]

    filename        = "${path.module}/../Resources/expiry.zip"
    function_name   = "${lookup(var.lambda,"name")}"
    role            = "${aws_iam_role.lambda_expiry_test.arn}"
    handler         = "expiry.execute_me_lambda"
    runtime         = "python2.7"
    memory_size     = 128
    timeout         = 5
    environment {
        variables = {
            account = "${data.aws_iam_account_alias.current.account_alias}",
            sns_arn = "${aws_sns_topic.password_expiration.arn}"
        }
    }
}
