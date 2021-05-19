import json
from typing import Dict, Union

import boto3


class BasicTagger:
    ADDITIONAL_TAGS = {
        "Key": 'environment',
        "Value": 'stage'
    }

    def __repr__(self) -> str:
        return f"{super().__repr__()}: {self.__dict__}"

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

    def instances(self):
        # TODO: paginator with filter
        # TODO: filter example {"Filters": [{"Name": "vpc-id", "Values": ["vpc-f17ac095"]}]}
        aggr = []
        for instance in self.describe().get('Reservations')[0]['Instances']:
            aggr.append(instance)

        return aggr

    def add_additional_tags(self):
        for instance in self.instances():
            instance['Tags'].append(self.ADDITIONAL_TAGS)
            metadata = {instance['InstanceId']: instance['Tags']}
            print(metadata)

            return json.dumps(metadata, default=str)

    def update_tags(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_tags
        raise NotImplementedError


if __name__ == "__main__":
    tagger = BasicTagger(
        account_id='835377776149',
        credentials={
            'aws_access_key_id': None,
            'aws_secret_access_key': None,
            'aws_session_token': None
        },
        vpc_id='nonexistent'
    )
    print(tagger)
    tagger.add_additional_tags()
