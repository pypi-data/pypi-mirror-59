# A CDK L3 Construct for a Secure Bucket

This is an AWS CDK L3 Construct used to demonstrate the development and publishing process with the AWS CDK.

Please refer to the blog post [here](https://www.matthewbonig.com/2020/01/11/creating-constructs) for more information.

## Usage

Just import and use it.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from secure_bucket import SecureBucket

class SandboxCdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags)

        SecureBucket(self, "myBucket")
```

## Encryption options

This is just a wrapper around an S3 Bucket and the [props](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html) are shared.

However, you cannot supply an `UNENCRYPTED` option for the `encryption` property. If you do, or don't set it at all, it will use the `BucketEncryption.KMS_MANAGED` value by default.

## License

[MIT License](https://opensource.org/licenses/MIT)
