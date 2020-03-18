import json
from datetime import datetime
import boto3

def lambda_handler(event, context):
    # example of input message processing
    # message = json.loads(event['Records'][0]['Sns']['Message'])
    
    sns = boto3.client('sns')
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:85442027:cherkavi',   
        Message='Hello from boto3',   
    )
    
    
    return {
        'statusCode': 200,
        # str(datetime.now())
        'body': json.dumps(response)
    }
