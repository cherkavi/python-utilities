# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import json
import boto3

TABLE_NAME = "back2ussr-users"

# {"id": 10003, "id_value":  "cherkavi_value4"}
def lambda_handler_writer(event, context):
    print(event)
    dynamodb = boto3.resource("dynamodb")
    dynamodb_table = dynamodb.Table(TABLE_NAME)
    insert_result = dynamodb_table.put_item(Item=event)
    return {
        'statusCode': 200,
        'body': json.dumps(insert_result)
    }


def lambda_handler_reader(event, context):
    dynamodb = boto3.resource("dynamodb")
    dynamodb_table = dynamodb.Table(TABLE_NAME)
    search_criteria = dict()
    search_criteria["id"] = 10003
    result_data = dynamodb_table.get_item(Key=search_criteria).get("Item")
    result_metadata = dynamodb_table.get_item(Key=search_criteria).get("ResponseMetadata")

    return {
        'statusCode': 200,
        # don't use 'json.dumps'
        'data': result_data,
        'metaData': result_metadata
    }

