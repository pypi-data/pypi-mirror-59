"""
Main interface for iotevents service client

Usage::

    import boto3
    from mypy_boto3.iotevents import IoTEventsClient

    session = boto3.Session()

    client: IoTEventsClient = boto3.client("iotevents")
    session_client: IoTEventsClient = session.client("iotevents")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_iotevents.client as client_scope
from mypy_boto3_iotevents.type_defs import (
    CreateDetectorModelResponseTypeDef,
    CreateInputResponseTypeDef,
    DescribeDetectorModelResponseTypeDef,
    DescribeInputResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DetectorModelDefinitionTypeDef,
    InputDefinitionTypeDef,
    ListDetectorModelVersionsResponseTypeDef,
    ListDetectorModelsResponseTypeDef,
    ListInputsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingOptionsTypeDef,
    TagTypeDef,
    UpdateDetectorModelResponseTypeDef,
    UpdateInputResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTEventsClient",)


class IoTEventsClient(BaseClient):
    """
    [IoTEvents.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.can_paginate)
        """

    def create_detector_model(
        self,
        detectorModelName: str,
        detectorModelDefinition: DetectorModelDefinitionTypeDef,
        roleArn: str,
        detectorModelDescription: str = None,
        key: str = None,
        tags: List[TagTypeDef] = None,
        evaluationMethod: Literal["BATCH", "SERIAL"] = None,
    ) -> CreateDetectorModelResponseTypeDef:
        """
        [Client.create_detector_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.create_detector_model)
        """

    def create_input(
        self,
        inputName: str,
        inputDefinition: InputDefinitionTypeDef,
        inputDescription: str = None,
        tags: List[TagTypeDef] = None,
    ) -> CreateInputResponseTypeDef:
        """
        [Client.create_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.create_input)
        """

    def delete_detector_model(self, detectorModelName: str) -> Dict[str, Any]:
        """
        [Client.delete_detector_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.delete_detector_model)
        """

    def delete_input(self, inputName: str) -> Dict[str, Any]:
        """
        [Client.delete_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.delete_input)
        """

    def describe_detector_model(
        self, detectorModelName: str, detectorModelVersion: str = None
    ) -> DescribeDetectorModelResponseTypeDef:
        """
        [Client.describe_detector_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.describe_detector_model)
        """

    def describe_input(self, inputName: str) -> DescribeInputResponseTypeDef:
        """
        [Client.describe_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.describe_input)
        """

    def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        [Client.describe_logging_options documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.describe_logging_options)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.generate_presigned_url)
        """

    def list_detector_model_versions(
        self, detectorModelName: str, nextToken: str = None, maxResults: int = None
    ) -> ListDetectorModelVersionsResponseTypeDef:
        """
        [Client.list_detector_model_versions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.list_detector_model_versions)
        """

    def list_detector_models(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListDetectorModelsResponseTypeDef:
        """
        [Client.list_detector_models documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.list_detector_models)
        """

    def list_inputs(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListInputsResponseTypeDef:
        """
        [Client.list_inputs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.list_inputs)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.list_tags_for_resource)
        """

    def put_logging_options(self, loggingOptions: LoggingOptionsTypeDef) -> None:
        """
        [Client.put_logging_options documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.put_logging_options)
        """

    def tag_resource(self, resourceArn: str, tags: List[TagTypeDef]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.untag_resource)
        """

    def update_detector_model(
        self,
        detectorModelName: str,
        detectorModelDefinition: DetectorModelDefinitionTypeDef,
        roleArn: str,
        detectorModelDescription: str = None,
        evaluationMethod: Literal["BATCH", "SERIAL"] = None,
    ) -> UpdateDetectorModelResponseTypeDef:
        """
        [Client.update_detector_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.update_detector_model)
        """

    def update_input(
        self, inputName: str, inputDefinition: InputDefinitionTypeDef, inputDescription: str = None
    ) -> UpdateInputResponseTypeDef:
        """
        [Client.update_input documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotevents.html#IoTEvents.Client.update_input)
        """


class Exceptions:
    ClientError: Boto3ClientError
    InternalFailureException: Boto3ClientError
    InvalidRequestException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    ResourceAlreadyExistsException: Boto3ClientError
    ResourceInUseException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    ServiceUnavailableException: Boto3ClientError
    ThrottlingException: Boto3ClientError
    UnsupportedOperationException: Boto3ClientError
