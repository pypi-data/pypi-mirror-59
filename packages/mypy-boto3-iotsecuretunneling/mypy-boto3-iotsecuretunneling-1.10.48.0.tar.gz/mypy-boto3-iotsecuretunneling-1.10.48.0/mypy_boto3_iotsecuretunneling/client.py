"""
Main interface for iotsecuretunneling service client

Usage::

    import boto3
    from mypy_boto3.iotsecuretunneling import IoTSecureTunnelingClient

    session = boto3.Session()

    client: IoTSecureTunnelingClient = boto3.client("iotsecuretunneling")
    session_client: IoTSecureTunnelingClient = session.client("iotsecuretunneling")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from __future__ import annotations

from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_iotsecuretunneling.client as client_scope
from mypy_boto3_iotsecuretunneling.type_defs import (
    DescribeTunnelResponseTypeDef,
    DestinationConfigTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTunnelsResponseTypeDef,
    OpenTunnelResponseTypeDef,
    TagTypeDef,
    TimeoutConfigTypeDef,
)


__all__ = ("IoTSecureTunnelingClient",)


class IoTSecureTunnelingClient(BaseClient):
    """
    [IoTSecureTunneling.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
    """

    exceptions: client_scope.Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.can_paginate)
        """

    def close_tunnel(self, tunnelId: str, delete: bool = None) -> Dict[str, Any]:
        """
        [Client.close_tunnel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.close_tunnel)
        """

    def describe_tunnel(self, tunnelId: str) -> DescribeTunnelResponseTypeDef:
        """
        [Client.describe_tunnel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.describe_tunnel)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.generate_presigned_url)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tags_for_resource)
        """

    def list_tunnels(
        self, thingName: str = None, maxResults: int = None, nextToken: str = None
    ) -> ListTunnelsResponseTypeDef:
        """
        [Client.list_tunnels documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tunnels)
        """

    def open_tunnel(
        self,
        description: str = None,
        tags: List[TagTypeDef] = None,
        destinationConfig: DestinationConfigTypeDef = None,
        timeoutConfig: TimeoutConfigTypeDef = None,
    ) -> OpenTunnelResponseTypeDef:
        """
        [Client.open_tunnel documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.open_tunnel)
        """

    def tag_resource(self, resourceArn: str, tags: List[TagTypeDef]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.10.48/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.untag_resource)
        """


class Exceptions:
    ClientError: Boto3ClientError
    LimitExceededException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
