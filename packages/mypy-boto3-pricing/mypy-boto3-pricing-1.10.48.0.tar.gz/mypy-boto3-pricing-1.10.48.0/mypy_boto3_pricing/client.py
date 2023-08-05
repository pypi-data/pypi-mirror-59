"""
Main interface for pricing service client

Usage::

    import boto3
    from mypy_boto3.pricing import PricingClient

    session = boto3.Session()

    client: PricingClient = boto3.client("pricing")
    session_client: PricingClient = session.client("pricing")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

import sys
from typing import Any, Dict, List, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_pricing.client as client_scope

# pylint: disable=import-self
import mypy_boto3_pricing.paginator as paginator_scope
from mypy_boto3_pricing.type_defs import (
    DescribeServicesResponseTypeDef,
    FilterTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("PricingClient",)


class PricingClient(BaseClient):
    """
    [Pricing.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client.can_paginate)
        """

    def describe_services(
        self,
        ServiceCode: str = None,
        FormatVersion: str = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> DescribeServicesResponseTypeDef:
        """
        [Client.describe_services documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client.describe_services)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client.generate_presigned_url)
        """

    def get_attribute_values(
        self, ServiceCode: str, AttributeName: str, NextToken: str = None, MaxResults: int = None
    ) -> GetAttributeValuesResponseTypeDef:
        """
        [Client.get_attribute_values documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client.get_attribute_values)
        """

    def get_products(
        self,
        ServiceCode: str = None,
        Filters: List[FilterTypeDef] = None,
        FormatVersion: str = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> GetProductsResponseTypeDef:
        """
        [Client.get_products documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Client.get_products)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_services"]
    ) -> paginator_scope.DescribeServicesPaginator:
        """
        [Paginator.DescribeServices documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Paginator.DescribeServices)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_attribute_values"]
    ) -> paginator_scope.GetAttributeValuesPaginator:
        """
        [Paginator.GetAttributeValues documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Paginator.GetAttributeValues)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_products"]
    ) -> paginator_scope.GetProductsPaginator:
        """
        [Paginator.GetProducts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/pricing.html#Pricing.Paginator.GetProducts)
        """


class Exceptions:
    ClientError: Boto3ClientError
    ExpiredNextTokenException: Boto3ClientError
    InternalErrorException: Boto3ClientError
    InvalidNextTokenException: Boto3ClientError
    InvalidParameterException: Boto3ClientError
    NotFoundException: Boto3ClientError
