########################################
### Variables ##########################
########################################

variable "global" {
    type    = "map"
    default = {
        region  = "us-west-2"
        tags    = "lambda_expiry_test"
    }
}

variable "lambda" {
    type    = "map"
    default = {
        name    = "lambda_expiry_test"
    }
}
