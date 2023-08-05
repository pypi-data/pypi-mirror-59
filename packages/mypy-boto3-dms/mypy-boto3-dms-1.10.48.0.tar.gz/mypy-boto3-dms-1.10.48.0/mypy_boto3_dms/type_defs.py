"""
Main interface for dms service type definitions.

Usage::

    from mypy_boto3.dms.type_defs import PendingMaintenanceActionTypeDef

    data: PendingMaintenanceActionTypeDef = {...}
"""
from __future__ import annotations

from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "PendingMaintenanceActionTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "ApplyPendingMaintenanceActionResponseTypeDef",
    "DmsTransferSettingsTypeDef",
    "DynamoDbSettingsTypeDef",
    "ElasticsearchSettingsTypeDef",
    "KinesisSettingsTypeDef",
    "MongoDbSettingsTypeDef",
    "RedshiftSettingsTypeDef",
    "S3SettingsTypeDef",
    "EndpointTypeDef",
    "CreateEndpointResponseTypeDef",
    "EventSubscriptionTypeDef",
    "CreateEventSubscriptionResponseTypeDef",
    "ReplicationPendingModifiedValuesTypeDef",
    "AvailabilityZoneTypeDef",
    "SubnetTypeDef",
    "ReplicationSubnetGroupTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "ReplicationInstanceTypeDef",
    "CreateReplicationInstanceResponseTypeDef",
    "CreateReplicationSubnetGroupResponseTypeDef",
    "ReplicationTaskStatsTypeDef",
    "ReplicationTaskTypeDef",
    "CreateReplicationTaskResponseTypeDef",
    "CertificateTypeDef",
    "DeleteCertificateResponseTypeDef",
    "ConnectionTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DeleteEndpointResponseTypeDef",
    "DeleteEventSubscriptionResponseTypeDef",
    "DeleteReplicationInstanceResponseTypeDef",
    "DeleteReplicationTaskResponseTypeDef",
    "AccountQuotaTypeDef",
    "DescribeAccountAttributesResponseTypeDef",
    "DescribeCertificatesResponseTypeDef",
    "DescribeConnectionsResponseTypeDef",
    "SupportedEndpointTypeTypeDef",
    "DescribeEndpointTypesResponseTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "EventCategoryGroupTypeDef",
    "DescribeEventCategoriesResponseTypeDef",
    "DescribeEventSubscriptionsResponseTypeDef",
    "EventTypeDef",
    "DescribeEventsResponseTypeDef",
    "OrderableReplicationInstanceTypeDef",
    "DescribeOrderableReplicationInstancesResponseTypeDef",
    "DescribePendingMaintenanceActionsResponseTypeDef",
    "RefreshSchemasStatusTypeDef",
    "DescribeRefreshSchemasStatusResponseTypeDef",
    "ReplicationInstanceTaskLogTypeDef",
    "DescribeReplicationInstanceTaskLogsResponseTypeDef",
    "DescribeReplicationInstancesResponseTypeDef",
    "DescribeReplicationSubnetGroupsResponseTypeDef",
    "ReplicationTaskAssessmentResultTypeDef",
    "DescribeReplicationTaskAssessmentResultsResponseTypeDef",
    "DescribeReplicationTasksResponseTypeDef",
    "DescribeSchemasResponseTypeDef",
    "TableStatisticsTypeDef",
    "DescribeTableStatisticsResponseTypeDef",
    "FilterTypeDef",
    "ImportCertificateResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyEndpointResponseTypeDef",
    "ModifyEventSubscriptionResponseTypeDef",
    "ModifyReplicationInstanceResponseTypeDef",
    "ModifyReplicationSubnetGroupResponseTypeDef",
    "ModifyReplicationTaskResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RebootReplicationInstanceResponseTypeDef",
    "RefreshSchemasResponseTypeDef",
    "ReloadTablesResponseTypeDef",
    "StartReplicationTaskAssessmentResponseTypeDef",
    "StartReplicationTaskResponseTypeDef",
    "StopReplicationTaskResponseTypeDef",
    "TableToReloadTypeDef",
    "TestConnectionResponseTypeDef",
    "WaiterConfigTypeDef",
)

PendingMaintenanceActionTypeDef = TypedDict(
    "PendingMaintenanceActionTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
    total=False,
)

ResourcePendingMaintenanceActionsTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionTypeDef],
    },
    total=False,
)

ApplyPendingMaintenanceActionResponseTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResponseTypeDef",
    {"ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsTypeDef},
    total=False,
)

DmsTransferSettingsTypeDef = TypedDict(
    "DmsTransferSettingsTypeDef", {"ServiceAccessRoleArn": str, "BucketName": str}, total=False
)

DynamoDbSettingsTypeDef = TypedDict("DynamoDbSettingsTypeDef", {"ServiceAccessRoleArn": str})

_RequiredElasticsearchSettingsTypeDef = TypedDict(
    "_RequiredElasticsearchSettingsTypeDef", {"ServiceAccessRoleArn": str, "EndpointUri": str}
)
_OptionalElasticsearchSettingsTypeDef = TypedDict(
    "_OptionalElasticsearchSettingsTypeDef",
    {"FullLoadErrorPercentage": int, "ErrorRetryDuration": int},
    total=False,
)


class ElasticsearchSettingsTypeDef(
    _RequiredElasticsearchSettingsTypeDef, _OptionalElasticsearchSettingsTypeDef
):
    pass


KinesisSettingsTypeDef = TypedDict(
    "KinesisSettingsTypeDef",
    {"StreamArn": str, "MessageFormat": Literal["json"], "ServiceAccessRoleArn": str},
    total=False,
)

MongoDbSettingsTypeDef = TypedDict(
    "MongoDbSettingsTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "AuthType": Literal["no", "password"],
        "AuthMechanism": Literal["default", "mongodb_cr", "scram_sha_1"],
        "NestingLevel": Literal["none", "one"],
        "ExtractDocId": str,
        "DocsToInvestigate": str,
        "AuthSource": str,
        "KmsKeyId": str,
    },
    total=False,
)

RedshiftSettingsTypeDef = TypedDict(
    "RedshiftSettingsTypeDef",
    {
        "AcceptAnyDate": bool,
        "AfterConnectScript": str,
        "BucketFolder": str,
        "BucketName": str,
        "ConnectionTimeout": int,
        "DatabaseName": str,
        "DateFormat": str,
        "EmptyAsNull": bool,
        "EncryptionMode": Literal["sse-s3", "sse-kms"],
        "FileTransferUploadStreams": int,
        "LoadTimeout": int,
        "MaxFileSize": int,
        "Password": str,
        "Port": int,
        "RemoveQuotes": bool,
        "ReplaceInvalidChars": str,
        "ReplaceChars": str,
        "ServerName": str,
        "ServiceAccessRoleArn": str,
        "ServerSideEncryptionKmsKeyId": str,
        "TimeFormat": str,
        "TrimBlanks": bool,
        "TruncateColumns": bool,
        "Username": str,
        "WriteBufferSize": int,
    },
    total=False,
)

S3SettingsTypeDef = TypedDict(
    "S3SettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "CsvRowDelimiter": str,
        "CsvDelimiter": str,
        "BucketFolder": str,
        "BucketName": str,
        "CompressionType": Literal["none", "gzip"],
        "EncryptionMode": Literal["sse-s3", "sse-kms"],
        "ServerSideEncryptionKmsKeyId": str,
        "DataFormat": Literal["csv", "parquet"],
        "EncodingType": Literal["plain", "plain-dictionary", "rle-dictionary"],
        "DictPageSizeLimit": int,
        "RowGroupLength": int,
        "DataPageSize": int,
        "ParquetVersion": Literal["parquet-1-0", "parquet-2-0"],
        "EnableStatistics": bool,
        "IncludeOpForFullLoad": bool,
        "CdcInsertsOnly": bool,
        "TimestampColumnName": str,
        "ParquetTimestampInMillisecond": bool,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": Literal["source", "target"],
        "EngineName": str,
        "EngineDisplayName": str,
        "Username": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "Status": str,
        "KmsKeyId": str,
        "EndpointArn": str,
        "CertificateArn": str,
        "SslMode": Literal["none", "require", "verify-ca", "verify-full"],
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "ExternalId": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
    },
    total=False,
)

CreateEndpointResponseTypeDef = TypedDict(
    "CreateEndpointResponseTypeDef", {"Endpoint": EndpointTypeDef}, total=False
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
    },
    total=False,
)

CreateEventSubscriptionResponseTypeDef = TypedDict(
    "CreateEventSubscriptionResponseTypeDef",
    {"EventSubscription": EventSubscriptionTypeDef},
    total=False,
)

ReplicationPendingModifiedValuesTypeDef = TypedDict(
    "ReplicationPendingModifiedValuesTypeDef",
    {
        "ReplicationInstanceClass": str,
        "AllocatedStorage": int,
        "MultiAZ": bool,
        "EngineVersion": str,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict("AvailabilityZoneTypeDef", {"Name": str}, total=False)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

ReplicationSubnetGroupTypeDef = TypedDict(
    "ReplicationSubnetGroupTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "ReplicationSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
    },
    total=False,
)

VpcSecurityGroupMembershipTypeDef = TypedDict(
    "VpcSecurityGroupMembershipTypeDef", {"VpcSecurityGroupId": str, "Status": str}, total=False
)

ReplicationInstanceTypeDef = TypedDict(
    "ReplicationInstanceTypeDef",
    {
        "ReplicationInstanceIdentifier": str,
        "ReplicationInstanceClass": str,
        "ReplicationInstanceStatus": str,
        "AllocatedStorage": int,
        "InstanceCreateTime": datetime,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "AvailabilityZone": str,
        "ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": ReplicationPendingModifiedValuesTypeDef,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "KmsKeyId": str,
        "ReplicationInstanceArn": str,
        "ReplicationInstancePublicIpAddress": str,
        "ReplicationInstancePrivateIpAddress": str,
        "ReplicationInstancePublicIpAddresses": List[str],
        "ReplicationInstancePrivateIpAddresses": List[str],
        "PubliclyAccessible": bool,
        "SecondaryAvailabilityZone": str,
        "FreeUntil": datetime,
        "DnsNameServers": str,
    },
    total=False,
)

CreateReplicationInstanceResponseTypeDef = TypedDict(
    "CreateReplicationInstanceResponseTypeDef",
    {"ReplicationInstance": ReplicationInstanceTypeDef},
    total=False,
)

CreateReplicationSubnetGroupResponseTypeDef = TypedDict(
    "CreateReplicationSubnetGroupResponseTypeDef",
    {"ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef},
    total=False,
)

ReplicationTaskStatsTypeDef = TypedDict(
    "ReplicationTaskStatsTypeDef",
    {
        "FullLoadProgressPercent": int,
        "ElapsedTimeMillis": int,
        "TablesLoaded": int,
        "TablesLoading": int,
        "TablesQueued": int,
        "TablesErrored": int,
        "FreshStartDate": datetime,
        "StartDate": datetime,
        "StopDate": datetime,
        "FullLoadStartDate": datetime,
        "FullLoadFinishDate": datetime,
    },
    total=False,
)

ReplicationTaskTypeDef = TypedDict(
    "ReplicationTaskTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationInstanceArn": str,
        "MigrationType": Literal["full-load", "cdc", "full-load-and-cdc"],
        "TableMappings": str,
        "ReplicationTaskSettings": str,
        "Status": str,
        "LastFailureMessage": str,
        "StopReason": str,
        "ReplicationTaskCreationDate": datetime,
        "ReplicationTaskStartDate": datetime,
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "RecoveryCheckpoint": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskStats": ReplicationTaskStatsTypeDef,
    },
    total=False,
)

CreateReplicationTaskResponseTypeDef = TypedDict(
    "CreateReplicationTaskResponseTypeDef", {"ReplicationTask": ReplicationTaskTypeDef}, total=False
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateIdentifier": str,
        "CertificateCreationDate": datetime,
        "CertificatePem": str,
        "CertificateWallet": Union[bytes, IO],
        "CertificateArn": str,
        "CertificateOwner": str,
        "ValidFromDate": datetime,
        "ValidToDate": datetime,
        "SigningAlgorithm": str,
        "KeyLength": int,
    },
    total=False,
)

DeleteCertificateResponseTypeDef = TypedDict(
    "DeleteCertificateResponseTypeDef", {"Certificate": CertificateTypeDef}, total=False
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ReplicationInstanceArn": str,
        "EndpointArn": str,
        "Status": str,
        "LastFailureMessage": str,
        "EndpointIdentifier": str,
        "ReplicationInstanceIdentifier": str,
    },
    total=False,
)

DeleteConnectionResponseTypeDef = TypedDict(
    "DeleteConnectionResponseTypeDef", {"Connection": ConnectionTypeDef}, total=False
)

DeleteEndpointResponseTypeDef = TypedDict(
    "DeleteEndpointResponseTypeDef", {"Endpoint": EndpointTypeDef}, total=False
)

DeleteEventSubscriptionResponseTypeDef = TypedDict(
    "DeleteEventSubscriptionResponseTypeDef",
    {"EventSubscription": EventSubscriptionTypeDef},
    total=False,
)

DeleteReplicationInstanceResponseTypeDef = TypedDict(
    "DeleteReplicationInstanceResponseTypeDef",
    {"ReplicationInstance": ReplicationInstanceTypeDef},
    total=False,
)

DeleteReplicationTaskResponseTypeDef = TypedDict(
    "DeleteReplicationTaskResponseTypeDef", {"ReplicationTask": ReplicationTaskTypeDef}, total=False
)

AccountQuotaTypeDef = TypedDict(
    "AccountQuotaTypeDef", {"AccountQuotaName": str, "Used": int, "Max": int}, total=False
)

DescribeAccountAttributesResponseTypeDef = TypedDict(
    "DescribeAccountAttributesResponseTypeDef",
    {"AccountQuotas": List[AccountQuotaTypeDef], "UniqueAccountIdentifier": str},
    total=False,
)

DescribeCertificatesResponseTypeDef = TypedDict(
    "DescribeCertificatesResponseTypeDef",
    {"Marker": str, "Certificates": List[CertificateTypeDef]},
    total=False,
)

DescribeConnectionsResponseTypeDef = TypedDict(
    "DescribeConnectionsResponseTypeDef",
    {"Marker": str, "Connections": List[ConnectionTypeDef]},
    total=False,
)

SupportedEndpointTypeTypeDef = TypedDict(
    "SupportedEndpointTypeTypeDef",
    {
        "EngineName": str,
        "SupportsCDC": bool,
        "EndpointType": Literal["source", "target"],
        "EngineDisplayName": str,
    },
    total=False,
)

DescribeEndpointTypesResponseTypeDef = TypedDict(
    "DescribeEndpointTypesResponseTypeDef",
    {"Marker": str, "SupportedEndpointTypes": List[SupportedEndpointTypeTypeDef]},
    total=False,
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {"Marker": str, "Endpoints": List[EndpointTypeDef]},
    total=False,
)

EventCategoryGroupTypeDef = TypedDict(
    "EventCategoryGroupTypeDef", {"SourceType": str, "EventCategories": List[str]}, total=False
)

DescribeEventCategoriesResponseTypeDef = TypedDict(
    "DescribeEventCategoriesResponseTypeDef",
    {"EventCategoryGroupList": List[EventCategoryGroupTypeDef]},
    total=False,
)

DescribeEventSubscriptionsResponseTypeDef = TypedDict(
    "DescribeEventSubscriptionsResponseTypeDef",
    {"Marker": str, "EventSubscriptionsList": List[EventSubscriptionTypeDef]},
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "Message": str,
        "EventCategories": List[str],
        "Date": datetime,
    },
    total=False,
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef", {"Marker": str, "Events": List[EventTypeDef]}, total=False
)

OrderableReplicationInstanceTypeDef = TypedDict(
    "OrderableReplicationInstanceTypeDef",
    {
        "EngineVersion": str,
        "ReplicationInstanceClass": str,
        "StorageType": str,
        "MinAllocatedStorage": int,
        "MaxAllocatedStorage": int,
        "DefaultAllocatedStorage": int,
        "IncludedAllocatedStorage": int,
        "AvailabilityZones": List[str],
        "ReleaseStatus": Literal["beta"],
    },
    total=False,
)

DescribeOrderableReplicationInstancesResponseTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesResponseTypeDef",
    {"OrderableReplicationInstances": List[OrderableReplicationInstanceTypeDef], "Marker": str},
    total=False,
)

DescribePendingMaintenanceActionsResponseTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsResponseTypeDef",
    {"PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsTypeDef], "Marker": str},
    total=False,
)

RefreshSchemasStatusTypeDef = TypedDict(
    "RefreshSchemasStatusTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
        "Status": Literal["successful", "failed", "refreshing"],
        "LastRefreshDate": datetime,
        "LastFailureMessage": str,
    },
    total=False,
)

DescribeRefreshSchemasStatusResponseTypeDef = TypedDict(
    "DescribeRefreshSchemasStatusResponseTypeDef",
    {"RefreshSchemasStatus": RefreshSchemasStatusTypeDef},
    total=False,
)

ReplicationInstanceTaskLogTypeDef = TypedDict(
    "ReplicationInstanceTaskLogTypeDef",
    {"ReplicationTaskName": str, "ReplicationTaskArn": str, "ReplicationInstanceTaskLogSize": int},
    total=False,
)

DescribeReplicationInstanceTaskLogsResponseTypeDef = TypedDict(
    "DescribeReplicationInstanceTaskLogsResponseTypeDef",
    {
        "ReplicationInstanceArn": str,
        "ReplicationInstanceTaskLogs": List[ReplicationInstanceTaskLogTypeDef],
        "Marker": str,
    },
    total=False,
)

DescribeReplicationInstancesResponseTypeDef = TypedDict(
    "DescribeReplicationInstancesResponseTypeDef",
    {"Marker": str, "ReplicationInstances": List[ReplicationInstanceTypeDef]},
    total=False,
)

DescribeReplicationSubnetGroupsResponseTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsResponseTypeDef",
    {"Marker": str, "ReplicationSubnetGroups": List[ReplicationSubnetGroupTypeDef]},
    total=False,
)

ReplicationTaskAssessmentResultTypeDef = TypedDict(
    "ReplicationTaskAssessmentResultTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskLastAssessmentDate": datetime,
        "AssessmentStatus": str,
        "AssessmentResultsFile": str,
        "AssessmentResults": str,
        "S3ObjectUrl": str,
    },
    total=False,
)

DescribeReplicationTaskAssessmentResultsResponseTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsResponseTypeDef",
    {
        "Marker": str,
        "BucketName": str,
        "ReplicationTaskAssessmentResults": List[ReplicationTaskAssessmentResultTypeDef],
    },
    total=False,
)

DescribeReplicationTasksResponseTypeDef = TypedDict(
    "DescribeReplicationTasksResponseTypeDef",
    {"Marker": str, "ReplicationTasks": List[ReplicationTaskTypeDef]},
    total=False,
)

DescribeSchemasResponseTypeDef = TypedDict(
    "DescribeSchemasResponseTypeDef", {"Marker": str, "Schemas": List[str]}, total=False
)

TableStatisticsTypeDef = TypedDict(
    "TableStatisticsTypeDef",
    {
        "SchemaName": str,
        "TableName": str,
        "Inserts": int,
        "Deletes": int,
        "Updates": int,
        "Ddls": int,
        "FullLoadRows": int,
        "FullLoadCondtnlChkFailedRows": int,
        "FullLoadErrorRows": int,
        "LastUpdateTime": datetime,
        "TableState": str,
        "ValidationPendingRecords": int,
        "ValidationFailedRecords": int,
        "ValidationSuspendedRecords": int,
        "ValidationState": str,
        "ValidationStateDetails": str,
    },
    total=False,
)

DescribeTableStatisticsResponseTypeDef = TypedDict(
    "DescribeTableStatisticsResponseTypeDef",
    {"ReplicationTaskArn": str, "TableStatistics": List[TableStatisticsTypeDef], "Marker": str},
    total=False,
)

FilterTypeDef = TypedDict("FilterTypeDef", {"Name": str, "Values": List[str]})

ImportCertificateResponseTypeDef = TypedDict(
    "ImportCertificateResponseTypeDef", {"Certificate": CertificateTypeDef}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"TagList": List[TagTypeDef]}, total=False
)

ModifyEndpointResponseTypeDef = TypedDict(
    "ModifyEndpointResponseTypeDef", {"Endpoint": EndpointTypeDef}, total=False
)

ModifyEventSubscriptionResponseTypeDef = TypedDict(
    "ModifyEventSubscriptionResponseTypeDef",
    {"EventSubscription": EventSubscriptionTypeDef},
    total=False,
)

ModifyReplicationInstanceResponseTypeDef = TypedDict(
    "ModifyReplicationInstanceResponseTypeDef",
    {"ReplicationInstance": ReplicationInstanceTypeDef},
    total=False,
)

ModifyReplicationSubnetGroupResponseTypeDef = TypedDict(
    "ModifyReplicationSubnetGroupResponseTypeDef",
    {"ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef},
    total=False,
)

ModifyReplicationTaskResponseTypeDef = TypedDict(
    "ModifyReplicationTaskResponseTypeDef", {"ReplicationTask": ReplicationTaskTypeDef}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RebootReplicationInstanceResponseTypeDef = TypedDict(
    "RebootReplicationInstanceResponseTypeDef",
    {"ReplicationInstance": ReplicationInstanceTypeDef},
    total=False,
)

RefreshSchemasResponseTypeDef = TypedDict(
    "RefreshSchemasResponseTypeDef",
    {"RefreshSchemasStatus": RefreshSchemasStatusTypeDef},
    total=False,
)

ReloadTablesResponseTypeDef = TypedDict(
    "ReloadTablesResponseTypeDef", {"ReplicationTaskArn": str}, total=False
)

StartReplicationTaskAssessmentResponseTypeDef = TypedDict(
    "StartReplicationTaskAssessmentResponseTypeDef",
    {"ReplicationTask": ReplicationTaskTypeDef},
    total=False,
)

StartReplicationTaskResponseTypeDef = TypedDict(
    "StartReplicationTaskResponseTypeDef", {"ReplicationTask": ReplicationTaskTypeDef}, total=False
)

StopReplicationTaskResponseTypeDef = TypedDict(
    "StopReplicationTaskResponseTypeDef", {"ReplicationTask": ReplicationTaskTypeDef}, total=False
)

TableToReloadTypeDef = TypedDict(
    "TableToReloadTypeDef", {"SchemaName": str, "TableName": str}, total=False
)

TestConnectionResponseTypeDef = TypedDict(
    "TestConnectionResponseTypeDef", {"Connection": ConnectionTypeDef}, total=False
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
