"""
Main interface for personalize-runtime service client

Usage::

    import boto3
    from mypy_boto3.personalize_runtime import PersonalizeRuntimeClient

    session = boto3.Session()

    client: PersonalizeRuntimeClient = boto3.client("personalize-runtime")
    session_client: PersonalizeRuntimeClient = session.client("personalize-runtime")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_personalize_runtime.client as client_scope
from mypy_boto3_personalize_runtime.type_defs import (
    GetPersonalizedRankingResponseTypeDef,
    GetRecommendationsResponseTypeDef,
)


__all__ = ("PersonalizeRuntimeClient",)


class PersonalizeRuntimeClient(BaseClient):
    """
    [PersonalizeRuntime.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/personalize-runtime.html#PersonalizeRuntime.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.generate_presigned_url)
        """

    def get_personalized_ranking(
        self, campaignArn: str, inputList: List[str], userId: str, context: Dict[str, str] = None
    ) -> GetPersonalizedRankingResponseTypeDef:
        """
        [Client.get_personalized_ranking documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_personalized_ranking)
        """

    def get_recommendations(
        self,
        campaignArn: str,
        itemId: str = None,
        userId: str = None,
        numResults: int = None,
        context: Dict[str, str] = None,
    ) -> GetRecommendationsResponseTypeDef:
        """
        [Client.get_recommendations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_recommendations)
        """


class Exceptions:
    ClientError: Boto3ClientError
    InvalidInputException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
