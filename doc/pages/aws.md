# aws

## dynamodb

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/dynamodb.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/dynamodb.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## lambda code

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/lambda-code.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/lambda-code.py -->
```py
import json

def lambda_handler(event, context):
    body = "data from lambda"
    statusCode = 200
    return {
        "statusCode": statusCode,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## lambda sns

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/lambda-sns.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/lambda-sns.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## s3 external

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/s3-external.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/s3-external.py -->
```py
class AwsS3Storage(Storage):

    def __init__(self, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                 region_name=settings.AWS_REGION,
                 bucket_name=settings.AWS_S3_BUCKET_NAME):
        self._session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                              aws_secret_access_key=aws_secret_access_key,
                                              region_name=region_name)
        self._bucket_name = bucket_name
        self._s3_client: BaseClient = self._session.client(service_name="s3")

    def save(self, object_path_in_storage: Path, absolute_path_to_file: str) -> bool:
        try:
            response = self._s3_client.upload_file(absolute_path_to_file, self._bucket_name, "/".join(
                Path(settings.IMAGE_STORAGE_FOLDER).joinpath(object_path_in_storage).parts))
            log.info(f"upload file result: {response}")
            return True
        except ClientError as e:
            log.info(f"exception during upload file : {e.response['Error']['Code']}")
            return False
        except Boto3Error as e:
            log.info(f"exception during file uploading : {e.args}")
            return False

    def load(self, object_path_in_storage: Path, absolute_path_to_file: Path) -> bool:
        try:
            response = self._s3_client.download_file(self._bucket_name, "/".join(
                Path(settings.IMAGE_STORAGE_FOLDER).joinpath(object_path_in_storage).parts),
                                                     str(absolute_path_to_file.resolve()))
            log.info(f"download file result: {response}")
            return True
        except ClientError as e:
            log.info(f"exception during file download : {e.response['Error']['Code']}")
            return False
        except Boto3Error as e:
            log.info(f"exception during file downloading : {e.args}")
            return False


    #             result = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix="", Delimiter="/")
    # [obj["Key"] for obj in result['Contents']]
    def is_exist(self, object_path_in_storage: Path) -> bool:
        try:
            return self._s3_client.head_object(Bucket=self._bucket_name, Key="/".join(
                Path(settings.IMAGE_STORAGE_FOLDER).joinpath(object_path_in_storage).parts))
        except ClientError as e:
            log.info(f"exception during checking existence of file : {e.response['Error']['Code']}")
            return False
        except Boto3Error as e:
            log.info(f"exception during checking of file : {e.args}")
            return False

    def delete(self, object_path_in_storage: Path) -> bool:
        try:
            response = self._s3_client.list_objects(Bucket=self._bucket_name, Prefix="/".join(
                Path(settings.IMAGE_STORAGE_FOLDER).joinpath(object_path_in_storage).parts))
            if "Contents" not in response:
                return False
            for key in response["Contents"]:
                self._s3_client.delete_object(Bucket=self._bucket_name, Key=key["Key"])
            return True
        except [BaseException, KeyError] as e:
            log.info(f"exception during delete file : {e.response['Error']['Code']}")
            return False
        except Boto3Error as e:
            log.info(f"exception during file removing : {e.args}")
            return False
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## s3 read files

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/s3-read-files.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/s3-read-files.py -->
```py
    def file_names(self) -> Set[str]:
        is_truncated: bool = True
        token: Optional[str] = None

        list_of_files: Set[str] = set()
        while is_truncated:
            try:
                if token:
                    result = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix="", Delimiter="/",
                                                             ContinuationToken=token)
                else:
                    result = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix="", Delimiter="/")
            except ClientError as e:
                raise S3BucketException("can't retrieve list of files on S3")
            except Exception as e:
                raise S3BucketException("can't understand answer list of files on S3")

            is_truncated = result['IsTruncated'] if 'IsTruncated' in result else False
            token = result['NextContinuationToken'] if 'NextContinuationToken' in result else None
            for each_file in [obj["Key"] for obj in result['Contents'] if not str(obj["Key"]).endswith("_response")]:
                list_of_files.add(each_file)
        return list_of_files
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## s3 snapshot

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/s3-snapshot.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/s3-snapshot.py -->
```py
    def _read_from_storage(self, filename: str, version_id: str = None) -> Dict:
        file_with_content = self._path_to_temp_file(filename)
        try:
            # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/s3.html#S3.Bucket.download_file
            # e2fyi.utils.aws.s3.ALLOWED_DOWNLOAD_ARGS
            if version_id:
                response = self._s3_client.download_file(self._bucket_name, filename, file_with_content,
                                                         ExtraArgs={"VersionId": version_id})
            else:
                response = self._s3_client.download_file(self._bucket_name, filename, file_with_content)
            self._log.info(f"download file result: {response}")
        except ClientError as e:
            self._log.info(f"exception during file download : {e.response['Error']['Code']}")
            raise StorageException(f"read file from S3 exception: {e}")
        except Boto3Error as e:
            self._log.info(f"exception during file downloading : {e.args}")
            raise StorageException(f"can't read file from S3: {e}")

        with open(file_with_content, "r") as f:
            return_value: Dict = json.loads("".join(f.readlines()).encode("utf-8"))
        self._remove_temp_file(file_with_content)
        return return_value

    def read_from_storage(self, filename: str) -> Dict:
        return self._read_from_storage(filename)

    def read_from_storage_previous_version(self, filename: str) -> Dict:
        resp = self._s3_client.list_object_versions(Bucket=self._bucket_name, Prefix=filename)
        versions = sorted(list(filter(lambda x: x["Key"] == filename, resp['Versions'])),
                          key=lambda x: x.get("LastModified"), reverse=True)

        if len(versions) > 1:
            return {}
        else:
            return self._read_from_storage(filename, versions[1]["VersionId"])

        # for obj in to_delete:
        #     print(client.delete_object(Bucket=bucket, Key=obj['Key'], VersionId=obj['VersionId']))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## s3

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/s3.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/s3.py -->
```py
import boto3
import json

BUCKET_NAME = "tk-bt-001"
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssm

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/aws/ssm.py) -->
<!-- The below code snippet is automatically added from ../../python/aws/ssm.py -->
```py
import json
import boto3
import os

ssm = boto3.client('ssm', region_name="eu-west-3")
dev_or_prod = os.environ['DEV_OR_PROD']

def lambda_handler(event, context):
    db_url = ssm.get_parameters(Names=["/my-app/" + dev_or_prod + "/db-url"])
    print(db_url)   
    db_password = ssm.get_parameters(Names=["/my-app/" + dev_or_prod + "/db-password"], WithDecryption=True)
    print(db_password)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


