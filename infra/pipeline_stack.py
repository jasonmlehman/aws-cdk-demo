#!/usr/bin/env python3
''' Pipeline stack '''

import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from aws_cdk import Environment, Tags
from infra.application_stage import PipelineAppStage
from aws_cdk.aws_codecommit import Repository

class PipelineStack(cdk.Stack):

    def __init__(self, scope: Construct,
                 construct_id: str, context: str,
                 stage: str,env_data: Environment, **kwargs) -> None:

        """
        Parameters
        ----------
        context: str
            a string value referencing the parent element in cdk.json for this stack
        stage: str
            string value defining the stage where infrastructure is deployed
        env_data: Environment
            environment specs for target deployment
        """

        super().__init__(scope, construct_id, **kwargs)

        context = dict(self.node.try_get_context(context))
        repo = Repository.from_repository_name(
            self, context["repo_name"],
            repository_name=context["repo_name"])
        source = CodePipelineSource.code_commit(repo, "master")
        pipeline = CodePipeline(self, "Pipeline", 
                        pipeline_name=context["pipeline_name"]+f"{stage}",
                        cross_account_keys=True,
                        synth=ShellStep("Synth", 
                            input=source,
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]))

        appstage = PipelineAppStage(self,
                f"DeployTo{stage}",
                stage,
                env=env_data)
        pipeline.add_stage(appstage)