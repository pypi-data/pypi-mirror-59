"""
Main interface for transcribe service client

Usage::

    import boto3
    from mypy_boto3.transcribe import TranscribeServiceClient

    session = boto3.Session()

    client: TranscribeServiceClient = boto3.client("transcribe")
    session_client: TranscribeServiceClient = session.client("transcribe")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_transcribe.client as client_scope
from mypy_boto3_transcribe.type_defs import (
    CreateVocabularyFilterResponseTypeDef,
    CreateVocabularyResponseTypeDef,
    GetTranscriptionJobResponseTypeDef,
    GetVocabularyFilterResponseTypeDef,
    GetVocabularyResponseTypeDef,
    JobExecutionSettingsTypeDef,
    ListTranscriptionJobsResponseTypeDef,
    ListVocabulariesResponseTypeDef,
    ListVocabularyFiltersResponseTypeDef,
    MediaTypeDef,
    SettingsTypeDef,
    StartTranscriptionJobResponseTypeDef,
    UpdateVocabularyFilterResponseTypeDef,
    UpdateVocabularyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TranscribeServiceClient",)


class TranscribeServiceClient(BaseClient):
    """
    [TranscribeService.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.can_paginate)
        """

    def create_vocabulary(
        self,
        VocabularyName: str,
        LanguageCode: Literal[
            "en-US",
            "es-US",
            "en-AU",
            "fr-CA",
            "en-GB",
            "de-DE",
            "pt-BR",
            "fr-FR",
            "it-IT",
            "ko-KR",
            "es-ES",
            "en-IN",
            "hi-IN",
            "ar-SA",
            "ru-RU",
            "zh-CN",
            "nl-NL",
            "id-ID",
            "ta-IN",
            "fa-IR",
            "en-IE",
            "en-AB",
            "en-WL",
            "pt-PT",
            "te-IN",
            "tr-TR",
            "de-CH",
            "he-IL",
            "ms-MY",
            "ja-JP",
            "ar-AE",
        ],
        Phrases: List[str] = None,
        VocabularyFileUri: str = None,
    ) -> CreateVocabularyResponseTypeDef:
        """
        [Client.create_vocabulary documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.create_vocabulary)
        """

    def create_vocabulary_filter(
        self,
        VocabularyFilterName: str,
        LanguageCode: Literal[
            "en-US",
            "es-US",
            "en-AU",
            "fr-CA",
            "en-GB",
            "de-DE",
            "pt-BR",
            "fr-FR",
            "it-IT",
            "ko-KR",
            "es-ES",
            "en-IN",
            "hi-IN",
            "ar-SA",
            "ru-RU",
            "zh-CN",
            "nl-NL",
            "id-ID",
            "ta-IN",
            "fa-IR",
            "en-IE",
            "en-AB",
            "en-WL",
            "pt-PT",
            "te-IN",
            "tr-TR",
            "de-CH",
            "he-IL",
            "ms-MY",
            "ja-JP",
            "ar-AE",
        ],
        Words: List[str] = None,
        VocabularyFilterFileUri: str = None,
    ) -> CreateVocabularyFilterResponseTypeDef:
        """
        [Client.create_vocabulary_filter documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.create_vocabulary_filter)
        """

    def delete_transcription_job(self, TranscriptionJobName: str) -> None:
        """
        [Client.delete_transcription_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.delete_transcription_job)
        """

    def delete_vocabulary(self, VocabularyName: str) -> None:
        """
        [Client.delete_vocabulary documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.delete_vocabulary)
        """

    def delete_vocabulary_filter(self, VocabularyFilterName: str) -> None:
        """
        [Client.delete_vocabulary_filter documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.delete_vocabulary_filter)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.generate_presigned_url)
        """

    def get_transcription_job(
        self, TranscriptionJobName: str
    ) -> GetTranscriptionJobResponseTypeDef:
        """
        [Client.get_transcription_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.get_transcription_job)
        """

    def get_vocabulary(self, VocabularyName: str) -> GetVocabularyResponseTypeDef:
        """
        [Client.get_vocabulary documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.get_vocabulary)
        """

    def get_vocabulary_filter(
        self, VocabularyFilterName: str
    ) -> GetVocabularyFilterResponseTypeDef:
        """
        [Client.get_vocabulary_filter documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.get_vocabulary_filter)
        """

    def list_transcription_jobs(
        self,
        Status: Literal["QUEUED", "IN_PROGRESS", "FAILED", "COMPLETED"] = None,
        JobNameContains: str = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListTranscriptionJobsResponseTypeDef:
        """
        [Client.list_transcription_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.list_transcription_jobs)
        """

    def list_vocabularies(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        StateEquals: Literal["PENDING", "READY", "FAILED"] = None,
        NameContains: str = None,
    ) -> ListVocabulariesResponseTypeDef:
        """
        [Client.list_vocabularies documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.list_vocabularies)
        """

    def list_vocabulary_filters(
        self, NextToken: str = None, MaxResults: int = None, NameContains: str = None
    ) -> ListVocabularyFiltersResponseTypeDef:
        """
        [Client.list_vocabulary_filters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.list_vocabulary_filters)
        """

    def start_transcription_job(
        self,
        TranscriptionJobName: str,
        LanguageCode: Literal[
            "en-US",
            "es-US",
            "en-AU",
            "fr-CA",
            "en-GB",
            "de-DE",
            "pt-BR",
            "fr-FR",
            "it-IT",
            "ko-KR",
            "es-ES",
            "en-IN",
            "hi-IN",
            "ar-SA",
            "ru-RU",
            "zh-CN",
            "nl-NL",
            "id-ID",
            "ta-IN",
            "fa-IR",
            "en-IE",
            "en-AB",
            "en-WL",
            "pt-PT",
            "te-IN",
            "tr-TR",
            "de-CH",
            "he-IL",
            "ms-MY",
            "ja-JP",
            "ar-AE",
        ],
        Media: MediaTypeDef,
        MediaSampleRateHertz: int = None,
        MediaFormat: Literal["mp3", "mp4", "wav", "flac"] = None,
        OutputBucketName: str = None,
        OutputEncryptionKMSKeyId: str = None,
        Settings: SettingsTypeDef = None,
        JobExecutionSettings: JobExecutionSettingsTypeDef = None,
    ) -> StartTranscriptionJobResponseTypeDef:
        """
        [Client.start_transcription_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.start_transcription_job)
        """

    def update_vocabulary(
        self,
        VocabularyName: str,
        LanguageCode: Literal[
            "en-US",
            "es-US",
            "en-AU",
            "fr-CA",
            "en-GB",
            "de-DE",
            "pt-BR",
            "fr-FR",
            "it-IT",
            "ko-KR",
            "es-ES",
            "en-IN",
            "hi-IN",
            "ar-SA",
            "ru-RU",
            "zh-CN",
            "nl-NL",
            "id-ID",
            "ta-IN",
            "fa-IR",
            "en-IE",
            "en-AB",
            "en-WL",
            "pt-PT",
            "te-IN",
            "tr-TR",
            "de-CH",
            "he-IL",
            "ms-MY",
            "ja-JP",
            "ar-AE",
        ],
        Phrases: List[str] = None,
        VocabularyFileUri: str = None,
    ) -> UpdateVocabularyResponseTypeDef:
        """
        [Client.update_vocabulary documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.update_vocabulary)
        """

    def update_vocabulary_filter(
        self,
        VocabularyFilterName: str,
        Words: List[str] = None,
        VocabularyFilterFileUri: str = None,
    ) -> UpdateVocabularyFilterResponseTypeDef:
        """
        [Client.update_vocabulary_filter documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/transcribe.html#TranscribeService.Client.update_vocabulary_filter)
        """


class Exceptions:
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    ConflictException: Boto3ClientError
    InternalFailureException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    NotFoundException: Boto3ClientError
