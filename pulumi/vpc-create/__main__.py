"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

main = aws.ec2.Vpc("second_vpc", cidr_block="10.0.0.0/16")
print(main)
