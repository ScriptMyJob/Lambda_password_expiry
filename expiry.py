#!/usr/bin/env python

import base64
import csv
from datetime import datetime, timedelta

def main():
    report = get_report()
    out = read_data(report)
    print(out)
    return out

def get_report():
    test_hash ="dXNlcixhcm4sdXNlcl9jcmVhdGlvbl90aW1lLHBhc3N3b3JkX2VuYWJsZWQscGFzc3dvcmRfbGFzdF91c2VkLHBhc3N3b3JkX2xhc3RfY2hhbmdlZCxwYXNzd29yZF9uZXh0X3JvdGF0aW9uLG1mYV9hY3RpdmUsYWNjZXNzX2tleV8xX2FjdGl2ZSxhY2Nlc3Nfa2V5XzFfbGFzdF9yb3RhdGVkLGFjY2Vzc19rZXlfMV9sYXN0X3VzZWRfZGF0ZSxhY2Nlc3Nfa2V5XzFfbGFzdF91c2VkX3JlZ2lvbixhY2Nlc3Nfa2V5XzFfbGFzdF91c2VkX3NlcnZpY2UsYWNjZXNzX2tleV8yX2FjdGl2ZSxhY2Nlc3Nfa2V5XzJfbGFzdF9yb3RhdGVkLGFjY2Vzc19rZXlfMl9sYXN0X3VzZWRfZGF0ZSxhY2Nlc3Nfa2V5XzJfbGFzdF91c2VkX3JlZ2lvbixhY2Nlc3Nfa2V5XzJfbGFzdF91c2VkX3NlcnZpY2UsY2VydF8xX2FjdGl2ZSxjZXJ0XzFfbGFzdF9yb3RhdGVkLGNlcnRfMl9hY3RpdmUsY2VydF8yX2xhc3Rfcm90YXRlZAo8cm9vdF9hY2NvdW50Pixhcm46YXdzOmlhbTo6OTc2MTY4Mjk1MjI4OnJvb3QsMjAxNi0wNy0yM1QwNzowNzo0OSswMDowMCxub3Rfc3VwcG9ydGVkLDIwMTctMDctMjBUMTU6MTg6MjkrMDA6MDAsbm90X3N1cHBvcnRlZCxub3Rfc3VwcG9ydGVkLHRydWUsZmFsc2UsTi9BLE4vQSxOL0EsTi9BLGZhbHNlLE4vQSxOL0EsTi9BLE4vQSxmYWxzZSxOL0EsZmFsc2UsTi9BCnJvYmVydC5qYWNrc29uLGFybjphd3M6aWFtOjo5NzYxNjgyOTUyMjg6dXNlci9yb2JlcnQuamFja3NvbiwyMDE3LTA3LTE4VDIxOjQxOjM2KzAwOjAwLHRydWUsMjAxNy0wOC0wN1QxNTo1ODoxNiswMDowMCwyMDE3LTA3LTE4VDIxOjU4OjE3KzAwOjAwLDIwMTctMDktMDFUMjE6NTg6MTcrMDA6MDAsdHJ1ZSxmYWxzZSxOL0EsTi9BLE4vQSxOL0EsZmFsc2UsTi9BLE4vQSxOL0EsTi9BLGZhbHNlLE4vQSxmYWxzZSxOL0EKcm9iZXJ0LmphY2tzb24uY2xpLGFybjphd3M6aWFtOjo5NzYxNjgyOTUyMjg6dXNlci9yb2JlcnQuamFja3Nvbi5jbGksMjAxNy0wNy0xOVQxMzozNDowMSswMDowMCxmYWxzZSxOL0EsTi9BLE4vQSxmYWxzZSx0cnVlLDIwMTctMDctMTlUMTM6MzQ6MDErMDA6MDAsMjAxNy0wOC0xMFQxNDoxNjowMCswMDowMCx1cy1lYXN0LTEsaWFtLGZhbHNlLE4vQSxOL0EsTi9BLE4vQSxmYWxzZSxOL0EsZmFsc2UsTi9B"
    data = base64.b64decode(test_hash)
    return data

def read_data(data):
    value = ''
    for i in csv.DictReader(data.split()):
        if i['password_last_changed'] == 'not_supported':
            continue
        if i['password_last_changed'] == 'N/A':
            continue

        fmt         = '%Y-%m-%dT%H:%M:%S+00:00'
        date        = i['password_last_changed']

        changed     = datetime.strptime(date, fmt)
        now         = datetime.now()

        diff        = now - changed
        diff_days   = diff.total_seconds()/3600/24
        expiration  = changed + timedelta(45)

        if diff_days >= 22:
            value = value + '{}\'s password WILL EXPIRE at {}.'.format(i['user'], expiration) + "\n"

    if value == '':
        value = 'There are no expiring passwords.'

    return value

if __name__ == "__main__":
    main()

def execute_me_lambda(event, context):
    out = main()
    return out
