#!/usr/bin/env python3
import json
import aws_cdk as cdk
from cdk_infra.infra_stack import InfraStack
from configs.deployment_config import DeploymentConfig

app = cdk.App()
app_configs = json.load(open("configs/app_configs.json"))

app_name = app.node.try_get_context("app_name")
env_name = app.node.try_get_context("environment")
env_configs = app.node.try_get_context(env_name)

aws_account_id=env_configs["account_id"]
aws_region=env_configs["aws_region"]
app_env = cdk.Environment(account=aws_account_id, region =aws_region)

app_parameters = app_configs[env_name]

configs = DeploymentConfig(app_name, env_name, app_parameters)

InfraStack(app, "InfraStack", configs=configs, env=app_env)

app.synth()