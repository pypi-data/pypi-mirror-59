"""
Main interface for apigatewayv2 service client

Usage::

    import boto3
    from mypy_boto3.apigatewayv2 import ApiGatewayV2Client

    session = boto3.Session()

    client: ApiGatewayV2Client = boto3.client("apigatewayv2")
    session_client: ApiGatewayV2Client = session.client("apigatewayv2")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_apigatewayv2.client as client_scope

# pylint: disable=import-self
import mypy_boto3_apigatewayv2.paginator as paginator_scope
from mypy_boto3_apigatewayv2.type_defs import (
    AccessLogSettingsTypeDef,
    CorsTypeDef,
    CreateApiMappingResponseTypeDef,
    CreateApiResponseTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateDomainNameResponseTypeDef,
    CreateIntegrationResponseResponseTypeDef,
    CreateIntegrationResultTypeDef,
    CreateModelResponseTypeDef,
    CreateRouteResponseResponseTypeDef,
    CreateRouteResultTypeDef,
    CreateStageResponseTypeDef,
    DomainNameConfigurationTypeDef,
    GetApiMappingResponseTypeDef,
    GetApiMappingsResponseTypeDef,
    GetApiResponseTypeDef,
    GetApisResponseTypeDef,
    GetAuthorizerResponseTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentResponseTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNameResponseTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponseResponseTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationResultTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelResponseTypeDef,
    GetModelTemplateResponseTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponseResponseTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRouteResultTypeDef,
    GetRoutesResponseTypeDef,
    GetStageResponseTypeDef,
    GetStagesResponseTypeDef,
    GetTagsResponseTypeDef,
    ImportApiResponseTypeDef,
    JWTConfigurationTypeDef,
    ParameterConstraintsTypeDef,
    ReimportApiResponseTypeDef,
    RouteSettingsTypeDef,
    UpdateApiMappingResponseTypeDef,
    UpdateApiResponseTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateDeploymentResponseTypeDef,
    UpdateDomainNameResponseTypeDef,
    UpdateIntegrationResponseResponseTypeDef,
    UpdateIntegrationResultTypeDef,
    UpdateModelResponseTypeDef,
    UpdateRouteResponseResponseTypeDef,
    UpdateRouteResultTypeDef,
    UpdateStageResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ApiGatewayV2Client",)


class ApiGatewayV2Client(BaseClient):
    """
    [ApiGatewayV2.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.can_paginate)
        """

    def create_api(
        self,
        Name: str,
        ProtocolType: Literal["WEBSOCKET", "HTTP"],
        ApiKeySelectionExpression: str = None,
        CorsConfiguration: CorsTypeDef = None,
        CredentialsArn: str = None,
        Description: str = None,
        DisableSchemaValidation: bool = None,
        RouteKey: str = None,
        RouteSelectionExpression: str = None,
        Tags: Dict[str, str] = None,
        Target: str = None,
        Version: str = None,
    ) -> CreateApiResponseTypeDef:
        """
        [Client.create_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_api)
        """

    def create_api_mapping(
        self, ApiId: str, DomainName: str, Stage: str, ApiMappingKey: str = None
    ) -> CreateApiMappingResponseTypeDef:
        """
        [Client.create_api_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_api_mapping)
        """

    def create_authorizer(
        self,
        ApiId: str,
        AuthorizerType: Literal["REQUEST", "JWT"],
        IdentitySource: List[str],
        Name: str,
        AuthorizerCredentialsArn: str = None,
        AuthorizerResultTtlInSeconds: int = None,
        AuthorizerUri: str = None,
        IdentityValidationExpression: str = None,
        JwtConfiguration: JWTConfigurationTypeDef = None,
    ) -> CreateAuthorizerResponseTypeDef:
        """
        [Client.create_authorizer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_authorizer)
        """

    def create_deployment(
        self, ApiId: str, Description: str = None, StageName: str = None
    ) -> CreateDeploymentResponseTypeDef:
        """
        [Client.create_deployment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_deployment)
        """

    def create_domain_name(
        self,
        DomainName: str,
        DomainNameConfigurations: List[DomainNameConfigurationTypeDef] = None,
        Tags: Dict[str, str] = None,
    ) -> CreateDomainNameResponseTypeDef:
        """
        [Client.create_domain_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_domain_name)
        """

    def create_integration(
        self,
        ApiId: str,
        IntegrationType: Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"],
        ConnectionId: str = None,
        ConnectionType: Literal["INTERNET", "VPC_LINK"] = None,
        ContentHandlingStrategy: Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"] = None,
        CredentialsArn: str = None,
        Description: str = None,
        IntegrationMethod: str = None,
        IntegrationUri: str = None,
        PassthroughBehavior: Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"] = None,
        PayloadFormatVersion: str = None,
        RequestParameters: Dict[str, str] = None,
        RequestTemplates: Dict[str, str] = None,
        TemplateSelectionExpression: str = None,
        TimeoutInMillis: int = None,
    ) -> CreateIntegrationResultTypeDef:
        """
        [Client.create_integration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_integration)
        """

    def create_integration_response(
        self,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseKey: str,
        ContentHandlingStrategy: Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"] = None,
        ResponseParameters: Dict[str, str] = None,
        ResponseTemplates: Dict[str, str] = None,
        TemplateSelectionExpression: str = None,
    ) -> CreateIntegrationResponseResponseTypeDef:
        """
        [Client.create_integration_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_integration_response)
        """

    def create_model(
        self, ApiId: str, Name: str, Schema: str, ContentType: str = None, Description: str = None
    ) -> CreateModelResponseTypeDef:
        """
        [Client.create_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_model)
        """

    def create_route(
        self,
        ApiId: str,
        RouteKey: str,
        ApiKeyRequired: bool = None,
        AuthorizationScopes: List[str] = None,
        AuthorizationType: Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"] = None,
        AuthorizerId: str = None,
        ModelSelectionExpression: str = None,
        OperationName: str = None,
        RequestModels: Dict[str, str] = None,
        RequestParameters: Dict[str, ParameterConstraintsTypeDef] = None,
        RouteResponseSelectionExpression: str = None,
        Target: str = None,
    ) -> CreateRouteResultTypeDef:
        """
        [Client.create_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_route)
        """

    def create_route_response(
        self,
        ApiId: str,
        RouteId: str,
        RouteResponseKey: str,
        ModelSelectionExpression: str = None,
        ResponseModels: Dict[str, str] = None,
        ResponseParameters: Dict[str, ParameterConstraintsTypeDef] = None,
    ) -> CreateRouteResponseResponseTypeDef:
        """
        [Client.create_route_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_route_response)
        """

    def create_stage(
        self,
        ApiId: str,
        StageName: str,
        AccessLogSettings: AccessLogSettingsTypeDef = None,
        AutoDeploy: bool = None,
        ClientCertificateId: str = None,
        DefaultRouteSettings: RouteSettingsTypeDef = None,
        DeploymentId: str = None,
        Description: str = None,
        RouteSettings: Dict[str, RouteSettingsTypeDef] = None,
        StageVariables: Dict[str, str] = None,
        Tags: Dict[str, str] = None,
    ) -> CreateStageResponseTypeDef:
        """
        [Client.create_stage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_stage)
        """

    def delete_api(self, ApiId: str) -> None:
        """
        [Client.delete_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_api)
        """

    def delete_api_mapping(self, ApiMappingId: str, DomainName: str) -> None:
        """
        [Client.delete_api_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_api_mapping)
        """

    def delete_authorizer(self, ApiId: str, AuthorizerId: str) -> None:
        """
        [Client.delete_authorizer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_authorizer)
        """

    def delete_cors_configuration(self, ApiId: str) -> None:
        """
        [Client.delete_cors_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_cors_configuration)
        """

    def delete_deployment(self, ApiId: str, DeploymentId: str) -> None:
        """
        [Client.delete_deployment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_deployment)
        """

    def delete_domain_name(self, DomainName: str) -> None:
        """
        [Client.delete_domain_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_domain_name)
        """

    def delete_integration(self, ApiId: str, IntegrationId: str) -> None:
        """
        [Client.delete_integration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_integration)
        """

    def delete_integration_response(
        self, ApiId: str, IntegrationId: str, IntegrationResponseId: str
    ) -> None:
        """
        [Client.delete_integration_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_integration_response)
        """

    def delete_model(self, ApiId: str, ModelId: str) -> None:
        """
        [Client.delete_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_model)
        """

    def delete_route(self, ApiId: str, RouteId: str) -> None:
        """
        [Client.delete_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route)
        """

    def delete_route_response(self, ApiId: str, RouteId: str, RouteResponseId: str) -> None:
        """
        [Client.delete_route_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route_response)
        """

    def delete_route_settings(self, ApiId: str, RouteKey: str, StageName: str) -> None:
        """
        [Client.delete_route_settings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_route_settings)
        """

    def delete_stage(self, ApiId: str, StageName: str) -> None:
        """
        [Client.delete_stage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.delete_stage)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.generate_presigned_url)
        """

    def get_api(self, ApiId: str) -> GetApiResponseTypeDef:
        """
        [Client.get_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api)
        """

    def get_api_mapping(self, ApiMappingId: str, DomainName: str) -> GetApiMappingResponseTypeDef:
        """
        [Client.get_api_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api_mapping)
        """

    def get_api_mappings(
        self, DomainName: str, MaxResults: str = None, NextToken: str = None
    ) -> GetApiMappingsResponseTypeDef:
        """
        [Client.get_api_mappings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_api_mappings)
        """

    def get_apis(self, MaxResults: str = None, NextToken: str = None) -> GetApisResponseTypeDef:
        """
        [Client.get_apis documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_apis)
        """

    def get_authorizer(self, ApiId: str, AuthorizerId: str) -> GetAuthorizerResponseTypeDef:
        """
        [Client.get_authorizer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_authorizer)
        """

    def get_authorizers(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetAuthorizersResponseTypeDef:
        """
        [Client.get_authorizers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_authorizers)
        """

    def get_deployment(self, ApiId: str, DeploymentId: str) -> GetDeploymentResponseTypeDef:
        """
        [Client.get_deployment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_deployment)
        """

    def get_deployments(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetDeploymentsResponseTypeDef:
        """
        [Client.get_deployments documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_deployments)
        """

    def get_domain_name(self, DomainName: str) -> GetDomainNameResponseTypeDef:
        """
        [Client.get_domain_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_domain_name)
        """

    def get_domain_names(
        self, MaxResults: str = None, NextToken: str = None
    ) -> GetDomainNamesResponseTypeDef:
        """
        [Client.get_domain_names documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_domain_names)
        """

    def get_integration(self, ApiId: str, IntegrationId: str) -> GetIntegrationResultTypeDef:
        """
        [Client.get_integration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration)
        """

    def get_integration_response(
        self, ApiId: str, IntegrationId: str, IntegrationResponseId: str
    ) -> GetIntegrationResponseResponseTypeDef:
        """
        [Client.get_integration_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration_response)
        """

    def get_integration_responses(
        self, ApiId: str, IntegrationId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetIntegrationResponsesResponseTypeDef:
        """
        [Client.get_integration_responses documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integration_responses)
        """

    def get_integrations(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetIntegrationsResponseTypeDef:
        """
        [Client.get_integrations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_integrations)
        """

    def get_model(self, ApiId: str, ModelId: str) -> GetModelResponseTypeDef:
        """
        [Client.get_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_model)
        """

    def get_model_template(self, ApiId: str, ModelId: str) -> GetModelTemplateResponseTypeDef:
        """
        [Client.get_model_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_model_template)
        """

    def get_models(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetModelsResponseTypeDef:
        """
        [Client.get_models documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_models)
        """

    def get_route(self, ApiId: str, RouteId: str) -> GetRouteResultTypeDef:
        """
        [Client.get_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route)
        """

    def get_route_response(
        self, ApiId: str, RouteId: str, RouteResponseId: str
    ) -> GetRouteResponseResponseTypeDef:
        """
        [Client.get_route_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route_response)
        """

    def get_route_responses(
        self, ApiId: str, RouteId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetRouteResponsesResponseTypeDef:
        """
        [Client.get_route_responses documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_route_responses)
        """

    def get_routes(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetRoutesResponseTypeDef:
        """
        [Client.get_routes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_routes)
        """

    def get_stage(self, ApiId: str, StageName: str) -> GetStageResponseTypeDef:
        """
        [Client.get_stage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_stage)
        """

    def get_stages(
        self, ApiId: str, MaxResults: str = None, NextToken: str = None
    ) -> GetStagesResponseTypeDef:
        """
        [Client.get_stages documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_stages)
        """

    def get_tags(self, ResourceArn: str) -> GetTagsResponseTypeDef:
        """
        [Client.get_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.get_tags)
        """

    def import_api(
        self, Body: str, Basepath: str = None, FailOnWarnings: bool = None
    ) -> ImportApiResponseTypeDef:
        """
        [Client.import_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.import_api)
        """

    def reimport_api(
        self, ApiId: str, Body: str, Basepath: str = None, FailOnWarnings: bool = None
    ) -> ReimportApiResponseTypeDef:
        """
        [Client.reimport_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.reimport_api)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str] = None) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.untag_resource)
        """

    def update_api(
        self,
        ApiId: str,
        ApiKeySelectionExpression: str = None,
        CorsConfiguration: CorsTypeDef = None,
        CredentialsArn: str = None,
        Description: str = None,
        DisableSchemaValidation: bool = None,
        Name: str = None,
        RouteKey: str = None,
        RouteSelectionExpression: str = None,
        Target: str = None,
        Version: str = None,
    ) -> UpdateApiResponseTypeDef:
        """
        [Client.update_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_api)
        """

    def update_api_mapping(
        self,
        ApiId: str,
        ApiMappingId: str,
        DomainName: str,
        ApiMappingKey: str = None,
        Stage: str = None,
    ) -> UpdateApiMappingResponseTypeDef:
        """
        [Client.update_api_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_api_mapping)
        """

    def update_authorizer(
        self,
        ApiId: str,
        AuthorizerId: str,
        AuthorizerCredentialsArn: str = None,
        AuthorizerResultTtlInSeconds: int = None,
        AuthorizerType: Literal["REQUEST", "JWT"] = None,
        AuthorizerUri: str = None,
        IdentitySource: List[str] = None,
        IdentityValidationExpression: str = None,
        JwtConfiguration: JWTConfigurationTypeDef = None,
        Name: str = None,
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        [Client.update_authorizer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_authorizer)
        """

    def update_deployment(
        self, ApiId: str, DeploymentId: str, Description: str = None
    ) -> UpdateDeploymentResponseTypeDef:
        """
        [Client.update_deployment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_deployment)
        """

    def update_domain_name(
        self, DomainName: str, DomainNameConfigurations: List[DomainNameConfigurationTypeDef] = None
    ) -> UpdateDomainNameResponseTypeDef:
        """
        [Client.update_domain_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_domain_name)
        """

    def update_integration(
        self,
        ApiId: str,
        IntegrationId: str,
        ConnectionId: str = None,
        ConnectionType: Literal["INTERNET", "VPC_LINK"] = None,
        ContentHandlingStrategy: Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"] = None,
        CredentialsArn: str = None,
        Description: str = None,
        IntegrationMethod: str = None,
        IntegrationType: Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"] = None,
        IntegrationUri: str = None,
        PassthroughBehavior: Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"] = None,
        PayloadFormatVersion: str = None,
        RequestParameters: Dict[str, str] = None,
        RequestTemplates: Dict[str, str] = None,
        TemplateSelectionExpression: str = None,
        TimeoutInMillis: int = None,
    ) -> UpdateIntegrationResultTypeDef:
        """
        [Client.update_integration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_integration)
        """

    def update_integration_response(
        self,
        ApiId: str,
        IntegrationId: str,
        IntegrationResponseId: str,
        ContentHandlingStrategy: Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"] = None,
        IntegrationResponseKey: str = None,
        ResponseParameters: Dict[str, str] = None,
        ResponseTemplates: Dict[str, str] = None,
        TemplateSelectionExpression: str = None,
    ) -> UpdateIntegrationResponseResponseTypeDef:
        """
        [Client.update_integration_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_integration_response)
        """

    def update_model(
        self,
        ApiId: str,
        ModelId: str,
        ContentType: str = None,
        Description: str = None,
        Name: str = None,
        Schema: str = None,
    ) -> UpdateModelResponseTypeDef:
        """
        [Client.update_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_model)
        """

    def update_route(
        self,
        ApiId: str,
        RouteId: str,
        ApiKeyRequired: bool = None,
        AuthorizationScopes: List[str] = None,
        AuthorizationType: Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"] = None,
        AuthorizerId: str = None,
        ModelSelectionExpression: str = None,
        OperationName: str = None,
        RequestModels: Dict[str, str] = None,
        RequestParameters: Dict[str, ParameterConstraintsTypeDef] = None,
        RouteKey: str = None,
        RouteResponseSelectionExpression: str = None,
        Target: str = None,
    ) -> UpdateRouteResultTypeDef:
        """
        [Client.update_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_route)
        """

    def update_route_response(
        self,
        ApiId: str,
        RouteId: str,
        RouteResponseId: str,
        ModelSelectionExpression: str = None,
        ResponseModels: Dict[str, str] = None,
        ResponseParameters: Dict[str, ParameterConstraintsTypeDef] = None,
        RouteResponseKey: str = None,
    ) -> UpdateRouteResponseResponseTypeDef:
        """
        [Client.update_route_response documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_route_response)
        """

    def update_stage(
        self,
        ApiId: str,
        StageName: str,
        AccessLogSettings: AccessLogSettingsTypeDef = None,
        AutoDeploy: bool = None,
        ClientCertificateId: str = None,
        DefaultRouteSettings: RouteSettingsTypeDef = None,
        DeploymentId: str = None,
        Description: str = None,
        RouteSettings: Dict[str, RouteSettingsTypeDef] = None,
        StageVariables: Dict[str, str] = None,
    ) -> UpdateStageResponseTypeDef:
        """
        [Client.update_stage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Client.update_stage)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_apis"]
    ) -> paginator_scope.GetApisPaginator:
        """
        [Paginator.GetApis documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_authorizers"]
    ) -> paginator_scope.GetAuthorizersPaginator:
        """
        [Paginator.GetAuthorizers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_deployments"]
    ) -> paginator_scope.GetDeploymentsPaginator:
        """
        [Paginator.GetDeployments documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_domain_names"]
    ) -> paginator_scope.GetDomainNamesPaginator:
        """
        [Paginator.GetDomainNames documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_integration_responses"]
    ) -> paginator_scope.GetIntegrationResponsesPaginator:
        """
        [Paginator.GetIntegrationResponses documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_integrations"]
    ) -> paginator_scope.GetIntegrationsPaginator:
        """
        [Paginator.GetIntegrations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_models"]
    ) -> paginator_scope.GetModelsPaginator:
        """
        [Paginator.GetModels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_route_responses"]
    ) -> paginator_scope.GetRouteResponsesPaginator:
        """
        [Paginator.GetRouteResponses documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_routes"]
    ) -> paginator_scope.GetRoutesPaginator:
        """
        [Paginator.GetRoutes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_stages"]
    ) -> paginator_scope.GetStagesPaginator:
        """
        [Paginator.GetStages documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages)
        """


class Exceptions:
    AccessDeniedException: Boto3ClientError
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    ConflictException: Boto3ClientError
    NotFoundException: Boto3ClientError
    TooManyRequestsException: Boto3ClientError
