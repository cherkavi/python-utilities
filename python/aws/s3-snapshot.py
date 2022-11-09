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

