"""
Main interface for secretsmanager service client

Usage::

    import boto3
    from mypy_boto3.secretsmanager import SecretsManagerClient

    session = boto3.Session()

    client: SecretsManagerClient = boto3.client("secretsmanager")
    session_client: SecretsManagerClient = session.client("secretsmanager")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, IO, List, Union, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_secretsmanager.client as client_scope

# pylint: disable=import-self
import mypy_boto3_secretsmanager.paginator as paginator_scope
from mypy_boto3_secretsmanager.type_defs import (
    CancelRotateSecretResponseTypeDef,
    CreateSecretResponseTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteSecretResponseTypeDef,
    DescribeSecretResponseTypeDef,
    GetRandomPasswordResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSecretValueResponseTypeDef,
    ListSecretVersionIdsResponseTypeDef,
    ListSecretsResponseTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSecretValueResponseTypeDef,
    RestoreSecretResponseTypeDef,
    RotateSecretResponseTypeDef,
    RotationRulesTypeTypeDef,
    TagTypeDef,
    UpdateSecretResponseTypeDef,
    UpdateSecretVersionStageResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SecretsManagerClient",)


class SecretsManagerClient(BaseClient):
    """
    [SecretsManager.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.can_paginate)
        """

    def cancel_rotate_secret(self, SecretId: str) -> CancelRotateSecretResponseTypeDef:
        """
        [Client.cancel_rotate_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.cancel_rotate_secret)
        """

    def create_secret(
        self,
        Name: str,
        ClientRequestToken: str = None,
        Description: str = None,
        KmsKeyId: str = None,
        SecretBinary: Union[bytes, IO] = None,
        SecretString: str = None,
        Tags: List[TagTypeDef] = None,
    ) -> CreateSecretResponseTypeDef:
        """
        [Client.create_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.create_secret)
        """

    def delete_resource_policy(self, SecretId: str) -> DeleteResourcePolicyResponseTypeDef:
        """
        [Client.delete_resource_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.delete_resource_policy)
        """

    def delete_secret(
        self,
        SecretId: str,
        RecoveryWindowInDays: int = None,
        ForceDeleteWithoutRecovery: bool = None,
    ) -> DeleteSecretResponseTypeDef:
        """
        [Client.delete_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.delete_secret)
        """

    def describe_secret(self, SecretId: str) -> DescribeSecretResponseTypeDef:
        """
        [Client.describe_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.describe_secret)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.generate_presigned_url)
        """

    def get_random_password(
        self,
        PasswordLength: int = None,
        ExcludeCharacters: str = None,
        ExcludeNumbers: bool = None,
        ExcludePunctuation: bool = None,
        ExcludeUppercase: bool = None,
        ExcludeLowercase: bool = None,
        IncludeSpace: bool = None,
        RequireEachIncludedType: bool = None,
    ) -> GetRandomPasswordResponseTypeDef:
        """
        [Client.get_random_password documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.get_random_password)
        """

    def get_resource_policy(self, SecretId: str) -> GetResourcePolicyResponseTypeDef:
        """
        [Client.get_resource_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.get_resource_policy)
        """

    def get_secret_value(
        self, SecretId: str, VersionId: str = None, VersionStage: str = None
    ) -> GetSecretValueResponseTypeDef:
        """
        [Client.get_secret_value documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value)
        """

    def list_secret_version_ids(
        self,
        SecretId: str,
        MaxResults: int = None,
        NextToken: str = None,
        IncludeDeprecated: bool = None,
    ) -> ListSecretVersionIdsResponseTypeDef:
        """
        [Client.list_secret_version_ids documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.list_secret_version_ids)
        """

    def list_secrets(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListSecretsResponseTypeDef:
        """
        [Client.list_secrets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.list_secrets)
        """

    def put_resource_policy(
        self, SecretId: str, ResourcePolicy: str
    ) -> PutResourcePolicyResponseTypeDef:
        """
        [Client.put_resource_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.put_resource_policy)
        """

    def put_secret_value(
        self,
        SecretId: str,
        ClientRequestToken: str = None,
        SecretBinary: Union[bytes, IO] = None,
        SecretString: str = None,
        VersionStages: List[str] = None,
    ) -> PutSecretValueResponseTypeDef:
        """
        [Client.put_secret_value documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.put_secret_value)
        """

    def restore_secret(self, SecretId: str) -> RestoreSecretResponseTypeDef:
        """
        [Client.restore_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.restore_secret)
        """

    def rotate_secret(
        self,
        SecretId: str,
        ClientRequestToken: str = None,
        RotationLambdaARN: str = None,
        RotationRules: RotationRulesTypeTypeDef = None,
    ) -> RotateSecretResponseTypeDef:
        """
        [Client.rotate_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.rotate_secret)
        """

    def tag_resource(self, SecretId: str, Tags: List[TagTypeDef]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.tag_resource)
        """

    def untag_resource(self, SecretId: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.untag_resource)
        """

    def update_secret(
        self,
        SecretId: str,
        ClientRequestToken: str = None,
        Description: str = None,
        KmsKeyId: str = None,
        SecretBinary: Union[bytes, IO] = None,
        SecretString: str = None,
    ) -> UpdateSecretResponseTypeDef:
        """
        [Client.update_secret documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.update_secret)
        """

    def update_secret_version_stage(
        self,
        SecretId: str,
        VersionStage: str,
        RemoveFromVersionId: str = None,
        MoveToVersionId: str = None,
    ) -> UpdateSecretVersionStageResponseTypeDef:
        """
        [Client.update_secret_version_stage documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Client.update_secret_version_stage)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_secrets"]
    ) -> paginator_scope.ListSecretsPaginator:
        """
        [Paginator.ListSecrets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/secretsmanager.html#SecretsManager.Paginator.ListSecrets)
        """


class Exceptions:
    ClientError: Boto3ClientError
    DecryptionFailure: Boto3ClientError
    EncryptionFailure: Boto3ClientError
    InternalServiceError: Boto3ClientError
    InvalidNextTokenException: Boto3ClientError
    InvalidParameterException: Boto3ClientError
    InvalidRequestException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    MalformedPolicyDocumentException: Boto3ClientError
    PreconditionNotMetException: Boto3ClientError
    ResourceExistsException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
