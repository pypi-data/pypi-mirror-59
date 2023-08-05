"""
Main interface for shield service client

Usage::

    import boto3
    from mypy_boto3.shield import ShieldClient

    session = boto3.Session()

    client: ShieldClient = boto3.client("shield")
    session_client: ShieldClient = session.client("shield")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_shield.client as client_scope

# pylint: disable=import-self
import mypy_boto3_shield.paginator as paginator_scope
from mypy_boto3_shield.type_defs import (
    CreateProtectionResponseTypeDef,
    DescribeAttackResponseTypeDef,
    DescribeDRTAccessResponseTypeDef,
    DescribeEmergencyContactSettingsResponseTypeDef,
    DescribeProtectionResponseTypeDef,
    DescribeSubscriptionResponseTypeDef,
    EmergencyContactTypeDef,
    GetSubscriptionStateResponseTypeDef,
    ListAttacksResponseTypeDef,
    ListProtectionsResponseTypeDef,
    TimeRangeTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ShieldClient",)


class ShieldClient(BaseClient):
    """
    [Shield.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client)
    """

    exceptions: client_scope.Exceptions

    def associate_drt_log_bucket(self, LogBucket: str) -> Dict[str, Any]:
        """
        [Client.associate_drt_log_bucket documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.associate_drt_log_bucket)
        """

    def associate_drt_role(self, RoleArn: str) -> Dict[str, Any]:
        """
        [Client.associate_drt_role documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.associate_drt_role)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.can_paginate)
        """

    def create_protection(self, Name: str, ResourceArn: str) -> CreateProtectionResponseTypeDef:
        """
        [Client.create_protection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.create_protection)
        """

    def create_subscription(self) -> Dict[str, Any]:
        """
        [Client.create_subscription documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.create_subscription)
        """

    def delete_protection(self, ProtectionId: str) -> Dict[str, Any]:
        """
        [Client.delete_protection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.delete_protection)
        """

    def delete_subscription(self) -> Dict[str, Any]:
        """
        [Client.delete_subscription documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.delete_subscription)
        """

    def describe_attack(self, AttackId: str) -> DescribeAttackResponseTypeDef:
        """
        [Client.describe_attack documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.describe_attack)
        """

    def describe_drt_access(self) -> DescribeDRTAccessResponseTypeDef:
        """
        [Client.describe_drt_access documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.describe_drt_access)
        """

    def describe_emergency_contact_settings(
        self,
    ) -> DescribeEmergencyContactSettingsResponseTypeDef:
        """
        [Client.describe_emergency_contact_settings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.describe_emergency_contact_settings)
        """

    def describe_protection(
        self, ProtectionId: str = None, ResourceArn: str = None
    ) -> DescribeProtectionResponseTypeDef:
        """
        [Client.describe_protection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.describe_protection)
        """

    def describe_subscription(self) -> DescribeSubscriptionResponseTypeDef:
        """
        [Client.describe_subscription documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.describe_subscription)
        """

    def disassociate_drt_log_bucket(self, LogBucket: str) -> Dict[str, Any]:
        """
        [Client.disassociate_drt_log_bucket documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.disassociate_drt_log_bucket)
        """

    def disassociate_drt_role(self) -> Dict[str, Any]:
        """
        [Client.disassociate_drt_role documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.disassociate_drt_role)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.generate_presigned_url)
        """

    def get_subscription_state(self) -> GetSubscriptionStateResponseTypeDef:
        """
        [Client.get_subscription_state documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.get_subscription_state)
        """

    def list_attacks(
        self,
        ResourceArns: List[str] = None,
        StartTime: TimeRangeTypeDef = None,
        EndTime: TimeRangeTypeDef = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListAttacksResponseTypeDef:
        """
        [Client.list_attacks documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.list_attacks)
        """

    def list_protections(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListProtectionsResponseTypeDef:
        """
        [Client.list_protections documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.list_protections)
        """

    def update_emergency_contact_settings(
        self, EmergencyContactList: List[EmergencyContactTypeDef] = None
    ) -> Dict[str, Any]:
        """
        [Client.update_emergency_contact_settings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.update_emergency_contact_settings)
        """

    def update_subscription(
        self, AutoRenew: Literal["ENABLED", "DISABLED"] = None
    ) -> Dict[str, Any]:
        """
        [Client.update_subscription documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Client.update_subscription)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attacks"]
    ) -> paginator_scope.ListAttacksPaginator:
        """
        [Paginator.ListAttacks documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Paginator.ListAttacks)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protections"]
    ) -> paginator_scope.ListProtectionsPaginator:
        """
        [Paginator.ListProtections documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/shield.html#Shield.Paginator.ListProtections)
        """


class Exceptions:
    AccessDeniedException: Boto3ClientError
    AccessDeniedForDependencyException: Boto3ClientError
    ClientError: Boto3ClientError
    InternalErrorException: Boto3ClientError
    InvalidOperationException: Boto3ClientError
    InvalidPaginationTokenException: Boto3ClientError
    InvalidParameterException: Boto3ClientError
    InvalidResourceException: Boto3ClientError
    LimitsExceededException: Boto3ClientError
    LockedSubscriptionException: Boto3ClientError
    NoAssociatedRoleException: Boto3ClientError
    OptimisticLockException: Boto3ClientError
    ResourceAlreadyExistsException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
