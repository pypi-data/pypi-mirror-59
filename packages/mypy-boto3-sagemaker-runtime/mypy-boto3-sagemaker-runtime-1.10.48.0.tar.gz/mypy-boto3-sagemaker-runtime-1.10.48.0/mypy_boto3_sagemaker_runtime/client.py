"""
Main interface for sagemaker-runtime service client

Usage::

    import boto3
    from mypy_boto3.sagemaker_runtime import SageMakerRuntimeClient

    session = boto3.Session()

    client: SageMakerRuntimeClient = boto3.client("sagemaker-runtime")
    session_client: SageMakerRuntimeClient = session.client("sagemaker-runtime")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

from typing import Any, Dict, IO, Union
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_sagemaker_runtime.client as client_scope
from mypy_boto3_sagemaker_runtime.type_defs import InvokeEndpointOutputTypeDef


__all__ = ("SageMakerRuntimeClient",)


class SageMakerRuntimeClient(BaseClient):
    """
    [SageMakerRuntime.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.generate_presigned_url)
        """

    def invoke_endpoint(
        self,
        EndpointName: str,
        Body: Union[bytes, IO],
        ContentType: str = None,
        Accept: str = None,
        CustomAttributes: str = None,
        TargetModel: str = None,
    ) -> InvokeEndpointOutputTypeDef:
        """
        [Client.invoke_endpoint documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint)
        """


class Exceptions:
    ClientError: Boto3ClientError
    InternalFailure: Boto3ClientError
    ModelError: Boto3ClientError
    ServiceUnavailable: Boto3ClientError
    ValidationError: Boto3ClientError
