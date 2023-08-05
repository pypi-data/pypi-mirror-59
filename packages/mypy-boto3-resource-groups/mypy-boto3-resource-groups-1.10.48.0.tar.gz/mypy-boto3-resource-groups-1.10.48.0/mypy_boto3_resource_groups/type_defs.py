"""
Main interface for resource-groups service type definitions.

Usage::

    from mypy_boto3.resource_groups.type_defs import GroupTypeDef

    data: GroupTypeDef = {...}
"""
from __future__ import annotations

import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "GroupTypeDef",
    "ResourceQueryTypeDef",
    "CreateGroupOutputTypeDef",
    "DeleteGroupOutputTypeDef",
    "GetGroupOutputTypeDef",
    "GroupQueryTypeDef",
    "GetGroupQueryOutputTypeDef",
    "GetTagsOutputTypeDef",
    "GroupFilterTypeDef",
    "QueryErrorTypeDef",
    "ResourceIdentifierTypeDef",
    "ListGroupResourcesOutputTypeDef",
    "GroupIdentifierTypeDef",
    "ListGroupsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceFilterTypeDef",
    "SearchResourcesOutputTypeDef",
    "TagOutputTypeDef",
    "UntagOutputTypeDef",
    "UpdateGroupOutputTypeDef",
    "UpdateGroupQueryOutputTypeDef",
)

_RequiredGroupTypeDef = TypedDict("_RequiredGroupTypeDef", {"GroupArn": str, "Name": str})
_OptionalGroupTypeDef = TypedDict("_OptionalGroupTypeDef", {"Description": str}, total=False)


class GroupTypeDef(_RequiredGroupTypeDef, _OptionalGroupTypeDef):
    pass


ResourceQueryTypeDef = TypedDict(
    "ResourceQueryTypeDef",
    {"Type": Literal["TAG_FILTERS_1_0", "CLOUDFORMATION_STACK_1_0"], "Query": str},
)

CreateGroupOutputTypeDef = TypedDict(
    "CreateGroupOutputTypeDef",
    {"Group": GroupTypeDef, "ResourceQuery": ResourceQueryTypeDef, "Tags": Dict[str, str]},
    total=False,
)

DeleteGroupOutputTypeDef = TypedDict(
    "DeleteGroupOutputTypeDef", {"Group": GroupTypeDef}, total=False
)

GetGroupOutputTypeDef = TypedDict("GetGroupOutputTypeDef", {"Group": GroupTypeDef}, total=False)

GroupQueryTypeDef = TypedDict(
    "GroupQueryTypeDef", {"GroupName": str, "ResourceQuery": ResourceQueryTypeDef}
)

GetGroupQueryOutputTypeDef = TypedDict(
    "GetGroupQueryOutputTypeDef", {"GroupQuery": GroupQueryTypeDef}, total=False
)

GetTagsOutputTypeDef = TypedDict(
    "GetTagsOutputTypeDef", {"Arn": str, "Tags": Dict[str, str]}, total=False
)

GroupFilterTypeDef = TypedDict(
    "GroupFilterTypeDef", {"Name": Literal["resource-type"], "Values": List[str]}
)

QueryErrorTypeDef = TypedDict(
    "QueryErrorTypeDef",
    {
        "ErrorCode": Literal["CLOUDFORMATION_STACK_INACTIVE", "CLOUDFORMATION_STACK_NOT_EXISTING"],
        "Message": str,
    },
    total=False,
)

ResourceIdentifierTypeDef = TypedDict(
    "ResourceIdentifierTypeDef", {"ResourceArn": str, "ResourceType": str}, total=False
)

ListGroupResourcesOutputTypeDef = TypedDict(
    "ListGroupResourcesOutputTypeDef",
    {
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "NextToken": str,
        "QueryErrors": List[QueryErrorTypeDef],
    },
    total=False,
)

GroupIdentifierTypeDef = TypedDict(
    "GroupIdentifierTypeDef", {"GroupName": str, "GroupArn": str}, total=False
)

ListGroupsOutputTypeDef = TypedDict(
    "ListGroupsOutputTypeDef",
    {
        "GroupIdentifiers": List[GroupIdentifierTypeDef],
        "Groups": List[GroupTypeDef],
        "NextToken": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ResourceFilterTypeDef = TypedDict(
    "ResourceFilterTypeDef", {"Name": Literal["resource-type"], "Values": List[str]}
)

SearchResourcesOutputTypeDef = TypedDict(
    "SearchResourcesOutputTypeDef",
    {
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "NextToken": str,
        "QueryErrors": List[QueryErrorTypeDef],
    },
    total=False,
)

TagOutputTypeDef = TypedDict("TagOutputTypeDef", {"Arn": str, "Tags": Dict[str, str]}, total=False)

UntagOutputTypeDef = TypedDict("UntagOutputTypeDef", {"Arn": str, "Keys": List[str]}, total=False)

UpdateGroupOutputTypeDef = TypedDict(
    "UpdateGroupOutputTypeDef", {"Group": GroupTypeDef}, total=False
)

UpdateGroupQueryOutputTypeDef = TypedDict(
    "UpdateGroupQueryOutputTypeDef", {"GroupQuery": GroupQueryTypeDef}, total=False
)
