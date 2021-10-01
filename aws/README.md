boto3 configuration
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

logging
```python
logging.getLogger('boto').setLevel(logging.WARNING)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

```
