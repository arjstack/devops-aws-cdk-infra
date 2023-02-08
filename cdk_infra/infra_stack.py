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
        subnets_map = self.__createSubnets(configs.deployment_name, vpc.vpc_id, configs.app_parameters["subnets"])
        print(subnets_map)

    def __createVPC(self: Construct, deployment_name: str, vpc_configs: Dict) -> ec2.Vpc:
        vpc = ec2.Vpc(self, f'{deployment_name}-vpc',
                        vpc_name = f'{deployment_name}-vpc', 
                        ip_addresses = ec2.IpAddresses.cidr(vpc_configs["cidr"]),
                        enable_dns_hostnames = vpc_configs["enable_dns_hostnames"],
                        enable_dns_support = vpc_configs["enable_dns_support"],
                        subnet_configuration = [])
        CfnOutput(self, "Output",
                       value=vpc.vpc_id)
        return vpc

    def __createSubnets(self: Construct, deployment_name: str, vpc_id: str, subnet_configs: Dict):

        public_subnets_configs = subnet_configs["public"]
        private_subnets_configs = subnet_configs["private"]
        subnets_map = {}

        for subnet_config in public_subnets_configs:

            subnet = ec2.PublicSubnet(self, f'{deployment_name}-{subnet_config["name"]}',
                                availability_zone=subnet_config["availability_zone"],
                                cidr_block=subnet_config["cidr_block"],
                                vpc_id=vpc_id,
                                map_public_ip_on_launch=True
                            )
            subnets_map[subnet_config["name"]] = subnet.subnet_id
        
        for subnet_config in private_subnets_configs:

            subnet = ec2.PrivateSubnet(self, f'{deployment_name}-{subnet_config["name"]}',
                                availability_zone=subnet_config["availability_zone"],
                                cidr_block=subnet_config["cidr_block"],
                                vpc_id=vpc_id,
                                map_public_ip_on_launch=False
                            )
            subnets_map[subnet_config["name"]] = subnet.subnet_id
        
        return subnets_map