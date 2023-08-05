"""
Main interface for cloudhsmv2 service client

Usage::

    import boto3
    from mypy_boto3.cloudhsmv2 import CloudHSMV2Client

    session = boto3.Session()

    client: CloudHSMV2Client = boto3.client("cloudhsmv2")
    session_client: CloudHSMV2Client = session.client("cloudhsmv2")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_cloudhsmv2.client as client_scope

# pylint: disable=import-self
import mypy_boto3_cloudhsmv2.paginator as paginator_scope
from mypy_boto3_cloudhsmv2.type_defs import (
    CopyBackupToRegionResponseTypeDef,
    CreateClusterResponseTypeDef,
    CreateHsmResponseTypeDef,
    DeleteBackupResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteHsmResponseTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    InitializeClusterResponseTypeDef,
    ListTagsResponseTypeDef,
    RestoreBackupResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudHSMV2Client",)


class CloudHSMV2Client(BaseClient):
    """
    [CloudHSMV2.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.can_paginate)
        """

    def copy_backup_to_region(
        self, DestinationRegion: str, BackupId: str
    ) -> CopyBackupToRegionResponseTypeDef:
        """
        [Client.copy_backup_to_region documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.copy_backup_to_region)
        """

    def create_cluster(
        self, SubnetIds: List[str], HsmType: str, SourceBackupId: str = None
    ) -> CreateClusterResponseTypeDef:
        """
        [Client.create_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.create_cluster)
        """

    def create_hsm(
        self, ClusterId: str, AvailabilityZone: str, IpAddress: str = None
    ) -> CreateHsmResponseTypeDef:
        """
        [Client.create_hsm documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.create_hsm)
        """

    def delete_backup(self, BackupId: str) -> DeleteBackupResponseTypeDef:
        """
        [Client.delete_backup documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_backup)
        """

    def delete_cluster(self, ClusterId: str) -> DeleteClusterResponseTypeDef:
        """
        [Client.delete_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_cluster)
        """

    def delete_hsm(
        self, ClusterId: str, HsmId: str = None, EniId: str = None, EniIp: str = None
    ) -> DeleteHsmResponseTypeDef:
        """
        [Client.delete_hsm documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_hsm)
        """

    def describe_backups(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: Dict[str, List[str]] = None,
        SortAscending: bool = None,
    ) -> DescribeBackupsResponseTypeDef:
        """
        [Client.describe_backups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.describe_backups)
        """

    def describe_clusters(
        self, Filters: Dict[str, List[str]] = None, NextToken: str = None, MaxResults: int = None
    ) -> DescribeClustersResponseTypeDef:
        """
        [Client.describe_clusters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.describe_clusters)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.generate_presigned_url)
        """

    def initialize_cluster(
        self, ClusterId: str, SignedCert: str, TrustAnchor: str
    ) -> InitializeClusterResponseTypeDef:
        """
        [Client.initialize_cluster documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.initialize_cluster)
        """

    def list_tags(
        self, ResourceId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTagsResponseTypeDef:
        """
        [Client.list_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.list_tags)
        """

    def restore_backup(self, BackupId: str) -> RestoreBackupResponseTypeDef:
        """
        [Client.restore_backup documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.restore_backup)
        """

    def tag_resource(self, ResourceId: str, TagList: List[TagTypeDef]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.tag_resource)
        """

    def untag_resource(self, ResourceId: str, TagKeyList: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Client.untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_backups"]
    ) -> paginator_scope.DescribeBackupsPaginator:
        """
        [Paginator.DescribeBackups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeBackups)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_clusters"]
    ) -> paginator_scope.DescribeClustersPaginator:
        """
        [Paginator.DescribeClusters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeClusters)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags"]
    ) -> paginator_scope.ListTagsPaginator:
        """
        [Paginator.ListTags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.ListTags)
        """


class Exceptions:
    ClientError: Boto3ClientError
    CloudHsmAccessDeniedException: Boto3ClientError
    CloudHsmInternalFailureException: Boto3ClientError
    CloudHsmInvalidRequestException: Boto3ClientError
    CloudHsmResourceNotFoundException: Boto3ClientError
    CloudHsmServiceException: Boto3ClientError
