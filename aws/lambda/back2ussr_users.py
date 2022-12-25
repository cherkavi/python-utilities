import boto3
import json

BUCKET_NAME = "technik-bucket-001"
BUCKET_ITEM = "index.html"


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    item_from_s3 = s3.Object(BUCKET_NAME, BUCKET_ITEM)
    data_from_s3 = item_from_s3.get()['Body'].read()
    # save to temporary 512Mb storage
    with open("/tmp/out.txt", "w") as output_file:
        output_file.write(data_from_s3.decode("utf-8"))

    return {
        'statusCode': 200,
        'data': json.dumps(str(data_from_s3))
    }
