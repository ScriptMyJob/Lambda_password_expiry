#!/usr/bin/env python
# Written by: Robert J.

import csv
from datetime import datetime, timedelta
import boto3
import sys
import time

#######################################
### Global Vars #######################
#######################################

sns_arn     = 'arn:aws:sns:us-west-2:976168295228:Password_Expiration'
account     = 'scriptmyjob'
sns_subject = 'Upcoming Password Expirations - ' + account

iam         = boto3.client('iam')
sns         = boto3.client('sns')

#######################################
### Main Function #####################
#######################################

def main():
    report = get_report()

    get_password_age()
    test_policy(passwd_age)

    output = read_data(report)

    out_logic(output)

    # print output for CLI execution
    print(output),

    # return output for manually running lambda
    return output


#######################################
### Program Specific Functions ########
#######################################

def get_report():
    print("Generating Report...")

    state = iam.generate_credential_report()['State']
    print(state)

    while state != 'COMPLETE':
        state = iam.generate_credential_report()['State']
        print("Report in progress: %s", state)
        time.sleep(0.25)

    print("Pulling Report...")
    data = iam.get_credential_report()['Content']

    return data


def get_password_age():
    print("Pulling current password policy...")

    global passwd_age
    passwd_age = iam.get_account_password_policy()['PasswordPolicy']['MaxPasswordAge']
    print(str(passwd_age) + " days")

    return passwd_age


def test_policy(passwd_age):
    if isinstance( passwd_age, int ):
        global passwd_notification
        passwd_notification = passwd_age - 7;
    else:
        sns_push('Password IAM Policy Password Expiration has been disabled.')
        sys.exit()


def read_data(data):
    value = ''

    print("Parsing Report...")
    for i in csv.DictReader(data.split()):
        print(i['user'])
        if i['password_last_changed'] == 'not_supported':
            continue
        if i['password_last_changed'] == 'N/A':
            continue

        # date information for parsing
        fmt         = '%Y-%m-%dT%H:%M:%S+00:00'
        date        = i['password_last_changed']

        # date changed and now
        changed     = datetime.strptime(date, fmt)
        now         = datetime.now()

        # date difference
        diff        = now - changed
        diff_days   = diff.total_seconds()/3600/24
        expiration  = changed + timedelta(passwd_age)

        if diff_days >= passwd_age :
            value = value + \
                '{:>20}\'s password HAS expired at {}.'.format(
                    i['user'],
                    expiration
                ) + \
                "\n"
            continue

        if diff_days >= passwd_notification :
            value = value + \
                '{:>20}\'s password WILL expire at {}.'.format(
                    i['user'],
                    expiration
                ) + \
                "\n"

    if value == '':
        value = 'There are no expiring passwords.'

    return value


def sns_push(sns_message):
    print("Pushing to SNS")
    response = sns.publish(
        TopicArn=sns_arn,
        Message=sns_message,
        Subject=sns_subject,
        MessageStructure='string'
    )

    return response


def out_logic(out):
    if out != 'There are no expiring passwords.':
        email = "Passwords can be reset at:" + \
            "\n" + "\n" + \
            account + ".signin.aws.amazon.com/console" + \
            "\n" + "\n" + \
            "Currnet Policy's have passwords expiring every " + \
            str(passwd_age) + " days" + \
            "\n" + "\n" + \
            out

        sns_push(email)


#######################################
### Execution #########################
#######################################

if __name__ == "__main__":
    main()


def execute_me_lambda(event, context):
    out = main()
    return out
