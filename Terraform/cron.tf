resource "aws_cloudwatch_event_rule" "cron_8AM_Everyday" {
    name                = "8AM_Everyday"
    description         = "Run at 8 AM CST Everyday"

    schedule_expression = "cron(00 13 * * ? *)"
}

resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id        = "AllowExecutionFromCloudWatch"
    action              = "lambda:InvokeFunction"
    function_name       = "${aws_lambda_function.expiry_test.arn}"
    principal           = "events.amazonaws.com"
    source_arn          = "${aws_cloudwatch_event_rule.cron_8AM_Everyday.arn}"
}

resource "aws_cloudwatch_event_target" "expiry_test" {
    rule                = "${aws_cloudwatch_event_rule.cron_8AM_Everyday.name}"
    target_id           = "${lookup(var.lambda,"name")}"
    arn                 = "${aws_lambda_function.expiry_test.arn}"
}
