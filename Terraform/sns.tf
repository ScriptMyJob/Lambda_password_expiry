########################################
### SNS Configurations #################
########################################

resource "aws_sns_topic" "password_expiration" {
    name = "Password_Expiration"
}

