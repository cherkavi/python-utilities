import settings

def check_mandatory_attributes(object_with_attributes, list_of_attributes: List[str]):
    for each_attribute in list_of_attributes:
        if getattr(object_with_attributes, each_attribute, None) is None:
            print(f"mandatory attribute should be present as ENV variable {each_attribute}")
            exit(1)

check_mandatory_attributes(settings, ["DATAAPI_BASE_URL","DATAAPI_API_KEY","DATAAPI_ACCOUNT_ID","DATAAPI_CONTEXT_ID","DATAAPI_CONTEXT","AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","AWS_REGION","AWS_S3_BUCKET_NAME","AIRFLOW_URL","AIRFLOW_USER","AIRFLOW_PASSWORD"])

