"""
Main interface for kinesis-video-signaling service type definitions.

Usage::

    from mypy_boto3.kinesis_video_signaling.type_defs import IceServerTypeDef

    data: IceServerTypeDef = {...}
"""
from __future__ import annotations

import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "IceServerTypeDef",
    "GetIceServerConfigResponseTypeDef",
    "SendAlexaOfferToMasterResponseTypeDef",
)

IceServerTypeDef = TypedDict(
    "IceServerTypeDef",
    {"Uris": List[str], "Username": str, "Password": str, "Ttl": int},
    total=False,
)

GetIceServerConfigResponseTypeDef = TypedDict(
    "GetIceServerConfigResponseTypeDef", {"IceServerList": List[IceServerTypeDef]}, total=False
)

SendAlexaOfferToMasterResponseTypeDef = TypedDict(
    "SendAlexaOfferToMasterResponseTypeDef", {"Answer": str}, total=False
)
