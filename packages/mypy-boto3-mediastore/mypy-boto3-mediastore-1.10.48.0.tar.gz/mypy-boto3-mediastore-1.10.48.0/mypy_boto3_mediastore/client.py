"""
Main interface for mediastore service client

Usage::

    import boto3
    from mypy_boto3.mediastore import MediaStoreClient

    session = boto3.Session()

    client: MediaStoreClient = boto3.client("mediastore")
    session_client: MediaStoreClient = session.client("mediastore")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_mediastore.client as client_scope

# pylint: disable=import-self
import mypy_boto3_mediastore.paginator as paginator_scope
from mypy_boto3_mediastore.type_defs import (
    CorsRuleTypeDef,
    CreateContainerOutputTypeDef,
    DescribeContainerOutputTypeDef,
    GetContainerPolicyOutputTypeDef,
    GetCorsPolicyOutputTypeDef,
    GetLifecyclePolicyOutputTypeDef,
    ListContainersOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaStoreClient",)


class MediaStoreClient(BaseClient):
    """
    [MediaStore.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.can_paginate)
        """

    def create_container(
        self, ContainerName: str, Tags: List[TagTypeDef] = None
    ) -> CreateContainerOutputTypeDef:
        """
        [Client.create_container documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.create_container)
        """

    def delete_container(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.delete_container documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.delete_container)
        """

    def delete_container_policy(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.delete_container_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.delete_container_policy)
        """

    def delete_cors_policy(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.delete_cors_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.delete_cors_policy)
        """

    def delete_lifecycle_policy(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.delete_lifecycle_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.delete_lifecycle_policy)
        """

    def describe_container(self, ContainerName: str = None) -> DescribeContainerOutputTypeDef:
        """
        [Client.describe_container documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.describe_container)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.generate_presigned_url)
        """

    def get_container_policy(self, ContainerName: str) -> GetContainerPolicyOutputTypeDef:
        """
        [Client.get_container_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.get_container_policy)
        """

    def get_cors_policy(self, ContainerName: str) -> GetCorsPolicyOutputTypeDef:
        """
        [Client.get_cors_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.get_cors_policy)
        """

    def get_lifecycle_policy(self, ContainerName: str) -> GetLifecyclePolicyOutputTypeDef:
        """
        [Client.get_lifecycle_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.get_lifecycle_policy)
        """

    def list_containers(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListContainersOutputTypeDef:
        """
        [Client.list_containers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.list_containers)
        """

    def list_tags_for_resource(self, Resource: str) -> ListTagsForResourceOutputTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.list_tags_for_resource)
        """

    def put_container_policy(self, ContainerName: str, Policy: str) -> Dict[str, Any]:
        """
        [Client.put_container_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.put_container_policy)
        """

    def put_cors_policy(
        self, ContainerName: str, CorsPolicy: List[CorsRuleTypeDef]
    ) -> Dict[str, Any]:
        """
        [Client.put_cors_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.put_cors_policy)
        """

    def put_lifecycle_policy(self, ContainerName: str, LifecyclePolicy: str) -> Dict[str, Any]:
        """
        [Client.put_lifecycle_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.put_lifecycle_policy)
        """

    def start_access_logging(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.start_access_logging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.start_access_logging)
        """

    def stop_access_logging(self, ContainerName: str) -> Dict[str, Any]:
        """
        [Client.stop_access_logging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.stop_access_logging)
        """

    def tag_resource(self, Resource: str, Tags: List[TagTypeDef]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.tag_resource)
        """

    def untag_resource(self, Resource: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Client.untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_containers"]
    ) -> paginator_scope.ListContainersPaginator:
        """
        [Paginator.ListContainers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/mediastore.html#MediaStore.Paginator.ListContainers)
        """


class Exceptions:
    ClientError: Boto3ClientError
    ContainerInUseException: Boto3ClientError
    ContainerNotFoundException: Boto3ClientError
    CorsPolicyNotFoundException: Boto3ClientError
    InternalServerError: Boto3ClientError
    LimitExceededException: Boto3ClientError
    PolicyNotFoundException: Boto3ClientError
