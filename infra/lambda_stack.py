#!/usr/bin/env python3
''' Lambda Stack '''

import aws_cdk as cdk
from aws_cdk import RemovalPolicy, Duration
from constructs import Construct
from aws_cdk.aws_lambda import Function, InlineCode, Runtime, Code, VersionOptions, Tracing
from aws_cdk.aws_logs import RetentionDays

class LambdaNodeStack(cdk.Stack):
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

        Function(self, "LambdaFunction", 
            function_name=f"node-lambda-{stage}",
            runtime=Runtime.NODEJS_12_X,
            handler="index.handler",
            code=InlineCode("exports.handler = _ => 'Hello, CDK';")
        )

class LambdaPyStack(cdk.Stack):
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

        Function(
            self,
            "Demo",
            function_name=f"Python-lambda-{stage}",
            runtime=Runtime.PYTHON_3_8,
            handler=context["lambda_handler"],
            code=Code.from_asset(context["lambda_path"]),
            current_version_options=VersionOptions(
                removal_policy=RemovalPolicy.DESTROY,
                retry_attempts=0,
                description="Demo-lambda",
            ),
            timeout=Duration.seconds(60),
            memory_size=(128),
            tracing=Tracing.ACTIVE,
            retry_attempts=0,
            log_retention=RetentionDays.ONE_DAY,
            environment=context.get("common_env_vars", {}) | {
                "POWERTOOLS_SERVICE_NAME": "test"}
        )
