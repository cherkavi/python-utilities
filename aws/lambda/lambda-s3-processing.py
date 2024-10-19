import csv
import json
import tempfile

# fieldnames = ("Column1","Column2","Column3")

def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    bucket_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    bucket_key_output = f"{bucket_key}.json"

    item_from_s3 = s3.Object(bucket_name, bucket_key)
    data_from_s3 = item_from_s3.get()['Body'].read()

    # save file to temp
    csv_file = tempfile.NamedTemporaryFile()    
    with open(csv_file.name, "w") as output:
        output.write(data_from_s3.decode("utf-8"))

    json_file = tempfile.NamedTemporaryFile()    
    # convert to JSON
    with open(csv_file.name, "r") as input:
        with open(json_file.name, "w") as output:
            reader = csv.DictReader( input)
            for row in reader:
                json.dump(row, jsonfile)
                output.write('\n')

    # save file - need to check 
    item_to_s3 = s3.Object(bucket_name, bucket_key_output)
    item_to_s3.upload_file(json_file.name)

    # Publish a simple message to the specified SNS topic
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:85442027:cherkavi',   
        Message=bucket_key_output,   
    )

    return {
        'statusCode': 200,
        'new_obj': json.dumps(bucket_key_output)
    }

