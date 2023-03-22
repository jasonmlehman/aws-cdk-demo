#!/usr/bin/env python3
''' APILambdaCognitoStack Stack '''

from aws_cdk.aws_apigateway import (AccessLogFormat, ApiKey, ConnectionType,
                                    EndpointConfiguration, EndpointType,
                                    IntegrationResponse, LambdaIntegration,
                                    LogGroupLogDestination, MethodLoggingLevel,
                                    MethodResponse, PassthroughBehavior,
                                    Resource, RestApi, StageOptions, UsagePlan,
                                    CognitoUserPoolsAuthorizer, AuthorizationType)
import aws_cdk as cdk
from aws_cdk import RemovalPolicy, Duration
from constructs import Construct
from aws_cdk.aws_lambda import Function, InlineCode, Runtime, Code, VersionOptions, Tracing
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.aws_logs import LogGroup
from infra.utilities import get_log_retention_days, get_removal_policy
from aws_cdk.aws_cognito import (UserPool, ResourceServerScope, OAuthSettings,
                                OAuthScope, OAuthFlows, CognitoDomainOptions)
from aws_cdk.aws_lambda import Function, InlineCode, Runtime, Code, VersionOptions, Tracing
from aws_cdk import aws_lambda as _lambda

class APILambdaCognitoStack(cdk.Stack):
    """
        This stack deploys an API Gateway, Lambda, and Cognito construct
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

        # Create the Cognito UserPool
        pool = UserPool(
                self,
                f"{context['app_name']}-user-pool",
                user_pool_name = f"{context['app_name']}-user-pool"
        )

        # Add the auth domain (token endpoint)
        pool.add_domain("CognitoDomain",
            cognito_domain=CognitoDomainOptions(
                domain_prefix=f"{context['Cognito_Domain_Name']}-{stage}"
            )
        )

        # Create the Resource Server and scopes
        read_only_scope = ResourceServerScope(scope_name="read", scope_description="Read-only access")
        full_access_scope = ResourceServerScope(scope_name="*", scope_description="Full access")

        # Create the Cognito Resource Server
        user_server = pool.add_resource_server("ResourceServer",
            identifier="rs",
            scopes=[read_only_scope, full_access_scope]
        )

        # Add the clients
        read_only_client = pool.add_client("read-only-client",
            user_pool_client_name = f"{context['app_name']}-read",
            generate_secret = True,
            o_auth=OAuthSettings(
                flows = OAuthFlows(
                      client_credentials = True
                  ),
                scopes=[OAuthScope.resource_server(user_server, read_only_scope)]
            )
        )

        full_access_client = pool.add_client("full-access-client",
            user_pool_client_name = f"{context['app_name']}-full",
            generate_secret = True,
            o_auth=OAuthSettings(
                flows = OAuthFlows(
                      client_credentials = True
                  ),
                scopes=[OAuthScope.resource_server(user_server, full_access_scope)]
            )
        )

        # Create the log group for API Gateway to log to cloudwatch
        log_group = LogGroup(
                self,
                f"{context['app_name']}-log-group",
                retention=get_log_retention_days(context["log_retention"]),
                removal_policy=get_removal_policy(context["log_removal_policy"])
        )

        apiconstruct = RestApi(
            self,
            f"{context['app_name']}-gateway",
            description=f"api gateway for {context['app_name']} ",
            endpoint_configuration=EndpointConfiguration(
                types=[EndpointType.REGIONAL]),
            deploy=True,
            deploy_options=StageOptions(
                data_trace_enabled=True,
                logging_level=MethodLoggingLevel.INFO,
                metrics_enabled=True,
                access_log_destination=LogGroupLogDestination(log_group),
                description="Stage for the api deployment",
                stage_name=stage,
                tracing_enabled=(context["enable_tracing"].lower() == "true")
            ),
            rest_api_name=f"{context['app_name']}-{stage}-gateway",
            cloud_watch_role=True
        )

        # Create the Cognito Authorizer
        auth = CognitoUserPoolsAuthorizer(
            self,
            f"{context['app_name']}-authorizer",
            authorizer_name = f"{context['app_name']}-authorizer",
            cognito_user_pools = [pool]
        )

        # Create the needed layer
        lambdaLayer = _lambda.LayerVersion(self, 'lambda-layer',
                  code = _lambda.Code.from_asset(context["lambda_zip"]),
                  compatible_runtimes = [_lambda.Runtime.PYTHON_3_8],
        )

        # Create the Lambda function
        lambda_function = Function(
            self,
            "Demo-py-Layer",
            function_name=f"{context['app_name']}-{stage}",
            runtime=Runtime.PYTHON_3_8,
            handler=context["lambda_handler"],
            code=Code.from_asset(context["lambda_code_pathv2"]),
            current_version_options=VersionOptions(
                removal_policy=RemovalPolicy.DESTROY,
                retry_attempts=0,
                description="context['app_name']}",
            ),
            timeout=Duration.seconds(60),
            memory_size=(128),
            tracing=Tracing.ACTIVE,
            retry_attempts=0,
            log_retention=RetentionDays.ONE_DAY,
            environment=context.get("common_env_vars", {}) | {
                "POWERTOOLS_SERVICE_NAME": "test"},
            layers = [lambdaLayer]
        )

        # Create the lambda integration
        lambda_integration = LambdaIntegration(
            handler=lambda_function,
            allow_test_invoke=True,
            proxy=True
        )

        # Create the methods
        apiconstruct.root.add_method("GET", lambda_integration,
            authorizer = auth,
            authorization_type=AuthorizationType.COGNITO,
            authorization_scopes=["rs/read"]
        )

        apiconstruct.root.add_method("POST", lambda_integration,
            authorizer = auth,
            authorization_type=AuthorizationType.COGNITO,
            authorization_scopes=["*"]
        )