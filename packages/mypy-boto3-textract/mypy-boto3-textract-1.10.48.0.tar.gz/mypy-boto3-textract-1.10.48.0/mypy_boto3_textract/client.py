"""
Main interface for textract service client

Usage::

    import boto3
    from mypy_boto3.textract import TextractClient

    session = boto3.Session()

    client: TextractClient = boto3.client("textract")
    session_client: TextractClient = session.client("textract")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_textract.client as client_scope
from mypy_boto3_textract.type_defs import (
    AnalyzeDocumentResponseTypeDef,
    DetectDocumentTextResponseTypeDef,
    DocumentLocationTypeDef,
    DocumentTypeDef,
    GetDocumentAnalysisResponseTypeDef,
    GetDocumentTextDetectionResponseTypeDef,
    HumanLoopConfigTypeDef,
    NotificationChannelTypeDef,
    StartDocumentAnalysisResponseTypeDef,
    StartDocumentTextDetectionResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TextractClient",)


class TextractClient(BaseClient):
    """
    [Textract.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client)
    """

    exceptions: client_scope.Exceptions

    def analyze_document(
        self,
        Document: DocumentTypeDef,
        FeatureTypes: List[Literal["TABLES", "FORMS"]],
        HumanLoopConfig: HumanLoopConfigTypeDef = None,
    ) -> AnalyzeDocumentResponseTypeDef:
        """
        [Client.analyze_document documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.analyze_document)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.can_paginate)
        """

    def detect_document_text(self, Document: DocumentTypeDef) -> DetectDocumentTextResponseTypeDef:
        """
        [Client.detect_document_text documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.detect_document_text)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.generate_presigned_url)
        """

    def get_document_analysis(
        self, JobId: str, MaxResults: int = None, NextToken: str = None
    ) -> GetDocumentAnalysisResponseTypeDef:
        """
        [Client.get_document_analysis documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.get_document_analysis)
        """

    def get_document_text_detection(
        self, JobId: str, MaxResults: int = None, NextToken: str = None
    ) -> GetDocumentTextDetectionResponseTypeDef:
        """
        [Client.get_document_text_detection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.get_document_text_detection)
        """

    def start_document_analysis(
        self,
        DocumentLocation: DocumentLocationTypeDef,
        FeatureTypes: List[Literal["TABLES", "FORMS"]],
        ClientRequestToken: str = None,
        JobTag: str = None,
        NotificationChannel: NotificationChannelTypeDef = None,
    ) -> StartDocumentAnalysisResponseTypeDef:
        """
        [Client.start_document_analysis documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.start_document_analysis)
        """

    def start_document_text_detection(
        self,
        DocumentLocation: DocumentLocationTypeDef,
        ClientRequestToken: str = None,
        JobTag: str = None,
        NotificationChannel: NotificationChannelTypeDef = None,
    ) -> StartDocumentTextDetectionResponseTypeDef:
        """
        [Client.start_document_text_detection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/textract.html#Textract.Client.start_document_text_detection)
        """


class Exceptions:
    AccessDeniedException: Boto3ClientError
    BadDocumentException: Boto3ClientError
    ClientError: Boto3ClientError
    DocumentTooLargeException: Boto3ClientError
    HumanLoopQuotaExceededException: Boto3ClientError
    IdempotentParameterMismatchException: Boto3ClientError
    InternalServerError: Boto3ClientError
    InvalidJobIdException: Boto3ClientError
    InvalidParameterException: Boto3ClientError
    InvalidS3ObjectException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    ProvisionedThroughputExceededException: Boto3ClientError
    ThrottlingException: Boto3ClientError
    UnsupportedDocumentException: Boto3ClientError
