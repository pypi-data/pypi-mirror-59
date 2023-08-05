# CDK IAM Generator

[AWS CDK](https://aws.amazon.com/cdk/) construct helps create IAM Managed Policies and IAM Roles using JSON Configuration

This package is written in TypeScript and made available via [JSII](https://github.com/aws/jsii) to all other supported languages. Package are available on:

* [npm](https://www.npmjs.com/package/cdk-iamgenerator)
* [PyPI] Work in Progress.
* [GitHub packages for Java][Maven] Work in Progress.

## Quickstart

Install or update from npm

TypeScript/Javascript

```console
npm i cdk-iamgenerator

```

## Usage

** TypeScript **

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from cdk_iam_generator import IamPolicyGenerator, IamRoleGenerator

IamPolicyGenerator(self, "IamPolicyGenerator",
    config_path="config/iam_generator_config.json",
    policy_path="config/policy"
)

IamRoleGenerator(self, "IamRoleGenerator",
    config_path="config/iam_generator_config.json"
)
```

## Prerequsites

Example: Place all the Policy Json files inside config/policy in your project root and policy file would look something like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codecommit:CancelUploadArchive",
        "codecommit:UploadArchive"
      ],
      "Resource": "*"
    }
  ]
}
```

Configure the policies and roles to be created in config/iam_generator_config.json file and would look something like this:

```json
{
    "policies": [
        {
            "policy_name": "CodeCommitArchive",
            "description": "CodeCommitArchive policy",
            "policy_file": "CodeCommitArchive.json"
        },
        {
            "policy_name": "KMSPolicy",
            "description": "KMSPolicy policy",
            "policy_file": "KMSPolicy.json"
        },
        {
            "policy_name": "CreateServiceLinkedRoleECS",
            "description": "CreateServiceLinkedRoleECS policy",
            "policy_file": "CreateServiceLinkedRoleECS.json"
        },
        {
            "policy_name": "DeployService1",
            "description": "DeployService1 policy",
            "policy_file": "DeployService1.json"
        },
        {
            "policy_name": "DeployService2",
            "description": "DeployService2 policy",
            "policy_file": "DeployService2.json"
        }
    ],
    "roles": [
        {
            "role_name": "TestRole1",
            "trust_service_principal": ["apigateway.amazonaws.com","lambda.amazonaws.com"],
            "customer_managed_policies": ["DeployService1","DeployService2","KMSPolicy"],
            "aws_managed_policies": ["service-role/AmazonAPIGatewayPushToCloudWatchLogs"]
        },
        {
            "role_name": "TestRole2",
            "trust_service_principal": ["sns.amazonaws.com"],
            "trust_account_principal": ["748669239283"],
            "customer_managed_policies": ["CreateServiceLinkedRoleECS","CodeCommitArchive","KMSPolicy"],
            "aws_managed_policies": ["service-role/AmazonAPIGatewayPushToCloudWatchLogs"]
        },
        {
            "role_name": "TestRole3",
            "trust_service_principal": ["ec2.amazonaws.com","sns.amazonaws.com"],
            "trust_account_principal": ["748669239283"],
            "customer_managed_policies": ["DeployService2","CodeCommitArchive","KMSPolicy"],
            "aws_managed_policies": ["AWSLambdaFullAccess"]
        }

    ]
}
```

## License

cdk-iamgenerator is distributed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

See [LICENSE](./LICENSE) for more information.
