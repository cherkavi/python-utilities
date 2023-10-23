import boto3
import json
import os
from datetime import datetime
from random import randrange

# Initialize S3 client
s3_client = boto3.client('s3')

# S3 bucket and file details
bucket_name = 'visitors'
file_name = 'request_data.txt'

def lambda_handler(event, context):
    # Extract user's IP from the event
    user_ip = event
    

    # Get the current time
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # get user name 
    query_params = event.get('queryStringParameters', {})

    # Access specific parameters by key
    bucket = query_params.get('name')
    
    if bucket is None or len(bucket.strip())==0:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'pls, specify name'})
        }

    file_name = f"{bucket}_{timestamp}_{str(randrange(100,999))}"    
    existing_data={'user_ip': user_ip, 'timestamp': timestamp, 'bucket': bucket}

    # Write the updated data back to S3
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(existing_data))
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'ok'})
    }

