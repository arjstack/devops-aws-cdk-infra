from typing import Dict
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)
from constructs import Construct
from configs.deployment_config import DeploymentConfig

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configs: DeploymentConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        vpc = self.__createVPC(configs.deployment_name, configs.app_parameters["vpc"])


    def __createVPC(self: Construct, deployment_name: str, vpc_configs: Dict) -> ec2.Vpc:
        vpc = ec2.Vpc(self, f'{deployment_name}-vpc',
                        vpc_name = f'{deployment_name}-vpc', 
                        ip_addresses = ec2.IpAddresses.cidr(vpc_configs["cidr"]),
                        enable_dns_hostnames = vpc_configs["enable_dns_hostnames"],
                        enable_dns_support = vpc_configs["enable_dns_support"])

        CfnOutput(self, "Output",
                       value=vpc.vpc_id)
        return vpc

