from typing import Dict, Union

import boto3


class BasicTagger:
    def __init__(
            self,
            account_id: str,
            vpc_id: str,
            credentials: Union[type(None), Dict],
            api_type: str = 'ec2',
            resource_type: str = 'instance',
            region: str = 'us-east-1'):
        self.region = region
        self.account_id = account_id
        self.vpc_id = vpc_id
        self.credentials = credentials
        self.api_type = api_type
        self.resource_type = resource_type
        self.client = boto3.client(api_type, region_name=region)

    def describe(self):
        return self.client.describe_instances()


if __name__ == "__main__":

    metadata = BasicTagger(
        account_id='835377776149',
        credentials={
            'aws_access_key_id': None,
            'aws_secret_access_key': None,
            'aws_session_token': None
        },
        vpc_id='nonexistent'
    ).describe()

    print(metadata)
