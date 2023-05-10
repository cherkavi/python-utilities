import pulumi
import pulumi_aws as aws

"""
```sh
export AWS_ACCESS_KEY_ID=`aws configure get aws_access_key_id`
export AWS_SECRET_ACCESS_KEY=`aws configure get aws_secret_access_key`
export AWS_SESSION_TOKEN=`aws configure get aws_session_token`
# todo: maybe pulumi doesn't work with AWS_SESSION_TOKEN

### write your code in __main__.py
pulumi up
```

https://www.pulumi.com/registry/packages/aws/api-docs/ec2/vpc/
"""

main = aws.ec2.Vpc("second_vpc", cidr_block="10.0.0.0/16")
print(main)

