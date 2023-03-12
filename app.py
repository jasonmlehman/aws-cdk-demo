#!/usr/bin/env python3
''' App entry point '''

import json
from aws_cdk import Environment, Tags, App
from infra.pipeline_stack import PipelineStack

app = App()

platformaccount = app.node.try_get_context("platformaccount")
devaccount = app.node.try_get_context("devaccount")
pipeline = app.node.try_get_context("pipelinename")

ENV_CODE = Environment(account=platformaccount, region="us-east-1") # Platform account for Code Pipelines
ENV_DEV = Environment(account=devaccount, region="us-east-1") # dev account
#ENV_TEST = Environment(account=testaccount, region="us-east-1") # test account, add to CDK.json
#ENV_PROD = Environment(account=prodaccount, region="us-east-1") # prod account, add to CDK.json

app = App()

# Deploys a new pipeline into the Platform Account
PipelineStack(app, pipeline + "-dev","pipeline","dev",ENV_DEV, env=ENV_CODE)
#PipelineStack(app, pipeline + "-test","pipeline","test",ENV_TEST, env=ENV_CODE)
#PipelineStack(app, pipeline + "-prod",pipeline","prod",ENV_PROD, env=ENV_CODE)

with open('./tags.json', 'r', encoding="utf8") as file:
    tags = json.loads(file.read())

for key, value in tags.items():
    Tags.of(app).add(key, value)

app.synth()
