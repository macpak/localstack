# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)
from localstack.utils.objects import keys_to_lower


class ApiGatewayDomainNameProperties(TypedDict):
    CertificateArn: Optional[str]
    DistributionDomainName: Optional[str]
    DistributionHostedZoneId: Optional[str]
    DomainName: Optional[str]
    EndpointConfiguration: Optional[EndpointConfiguration]
    MutualTlsAuthentication: Optional[MutualTlsAuthentication]
    OwnershipVerificationCertificateArn: Optional[str]
    RegionalCertificateArn: Optional[str]
    RegionalDomainName: Optional[str]
    RegionalHostedZoneId: Optional[str]
    SecurityPolicy: Optional[str]
    Tags: Optional[list[Tag]]


class EndpointConfiguration(TypedDict):
    Types: Optional[list[str]]


class MutualTlsAuthentication(TypedDict):
    TruststoreUri: Optional[str]
    TruststoreVersion: Optional[str]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class ApiGatewayDomainNameProvider(ResourceProvider[ApiGatewayDomainNameProperties]):
    TYPE = "AWS::ApiGateway::DomainName"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[ApiGatewayDomainNameProperties],
    ) -> ProgressEvent[ApiGatewayDomainNameProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/DomainName

        Create-only properties:
          - /properties/DomainName

        Read-only properties:
          - /properties/RegionalHostedZoneId
          - /properties/DistributionDomainName
          - /properties/RegionalDomainName
          - /properties/DistributionHostedZoneId

        IAM permissions required:
          - apigateway:*

        """
        model = request.desired_state
        apigw = request.aws_client_factory.apigateway

        params = keys_to_lower(model.copy())
        param_names = [
            "certificateArn",
            "domainName",
            "endpointConfiguration",
            "mutualTlsAuthentication",
            "ownershipVerificationCertificateArn",
            "regionalCertificateArn",
            "securityPolicy",
        ]
        params = util.select_attributes(params, param_names)
        if model.get("Tags"):
            params["tags"] = {tag["key"]: tag["value"] for tag in model["Tags"]}

        result = apigw.create_domain_name(**params)

        hosted_zones = request.aws_client_factory.route53.list_hosted_zones()
        """
        The hardcoded value is the only one that should be returned but due limitations it is not possible to
        use it.
        """
        if hosted_zones["HostedZones"]:
            model["DistributionHostedZoneId"] = hosted_zones["HostedZones"][0]["Id"]
        else:
            model["DistributionHostedZoneId"] = "Z2FDTNDATAQYW2"

        model["DistributionDomainName"] = result.get("distributionDomainName") or result.get(
            "domainName"
        )
        model["RegionalDomainName"] = (
            result.get("regionalDomainName") or model["DistributionDomainName"]
        )
        model["RegionalHostedZoneId"] = (
            result.get("regionalHostedZoneId") or model["DistributionHostedZoneId"]
        )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[ApiGatewayDomainNameProperties],
    ) -> ProgressEvent[ApiGatewayDomainNameProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - apigateway:*
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[ApiGatewayDomainNameProperties],
    ) -> ProgressEvent[ApiGatewayDomainNameProperties]:
        """
        Delete a resource

        IAM permissions required:
          - apigateway:*
        """
        model = request.desired_state
        apigw = request.aws_client_factory.apigateway

        apigw.delete_domain_name(domainName=model["DomainName"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[ApiGatewayDomainNameProperties],
    ) -> ProgressEvent[ApiGatewayDomainNameProperties]:
        """
        Update a resource

        IAM permissions required:
          - apigateway:*
        """
        raise NotImplementedError
