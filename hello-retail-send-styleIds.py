import os
import boto3

SQS_CLIENT = boto3.client('sqs')

def lambda_handler(event, context):
    return(SQS_CLIENT.send_message(
        QueueUrl='',
        MessageBody='4912233'
    ))


