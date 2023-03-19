#!/usr/bin/env python3
''' S3 Stack '''

import aws_cdk as cdk
from aws_cdk import RemovalPolicy, Duration
from constructs import Construct
from aws_cdk.aws_s3 import Bucket, BlockPublicAccess, BucketEncryption
from aws_cdk.aws_logs import RetentionDays

class S3Stack(cdk.Stack):
    """
        This stack deploys a lambda function
    """
    def __init__(self, scope: Construct, construct_id: str,
                 context: str, stage: str, **kwargs) -> None:
        """
            Attributes
            =========
            stage: str
                 The stage is a reference to the aws environment
        """
        super().__init__(scope, construct_id, **kwargs)

        # Get public access settings
        if context["block_public_access"].lower() == "false":
            block_public_access = BlockPublicAccess(
               block_public_acls=False,
               ignore_public_acls=False,
               block_public_policy=False,
               restrict_public_buckets=False
            )
        else:
            block_public_access = BlockPublicAccess.BLOCK_ALL
        
        Bucket(self, f"{context['bucket_name']}-{stage}",
            bucket_name=f"{context['bucket_name']}-{stage}",
            block_public_access=block_public_access,
            encryption=BucketEncryption.S3_MANAGED,
            enforce_ssl=context["enforce_ssl"].lower() == "true",
            versioned=context["versioned"].lower() == "true",
            removal_policy=RemovalPolicy.DESTROY,
            public_read_access=context["publicreadaccess"].lower() == "true"
        )
