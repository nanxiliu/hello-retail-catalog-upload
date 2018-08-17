import os
import boto3

SQS_CLIENT = boto3.client('sqs')

def lambda_handler(event, context):
    # Replace the txt file with your appropriate file with styleIds
    with open("styleIds.txt", "r") as file:
        for line in file:
            # Skip the line if it's empty
            if line.strip() == "":
                continue
            # Ensure there's no leading or trailing spaces
            styleId = str(line).strip()
            # Replace with correct queue url
            SQS_CLIENT.send_message(
                QueueUrl='',
                MessageBody= styleId
            )
    return ''
<<<<<<< HEAD


=======
>>>>>>> 44fc9fbfc7dc389c500471af2b6c2ec17a35e6b5
