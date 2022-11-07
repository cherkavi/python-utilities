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

