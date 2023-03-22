#!/usr/bin/env python3
''' Application Stage '''

import aws_cdk as cdk
from constructs import Construct
from aws_cdk import Environment, Stage, Tags
from infra.lambda_stack import LambdaPyStack
from infra.lambda_stack import LambdaNodeStack
from infra.lambda_stack import LambdaLayerPyStackv1, LambdaLayerPyStackv2
from infra.s3_stack import S3Stack

import json

class PipelineAppStage(Stage):
    """
        This stage encapsulates the application stack ( Staticsite stack in this case)
        For any additional infrastructure, include them as additional stacks.
    """

    def __init__(self, scope: Construct, construct_id: str,
                 stage: str, env: Environment, **kwargs):
        """
            Attributes
            =========
            stage: str
                   The stage is a reference to the aws environment
            env: Environment
                 The environment is a json object that consists of an account id and a region
        """
        super().__init__(scope, construct_id, **kwargs)
        lambdacontext = dict(self.node.try_get_context("lambda"))
        s3context = dict(self.node.try_get_context("s3"))

        LambdaNodeStack(
            self,
            f"{construct_id}-lambda-Node",
            lambdacontext,
            stage,
            env=env)

        LambdaPyStack(
            self,
            f"{construct_id}-lambda-Py",
            lambdacontext,
            stage,
            env=env)

        LambdaLayerPyStackv1(
            self,
            f"{construct_id}-lambda-LayerPyv1",
            lambdacontext,
            stage,
            env=env)

        LambdaLayerPyStackv2(
            self,
            f"{construct_id}-lambda-LayerPyv2",
            lambdacontext,
            stage,
            env=env)

        S3Stack(
            self,
            f"{construct_id}-S3",
            s3context,
            stage,
            env=env)

        with open( './tags.json', 'r') as file:
            tags = json.loads(file.read())

        for key, value in tags.items():
            Tags.of(self).add(key, value)

        Tags.of(self).add("Environment", stage)