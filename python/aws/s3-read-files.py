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

