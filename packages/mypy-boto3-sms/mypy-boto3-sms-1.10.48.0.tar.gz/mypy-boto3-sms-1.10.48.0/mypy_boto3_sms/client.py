"""
Main interface for sms service client

Usage::

    import boto3
    from mypy_boto3.sms import SMSClient

    session = boto3.Session()

    client: SMSClient = boto3.client("sms")
    session_client: SMSClient = session.client("sms")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

from datetime import datetime
import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_sms.client as client_scope

# pylint: disable=import-self
import mypy_boto3_sms.paginator as paginator_scope
from mypy_boto3_sms.type_defs import (
    CreateAppResponseTypeDef,
    CreateReplicationJobResponseTypeDef,
    GenerateChangeSetResponseTypeDef,
    GenerateTemplateResponseTypeDef,
    GetAppLaunchConfigurationResponseTypeDef,
    GetAppReplicationConfigurationResponseTypeDef,
    GetAppResponseTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersResponseTypeDef,
    ListAppsResponseTypeDef,
    ServerGroupLaunchConfigurationTypeDef,
    ServerGroupReplicationConfigurationTypeDef,
    ServerGroupTypeDef,
    StartOnDemandReplicationRunResponseTypeDef,
    TagTypeDef,
    UpdateAppResponseTypeDef,
    VmServerAddressTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SMSClient",)


class SMSClient(BaseClient):
    """
    [SMS.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.can_paginate)
        """

    def create_app(
        self,
        name: str = None,
        description: str = None,
        roleName: str = None,
        clientToken: str = None,
        serverGroups: List[ServerGroupTypeDef] = None,
        tags: List[TagTypeDef] = None,
    ) -> CreateAppResponseTypeDef:
        """
        [Client.create_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.create_app)
        """

    def create_replication_job(
        self,
        serverId: str,
        seedReplicationTime: datetime,
        frequency: int = None,
        runOnce: bool = None,
        licenseType: Literal["AWS", "BYOL"] = None,
        roleName: str = None,
        description: str = None,
        numberOfRecentAmisToKeep: int = None,
        encrypted: bool = None,
        kmsKeyId: str = None,
    ) -> CreateReplicationJobResponseTypeDef:
        """
        [Client.create_replication_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.create_replication_job)
        """

    def delete_app(
        self,
        appId: str = None,
        forceStopAppReplication: bool = None,
        forceTerminateApp: bool = None,
    ) -> Dict[str, Any]:
        """
        [Client.delete_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.delete_app)
        """

    def delete_app_launch_configuration(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.delete_app_launch_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.delete_app_launch_configuration)
        """

    def delete_app_replication_configuration(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.delete_app_replication_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.delete_app_replication_configuration)
        """

    def delete_replication_job(self, replicationJobId: str) -> Dict[str, Any]:
        """
        [Client.delete_replication_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.delete_replication_job)
        """

    def delete_server_catalog(self) -> Dict[str, Any]:
        """
        [Client.delete_server_catalog documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.delete_server_catalog)
        """

    def disassociate_connector(self, connectorId: str) -> Dict[str, Any]:
        """
        [Client.disassociate_connector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.disassociate_connector)
        """

    def generate_change_set(
        self, appId: str = None, changesetFormat: Literal["JSON", "YAML"] = None
    ) -> GenerateChangeSetResponseTypeDef:
        """
        [Client.generate_change_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.generate_change_set)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.generate_presigned_url)
        """

    def generate_template(
        self, appId: str = None, templateFormat: Literal["JSON", "YAML"] = None
    ) -> GenerateTemplateResponseTypeDef:
        """
        [Client.generate_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.generate_template)
        """

    def get_app(self, appId: str = None) -> GetAppResponseTypeDef:
        """
        [Client.get_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_app)
        """

    def get_app_launch_configuration(
        self, appId: str = None
    ) -> GetAppLaunchConfigurationResponseTypeDef:
        """
        [Client.get_app_launch_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_app_launch_configuration)
        """

    def get_app_replication_configuration(
        self, appId: str = None
    ) -> GetAppReplicationConfigurationResponseTypeDef:
        """
        [Client.get_app_replication_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_app_replication_configuration)
        """

    def get_connectors(
        self, nextToken: str = None, maxResults: int = None
    ) -> GetConnectorsResponseTypeDef:
        """
        [Client.get_connectors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_connectors)
        """

    def get_replication_jobs(
        self, replicationJobId: str = None, nextToken: str = None, maxResults: int = None
    ) -> GetReplicationJobsResponseTypeDef:
        """
        [Client.get_replication_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_replication_jobs)
        """

    def get_replication_runs(
        self, replicationJobId: str, nextToken: str = None, maxResults: int = None
    ) -> GetReplicationRunsResponseTypeDef:
        """
        [Client.get_replication_runs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_replication_runs)
        """

    def get_servers(
        self,
        nextToken: str = None,
        maxResults: int = None,
        vmServerAddressList: List[VmServerAddressTypeDef] = None,
    ) -> GetServersResponseTypeDef:
        """
        [Client.get_servers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.get_servers)
        """

    def import_server_catalog(self) -> Dict[str, Any]:
        """
        [Client.import_server_catalog documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.import_server_catalog)
        """

    def launch_app(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.launch_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.launch_app)
        """

    def list_apps(
        self, appIds: List[str] = None, nextToken: str = None, maxResults: int = None
    ) -> ListAppsResponseTypeDef:
        """
        [Client.list_apps documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.list_apps)
        """

    def put_app_launch_configuration(
        self,
        appId: str = None,
        roleName: str = None,
        serverGroupLaunchConfigurations: List[ServerGroupLaunchConfigurationTypeDef] = None,
    ) -> Dict[str, Any]:
        """
        [Client.put_app_launch_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.put_app_launch_configuration)
        """

    def put_app_replication_configuration(
        self,
        appId: str = None,
        serverGroupReplicationConfigurations: List[
            ServerGroupReplicationConfigurationTypeDef
        ] = None,
    ) -> Dict[str, Any]:
        """
        [Client.put_app_replication_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.put_app_replication_configuration)
        """

    def start_app_replication(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.start_app_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.start_app_replication)
        """

    def start_on_demand_replication_run(
        self, replicationJobId: str, description: str = None
    ) -> StartOnDemandReplicationRunResponseTypeDef:
        """
        [Client.start_on_demand_replication_run documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.start_on_demand_replication_run)
        """

    def stop_app_replication(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.stop_app_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.stop_app_replication)
        """

    def terminate_app(self, appId: str = None) -> Dict[str, Any]:
        """
        [Client.terminate_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.terminate_app)
        """

    def update_app(
        self,
        appId: str = None,
        name: str = None,
        description: str = None,
        roleName: str = None,
        serverGroups: List[ServerGroupTypeDef] = None,
        tags: List[TagTypeDef] = None,
    ) -> UpdateAppResponseTypeDef:
        """
        [Client.update_app documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.update_app)
        """

    def update_replication_job(
        self,
        replicationJobId: str,
        frequency: int = None,
        nextReplicationRunStartTime: datetime = None,
        licenseType: Literal["AWS", "BYOL"] = None,
        roleName: str = None,
        description: str = None,
        numberOfRecentAmisToKeep: int = None,
        encrypted: bool = None,
        kmsKeyId: str = None,
    ) -> Dict[str, Any]:
        """
        [Client.update_replication_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Client.update_replication_job)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_connectors"]
    ) -> paginator_scope.GetConnectorsPaginator:
        """
        [Paginator.GetConnectors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Paginator.GetConnectors)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_replication_jobs"]
    ) -> paginator_scope.GetReplicationJobsPaginator:
        """
        [Paginator.GetReplicationJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Paginator.GetReplicationJobs)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_replication_runs"]
    ) -> paginator_scope.GetReplicationRunsPaginator:
        """
        [Paginator.GetReplicationRuns documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Paginator.GetReplicationRuns)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_servers"]
    ) -> paginator_scope.GetServersPaginator:
        """
        [Paginator.GetServers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Paginator.GetServers)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_apps"]
    ) -> paginator_scope.ListAppsPaginator:
        """
        [Paginator.ListApps documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sms.html#SMS.Paginator.ListApps)
        """


class Exceptions:
    ClientError: Boto3ClientError
    InternalError: Boto3ClientError
    InvalidParameterException: Boto3ClientError
    MissingRequiredParameterException: Boto3ClientError
    NoConnectorsAvailableException: Boto3ClientError
    OperationNotPermittedException: Boto3ClientError
    ReplicationJobAlreadyExistsException: Boto3ClientError
    ReplicationJobNotFoundException: Boto3ClientError
    ReplicationRunLimitExceededException: Boto3ClientError
    ServerCannotBeReplicatedException: Boto3ClientError
    TemporarilyUnavailableException: Boto3ClientError
    UnauthorizedOperationException: Boto3ClientError
