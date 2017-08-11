#!/usr/bin/env python
# Written by: Robert J.

import csv
from datetime import datetime, timedelta
import boto3
import time

#######################################
### Global Vars #######################
#######################################

sns_arn='arn:aws:sns:us-west-2:976168295228:Password_Expiration'
sns_subject='Upcoming Password Expirations'

#######################################
### Main Function #####################
#######################################

def main():
    report = get_report()
    out = read_data(report)
    sns_push(out)

    # print output for CLI execution
    print(out),

    # return output for manually running lambda
    return out


#######################################
### Program Specific Functions ########
#######################################

def get_report():
    client = boto3.client('iam')

    print("Generating Report...")
    client.generate_credential_report()

    time.sleep(2)

    print("Pulling Report...")
    payload = client.get_credential_report()

    data = payload['Content']

    return data


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
        expiration  = changed + timedelta(45)

        if diff_days >= -1:
            value = value + \
                '{}\'s password WILL expire at {}.'.format(
                    i['user'],
                    expiration
                ) + \
                "\n"

        if diff_days >= 45:
            value = value + \
                '{}\'s password HAS expired at {}.'.format(
                    i['user'],
                    expiration
                ) + \
                "\n"

    if value == '':
        value = 'There are no expiring passwords.'

    return value


def sns_push(sns_message):
    print("Pushing to SNS")
    client = boto3.client('sns')
    response = client.publish(
        TopicArn=sns_arn,
        Message=sns_message,
        Subject=sns_subject,
        MessageStructure='string'
    )

    return response


#######################################
### Execution #########################
#######################################

if __name__ == "__main__":
    main()


def execute_me_lambda(event, context):
    out = main()
    return out
