"""
Main interface for kafka service client

Usage::

    import boto3
    from mypy_boto3.kafka import KafkaClient

    session = boto3.Session()

    client: KafkaClient = boto3.client("kafka")
    session_client: KafkaClient = session.client("kafka")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, IO, List, Union, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_kafka.client as client_scope

# pylint: disable=import-self
import mypy_boto3_kafka.paginator as paginator_scope
from mypy_boto3_kafka.type_defs import (
    BrokerEBSVolumeInfoTypeDef,
    BrokerNodeGroupInfoTypeDef,
    ClientAuthenticationTypeDef,
    ConfigurationInfoTypeDef,
    CreateClusterResponseTypeDef,
    CreateConfigurationResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DescribeClusterOperationResponseTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    EncryptionInfoTypeDef,
    GetBootstrapBrokersResponseTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClustersResponseTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsResponseTypeDef,
    ListNodesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OpenMonitoringInfoTypeDef,
    UpdateBrokerCountResponseTypeDef,
    UpdateBrokerStorageResponseTypeDef,
    UpdateClusterConfigurationResponseTypeDef,
    UpdateMonitoringResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KafkaClient",)


class KafkaClient(BaseClient):
    """
    [Kafka.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.can_paginate)
        """

    def create_cluster(
        self,
        BrokerNodeGroupInfo: BrokerNodeGroupInfoTypeDef,
        ClusterName: str,
        KafkaVersion: str,
        NumberOfBrokerNodes: int,
        ClientAuthentication: ClientAuthenticationTypeDef = None,
        ConfigurationInfo: ConfigurationInfoTypeDef = None,
        EncryptionInfo: EncryptionInfoTypeDef = None,
        EnhancedMonitoring: Literal["DEFAULT", "PER_BROKER", "PER_TOPIC_PER_BROKER"] = None,
        OpenMonitoring: OpenMonitoringInfoTypeDef = None,
        Tags: Dict[str, str] = None,
    ) -> CreateClusterResponseTypeDef:
        """
        [Client.create_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.create_cluster)
        """

    def create_configuration(
        self,
        KafkaVersions: List[str],
        Name: str,
        ServerProperties: Union[bytes, IO],
        Description: str = None,
    ) -> CreateConfigurationResponseTypeDef:
        """
        [Client.create_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.create_configuration)
        """

    def delete_cluster(
        self, ClusterArn: str, CurrentVersion: str = None
    ) -> DeleteClusterResponseTypeDef:
        """
        [Client.delete_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.delete_cluster)
        """

    def describe_cluster(self, ClusterArn: str) -> DescribeClusterResponseTypeDef:
        """
        [Client.describe_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.describe_cluster)
        """

    def describe_cluster_operation(
        self, ClusterOperationArn: str
    ) -> DescribeClusterOperationResponseTypeDef:
        """
        [Client.describe_cluster_operation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.describe_cluster_operation)
        """

    def describe_configuration(self, Arn: str) -> DescribeConfigurationResponseTypeDef:
        """
        [Client.describe_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.describe_configuration)
        """

    def describe_configuration_revision(
        self, Arn: str, Revision: int
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        [Client.describe_configuration_revision documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.describe_configuration_revision)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.generate_presigned_url)
        """

    def get_bootstrap_brokers(self, ClusterArn: str) -> GetBootstrapBrokersResponseTypeDef:
        """
        [Client.get_bootstrap_brokers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.get_bootstrap_brokers)
        """

    def list_cluster_operations(
        self, ClusterArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListClusterOperationsResponseTypeDef:
        """
        [Client.list_cluster_operations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_cluster_operations)
        """

    def list_clusters(
        self, ClusterNameFilter: str = None, MaxResults: int = None, NextToken: str = None
    ) -> ListClustersResponseTypeDef:
        """
        [Client.list_clusters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_clusters)
        """

    def list_configuration_revisions(
        self, Arn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        [Client.list_configuration_revisions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_configuration_revisions)
        """

    def list_configurations(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListConfigurationsResponseTypeDef:
        """
        [Client.list_configurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_configurations)
        """

    def list_nodes(
        self, ClusterArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListNodesResponseTypeDef:
        """
        [Client.list_nodes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_nodes)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.list_tags_for_resource)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.untag_resource)
        """

    def update_broker_count(
        self, ClusterArn: str, CurrentVersion: str, TargetNumberOfBrokerNodes: int
    ) -> UpdateBrokerCountResponseTypeDef:
        """
        [Client.update_broker_count documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.update_broker_count)
        """

    def update_broker_storage(
        self,
        ClusterArn: str,
        CurrentVersion: str,
        TargetBrokerEBSVolumeInfo: List[BrokerEBSVolumeInfoTypeDef],
    ) -> UpdateBrokerStorageResponseTypeDef:
        """
        [Client.update_broker_storage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.update_broker_storage)
        """

    def update_cluster_configuration(
        self, ClusterArn: str, ConfigurationInfo: ConfigurationInfoTypeDef, CurrentVersion: str
    ) -> UpdateClusterConfigurationResponseTypeDef:
        """
        [Client.update_cluster_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.update_cluster_configuration)
        """

    def update_monitoring(
        self,
        ClusterArn: str,
        CurrentVersion: str,
        EnhancedMonitoring: Literal["DEFAULT", "PER_BROKER", "PER_TOPIC_PER_BROKER"] = None,
        OpenMonitoring: OpenMonitoringInfoTypeDef = None,
    ) -> UpdateMonitoringResponseTypeDef:
        """
        [Client.update_monitoring documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Client.update_monitoring)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_operations"]
    ) -> paginator_scope.ListClusterOperationsPaginator:
        """
        [Paginator.ListClusterOperations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Paginator.ListClusterOperations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_clusters"]
    ) -> paginator_scope.ListClustersPaginator:
        """
        [Paginator.ListClusters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Paginator.ListClusters)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_revisions"]
    ) -> paginator_scope.ListConfigurationRevisionsPaginator:
        """
        [Paginator.ListConfigurationRevisions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Paginator.ListConfigurationRevisions)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configurations"]
    ) -> paginator_scope.ListConfigurationsPaginator:
        """
        [Paginator.ListConfigurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Paginator.ListConfigurations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_nodes"]
    ) -> paginator_scope.ListNodesPaginator:
        """
        [Paginator.ListNodes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/kafka.html#Kafka.Paginator.ListNodes)
        """


class Exceptions:
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    ConflictException: Boto3ClientError
    ForbiddenException: Boto3ClientError
    InternalServerErrorException: Boto3ClientError
    NotFoundException: Boto3ClientError
    ServiceUnavailableException: Boto3ClientError
    TooManyRequestsException: Boto3ClientError
    UnauthorizedException: Boto3ClientError
