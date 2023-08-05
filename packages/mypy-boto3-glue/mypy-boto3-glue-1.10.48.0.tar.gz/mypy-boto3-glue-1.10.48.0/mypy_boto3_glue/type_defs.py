"""
Main interface for glue service type definitions.

Usage::

    from mypy_boto3.glue.type_defs import NotificationPropertyTypeDef

    data: NotificationPropertyTypeDef = {...}
"""
from __future__ import annotations

from datetime import datetime
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
    "NotificationPropertyTypeDef",
    "ActionTypeDef",
    "ErrorDetailTypeDef",
    "PartitionErrorTypeDef",
    "BatchCreatePartitionResponseTypeDef",
    "BatchDeleteConnectionResponseTypeDef",
    "BatchDeletePartitionResponseTypeDef",
    "TableErrorTypeDef",
    "BatchDeleteTableResponseTypeDef",
    "TableVersionErrorTypeDef",
    "BatchDeleteTableVersionResponseTypeDef",
    "CatalogTargetTypeDef",
    "DynamoDBTargetTypeDef",
    "JdbcTargetTypeDef",
    "S3TargetTypeDef",
    "CrawlerTargetsTypeDef",
    "LastCrawlInfoTypeDef",
    "ScheduleTypeDef",
    "SchemaChangePolicyTypeDef",
    "CrawlerTypeDef",
    "BatchGetCrawlersResponseTypeDef",
    "DevEndpointTypeDef",
    "BatchGetDevEndpointsResponseTypeDef",
    "ConnectionsListTypeDef",
    "ExecutionPropertyTypeDef",
    "JobCommandTypeDef",
    "JobTypeDef",
    "BatchGetJobsResponseTypeDef",
    "ColumnTypeDef",
    "OrderTypeDef",
    "SerDeInfoTypeDef",
    "SkewedInfoTypeDef",
    "StorageDescriptorTypeDef",
    "PartitionTypeDef",
    "PartitionValueListTypeDef",
    "BatchGetPartitionResponseTypeDef",
    "ConditionTypeDef",
    "PredicateTypeDef",
    "TriggerTypeDef",
    "BatchGetTriggersResponseTypeDef",
    "EdgeTypeDef",
    "CrawlTypeDef",
    "CrawlerNodeDetailsTypeDef",
    "PredecessorTypeDef",
    "JobRunTypeDef",
    "JobNodeDetailsTypeDef",
    "TriggerNodeDetailsTypeDef",
    "NodeTypeDef",
    "WorkflowGraphTypeDef",
    "WorkflowRunStatisticsTypeDef",
    "WorkflowRunTypeDef",
    "WorkflowTypeDef",
    "BatchGetWorkflowsResponseTypeDef",
    "BatchStopJobRunErrorTypeDef",
    "BatchStopJobRunSuccessfulSubmissionTypeDef",
    "BatchStopJobRunResponseTypeDef",
    "CancelMLTaskRunResponseTypeDef",
    "CatalogEntryTypeDef",
    "CodeGenEdgeTypeDef",
    "CodeGenNodeArgTypeDef",
    "CodeGenNodeTypeDef",
    "PhysicalConnectionRequirementsTypeDef",
    "ConnectionInputTypeDef",
    "CreateCsvClassifierRequestTypeDef",
    "CreateDevEndpointResponseTypeDef",
    "CreateGrokClassifierRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreateJsonClassifierRequestTypeDef",
    "CreateMLTransformResponseTypeDef",
    "CreateScriptResponseTypeDef",
    "CreateSecurityConfigurationResponseTypeDef",
    "CreateTriggerResponseTypeDef",
    "CreateWorkflowResponseTypeDef",
    "CreateXMLClassifierRequestTypeDef",
    "ConnectionPasswordEncryptionTypeDef",
    "EncryptionAtRestTypeDef",
    "DataCatalogEncryptionSettingsTypeDef",
    "DataLakePrincipalTypeDef",
    "PrincipalPermissionsTypeDef",
    "DatabaseInputTypeDef",
    "DeleteJobResponseTypeDef",
    "DeleteMLTransformResponseTypeDef",
    "DeleteTriggerResponseTypeDef",
    "DeleteWorkflowResponseTypeDef",
    "DevEndpointCustomLibrariesTypeDef",
    "CloudWatchEncryptionTypeDef",
    "JobBookmarksEncryptionTypeDef",
    "S3EncryptionTypeDef",
    "EncryptionConfigurationTypeDef",
    "CatalogImportStatusTypeDef",
    "GetCatalogImportStatusResponseTypeDef",
    "CsvClassifierTypeDef",
    "GrokClassifierTypeDef",
    "JsonClassifierTypeDef",
    "XMLClassifierTypeDef",
    "ClassifierTypeDef",
    "GetClassifierResponseTypeDef",
    "GetClassifiersResponseTypeDef",
    "ConnectionTypeDef",
    "GetConnectionResponseTypeDef",
    "GetConnectionsFilterTypeDef",
    "GetConnectionsResponseTypeDef",
    "CrawlerMetricsTypeDef",
    "GetCrawlerMetricsResponseTypeDef",
    "GetCrawlerResponseTypeDef",
    "GetCrawlersResponseTypeDef",
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    "DatabaseTypeDef",
    "GetDatabaseResponseTypeDef",
    "GetDatabasesResponseTypeDef",
    "GetDataflowGraphResponseTypeDef",
    "GetDevEndpointResponseTypeDef",
    "GetDevEndpointsResponseTypeDef",
    "JobBookmarkEntryTypeDef",
    "GetJobBookmarkResponseTypeDef",
    "GetJobResponseTypeDef",
    "GetJobRunResponseTypeDef",
    "GetJobRunsResponseTypeDef",
    "GetJobsResponseTypeDef",
    "ExportLabelsTaskRunPropertiesTypeDef",
    "FindMatchesTaskRunPropertiesTypeDef",
    "ImportLabelsTaskRunPropertiesTypeDef",
    "LabelingSetGenerationTaskRunPropertiesTypeDef",
    "TaskRunPropertiesTypeDef",
    "GetMLTaskRunResponseTypeDef",
    "TaskRunTypeDef",
    "GetMLTaskRunsResponseTypeDef",
    "ConfusionMatrixTypeDef",
    "FindMatchesMetricsTypeDef",
    "EvaluationMetricsTypeDef",
    "GlueTableTypeDef",
    "SchemaColumnTypeDef",
    "FindMatchesParametersTypeDef",
    "TransformParametersTypeDef",
    "GetMLTransformResponseTypeDef",
    "MLTransformTypeDef",
    "GetMLTransformsResponseTypeDef",
    "MappingEntryTypeDef",
    "GetMappingResponseTypeDef",
    "GetPartitionResponseTypeDef",
    "GetPartitionsResponseTypeDef",
    "GetPlanResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "SecurityConfigurationTypeDef",
    "GetSecurityConfigurationResponseTypeDef",
    "GetSecurityConfigurationsResponseTypeDef",
    "TableTypeDef",
    "GetTableResponseTypeDef",
    "TableVersionTypeDef",
    "GetTableVersionResponseTypeDef",
    "GetTableVersionsResponseTypeDef",
    "GetTablesResponseTypeDef",
    "GetTagsResponseTypeDef",
    "GetTriggerResponseTypeDef",
    "GetTriggersResponseTypeDef",
    "ResourceUriTypeDef",
    "UserDefinedFunctionTypeDef",
    "GetUserDefinedFunctionResponseTypeDef",
    "GetUserDefinedFunctionsResponseTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetWorkflowRunPropertiesResponseTypeDef",
    "GetWorkflowRunResponseTypeDef",
    "GetWorkflowRunsResponseTypeDef",
    "JobUpdateTypeDef",
    "ListCrawlersResponseTypeDef",
    "ListDevEndpointsResponseTypeDef",
    "ListJobsResponseTypeDef",
    "ListTriggersResponseTypeDef",
    "ListWorkflowsResponseTypeDef",
    "LocationTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionInputTypeDef",
    "PropertyPredicateTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "ResetJobBookmarkResponseTypeDef",
    "SearchTablesResponseTypeDef",
    "SegmentTypeDef",
    "SortCriterionTypeDef",
    "StartExportLabelsTaskRunResponseTypeDef",
    "StartImportLabelsTaskRunResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "StartMLEvaluationTaskRunResponseTypeDef",
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef",
    "StartTriggerResponseTypeDef",
    "StartWorkflowRunResponseTypeDef",
    "StopTriggerResponseTypeDef",
    "TableInputTypeDef",
    "TaskRunFilterCriteriaTypeDef",
    "TaskRunSortCriteriaTypeDef",
    "TransformFilterCriteriaTypeDef",
    "TransformSortCriteriaTypeDef",
    "TriggerUpdateTypeDef",
    "UpdateCsvClassifierRequestTypeDef",
    "UpdateGrokClassifierRequestTypeDef",
    "UpdateJobResponseTypeDef",
    "UpdateJsonClassifierRequestTypeDef",
    "UpdateMLTransformResponseTypeDef",
    "UpdateTriggerResponseTypeDef",
    "UpdateWorkflowResponseTypeDef",
    "UpdateXMLClassifierRequestTypeDef",
    "UserDefinedFunctionInputTypeDef",
)

NotificationPropertyTypeDef = TypedDict(
    "NotificationPropertyTypeDef", {"NotifyDelayAfter": int}, total=False
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "JobName": str,
        "Arguments": Dict[str, str],
        "Timeout": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "CrawlerName": str,
    },
    total=False,
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef", {"ErrorCode": str, "ErrorMessage": str}, total=False
)

PartitionErrorTypeDef = TypedDict(
    "PartitionErrorTypeDef",
    {"PartitionValues": List[str], "ErrorDetail": ErrorDetailTypeDef},
    total=False,
)

BatchCreatePartitionResponseTypeDef = TypedDict(
    "BatchCreatePartitionResponseTypeDef", {"Errors": List[PartitionErrorTypeDef]}, total=False
)

BatchDeleteConnectionResponseTypeDef = TypedDict(
    "BatchDeleteConnectionResponseTypeDef",
    {"Succeeded": List[str], "Errors": Dict[str, ErrorDetailTypeDef]},
    total=False,
)

BatchDeletePartitionResponseTypeDef = TypedDict(
    "BatchDeletePartitionResponseTypeDef", {"Errors": List[PartitionErrorTypeDef]}, total=False
)

TableErrorTypeDef = TypedDict(
    "TableErrorTypeDef", {"TableName": str, "ErrorDetail": ErrorDetailTypeDef}, total=False
)

BatchDeleteTableResponseTypeDef = TypedDict(
    "BatchDeleteTableResponseTypeDef", {"Errors": List[TableErrorTypeDef]}, total=False
)

TableVersionErrorTypeDef = TypedDict(
    "TableVersionErrorTypeDef",
    {"TableName": str, "VersionId": str, "ErrorDetail": ErrorDetailTypeDef},
    total=False,
)

BatchDeleteTableVersionResponseTypeDef = TypedDict(
    "BatchDeleteTableVersionResponseTypeDef",
    {"Errors": List[TableVersionErrorTypeDef]},
    total=False,
)

CatalogTargetTypeDef = TypedDict("CatalogTargetTypeDef", {"DatabaseName": str, "Tables": List[str]})

DynamoDBTargetTypeDef = TypedDict("DynamoDBTargetTypeDef", {"Path": str}, total=False)

JdbcTargetTypeDef = TypedDict(
    "JdbcTargetTypeDef", {"ConnectionName": str, "Path": str, "Exclusions": List[str]}, total=False
)

S3TargetTypeDef = TypedDict("S3TargetTypeDef", {"Path": str, "Exclusions": List[str]}, total=False)

CrawlerTargetsTypeDef = TypedDict(
    "CrawlerTargetsTypeDef",
    {
        "S3Targets": List[S3TargetTypeDef],
        "JdbcTargets": List[JdbcTargetTypeDef],
        "DynamoDBTargets": List[DynamoDBTargetTypeDef],
        "CatalogTargets": List[CatalogTargetTypeDef],
    },
    total=False,
)

LastCrawlInfoTypeDef = TypedDict(
    "LastCrawlInfoTypeDef",
    {
        "Status": Literal["SUCCEEDED", "CANCELLED", "FAILED"],
        "ErrorMessage": str,
        "LogGroup": str,
        "LogStream": str,
        "MessagePrefix": str,
        "StartTime": datetime,
    },
    total=False,
)

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {"ScheduleExpression": str, "State": Literal["SCHEDULED", "NOT_SCHEDULED", "TRANSITIONING"]},
    total=False,
)

SchemaChangePolicyTypeDef = TypedDict(
    "SchemaChangePolicyTypeDef",
    {
        "UpdateBehavior": Literal["LOG", "UPDATE_IN_DATABASE"],
        "DeleteBehavior": Literal["LOG", "DELETE_FROM_DATABASE", "DEPRECATE_IN_DATABASE"],
    },
    total=False,
)

CrawlerTypeDef = TypedDict(
    "CrawlerTypeDef",
    {
        "Name": str,
        "Role": str,
        "Targets": CrawlerTargetsTypeDef,
        "DatabaseName": str,
        "Description": str,
        "Classifiers": List[str],
        "SchemaChangePolicy": SchemaChangePolicyTypeDef,
        "State": Literal["READY", "RUNNING", "STOPPING"],
        "TablePrefix": str,
        "Schedule": ScheduleTypeDef,
        "CrawlElapsedTime": int,
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "LastCrawl": LastCrawlInfoTypeDef,
        "Version": int,
        "Configuration": str,
        "CrawlerSecurityConfiguration": str,
    },
    total=False,
)

BatchGetCrawlersResponseTypeDef = TypedDict(
    "BatchGetCrawlersResponseTypeDef",
    {"Crawlers": List[CrawlerTypeDef], "CrawlersNotFound": List[str]},
    total=False,
)

DevEndpointTypeDef = TypedDict(
    "DevEndpointTypeDef",
    {
        "EndpointName": str,
        "RoleArn": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
        "YarnEndpointAddress": str,
        "PrivateAddress": str,
        "ZeppelinRemoteSparkInterpreterPort": int,
        "PublicAddress": str,
        "Status": str,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "NumberOfNodes": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "FailureReason": str,
        "LastUpdateStatus": str,
        "CreatedTimestamp": datetime,
        "LastModifiedTimestamp": datetime,
        "PublicKey": str,
        "PublicKeys": List[str],
        "SecurityConfiguration": str,
        "Arguments": Dict[str, str],
    },
    total=False,
)

BatchGetDevEndpointsResponseTypeDef = TypedDict(
    "BatchGetDevEndpointsResponseTypeDef",
    {"DevEndpoints": List[DevEndpointTypeDef], "DevEndpointsNotFound": List[str]},
    total=False,
)

ConnectionsListTypeDef = TypedDict(
    "ConnectionsListTypeDef", {"Connections": List[str]}, total=False
)

ExecutionPropertyTypeDef = TypedDict(
    "ExecutionPropertyTypeDef", {"MaxConcurrentRuns": int}, total=False
)

JobCommandTypeDef = TypedDict(
    "JobCommandTypeDef", {"Name": str, "ScriptLocation": str, "PythonVersion": str}, total=False
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Name": str,
        "Description": str,
        "LogUri": str,
        "Role": str,
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "ExecutionProperty": ExecutionPropertyTypeDef,
        "Command": JobCommandTypeDef,
        "DefaultArguments": Dict[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxRetries": int,
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
    },
    total=False,
)

BatchGetJobsResponseTypeDef = TypedDict(
    "BatchGetJobsResponseTypeDef",
    {"Jobs": List[JobTypeDef], "JobsNotFound": List[str]},
    total=False,
)

_RequiredColumnTypeDef = TypedDict("_RequiredColumnTypeDef", {"Name": str})
_OptionalColumnTypeDef = TypedDict(
    "_OptionalColumnTypeDef",
    {"Type": str, "Comment": str, "Parameters": Dict[str, str]},
    total=False,
)


class ColumnTypeDef(_RequiredColumnTypeDef, _OptionalColumnTypeDef):
    pass


OrderTypeDef = TypedDict("OrderTypeDef", {"Column": str, "SortOrder": int})

SerDeInfoTypeDef = TypedDict(
    "SerDeInfoTypeDef",
    {"Name": str, "SerializationLibrary": str, "Parameters": Dict[str, str]},
    total=False,
)

SkewedInfoTypeDef = TypedDict(
    "SkewedInfoTypeDef",
    {
        "SkewedColumnNames": List[str],
        "SkewedColumnValues": List[str],
        "SkewedColumnValueLocationMaps": Dict[str, str],
    },
    total=False,
)

StorageDescriptorTypeDef = TypedDict(
    "StorageDescriptorTypeDef",
    {
        "Columns": List[ColumnTypeDef],
        "Location": str,
        "InputFormat": str,
        "OutputFormat": str,
        "Compressed": bool,
        "NumberOfBuckets": int,
        "SerdeInfo": SerDeInfoTypeDef,
        "BucketColumns": List[str],
        "SortColumns": List[OrderTypeDef],
        "Parameters": Dict[str, str],
        "SkewedInfo": SkewedInfoTypeDef,
        "StoredAsSubDirectories": bool,
    },
    total=False,
)

PartitionTypeDef = TypedDict(
    "PartitionTypeDef",
    {
        "Values": List[str],
        "DatabaseName": str,
        "TableName": str,
        "CreationTime": datetime,
        "LastAccessTime": datetime,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "Parameters": Dict[str, str],
        "LastAnalyzedTime": datetime,
    },
    total=False,
)

PartitionValueListTypeDef = TypedDict("PartitionValueListTypeDef", {"Values": List[str]})

BatchGetPartitionResponseTypeDef = TypedDict(
    "BatchGetPartitionResponseTypeDef",
    {"Partitions": List[PartitionTypeDef], "UnprocessedKeys": List[PartitionValueListTypeDef]},
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "LogicalOperator": Literal["EQUALS"],
        "JobName": str,
        "State": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
        "CrawlerName": str,
        "CrawlState": Literal["RUNNING", "SUCCEEDED", "CANCELLED", "FAILED"],
    },
    total=False,
)

PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {"Logical": Literal["AND", "ANY"], "Conditions": List[ConditionTypeDef]},
    total=False,
)

TriggerTypeDef = TypedDict(
    "TriggerTypeDef",
    {
        "Name": str,
        "WorkflowName": str,
        "Id": str,
        "Type": Literal["SCHEDULED", "CONDITIONAL", "ON_DEMAND"],
        "State": Literal[
            "CREATING",
            "CREATED",
            "ACTIVATING",
            "ACTIVATED",
            "DEACTIVATING",
            "DEACTIVATED",
            "DELETING",
            "UPDATING",
        ],
        "Description": str,
        "Schedule": str,
        "Actions": List[ActionTypeDef],
        "Predicate": PredicateTypeDef,
    },
    total=False,
)

BatchGetTriggersResponseTypeDef = TypedDict(
    "BatchGetTriggersResponseTypeDef",
    {"Triggers": List[TriggerTypeDef], "TriggersNotFound": List[str]},
    total=False,
)

EdgeTypeDef = TypedDict("EdgeTypeDef", {"SourceId": str, "DestinationId": str}, total=False)

CrawlTypeDef = TypedDict(
    "CrawlTypeDef",
    {
        "State": Literal["RUNNING", "SUCCEEDED", "CANCELLED", "FAILED"],
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "ErrorMessage": str,
        "LogGroup": str,
        "LogStream": str,
    },
    total=False,
)

CrawlerNodeDetailsTypeDef = TypedDict(
    "CrawlerNodeDetailsTypeDef", {"Crawls": List[CrawlTypeDef]}, total=False
)

PredecessorTypeDef = TypedDict("PredecessorTypeDef", {"JobName": str, "RunId": str}, total=False)

JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "Id": str,
        "Attempt": int,
        "PreviousRunId": str,
        "TriggerName": str,
        "JobName": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "JobRunState": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
        "Arguments": Dict[str, str],
        "ErrorMessage": str,
        "PredecessorRuns": List[PredecessorTypeDef],
        "AllocatedCapacity": int,
        "ExecutionTime": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "LogGroupName": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
    },
    total=False,
)

JobNodeDetailsTypeDef = TypedDict(
    "JobNodeDetailsTypeDef", {"JobRuns": List[JobRunTypeDef]}, total=False
)

TriggerNodeDetailsTypeDef = TypedDict(
    "TriggerNodeDetailsTypeDef", {"Trigger": TriggerTypeDef}, total=False
)

NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "Type": Literal["CRAWLER", "JOB", "TRIGGER"],
        "Name": str,
        "UniqueId": str,
        "TriggerDetails": TriggerNodeDetailsTypeDef,
        "JobDetails": JobNodeDetailsTypeDef,
        "CrawlerDetails": CrawlerNodeDetailsTypeDef,
    },
    total=False,
)

WorkflowGraphTypeDef = TypedDict(
    "WorkflowGraphTypeDef", {"Nodes": List[NodeTypeDef], "Edges": List[EdgeTypeDef]}, total=False
)

WorkflowRunStatisticsTypeDef = TypedDict(
    "WorkflowRunStatisticsTypeDef",
    {
        "TotalActions": int,
        "TimeoutActions": int,
        "FailedActions": int,
        "StoppedActions": int,
        "SucceededActions": int,
        "RunningActions": int,
    },
    total=False,
)

WorkflowRunTypeDef = TypedDict(
    "WorkflowRunTypeDef",
    {
        "Name": str,
        "WorkflowRunId": str,
        "WorkflowRunProperties": Dict[str, str],
        "StartedOn": datetime,
        "CompletedOn": datetime,
        "Status": Literal["RUNNING", "COMPLETED"],
        "Statistics": WorkflowRunStatisticsTypeDef,
        "Graph": WorkflowGraphTypeDef,
    },
    total=False,
)

WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "Name": str,
        "Description": str,
        "DefaultRunProperties": Dict[str, str],
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "LastRun": WorkflowRunTypeDef,
        "Graph": WorkflowGraphTypeDef,
    },
    total=False,
)

BatchGetWorkflowsResponseTypeDef = TypedDict(
    "BatchGetWorkflowsResponseTypeDef",
    {"Workflows": List[WorkflowTypeDef], "MissingWorkflows": List[str]},
    total=False,
)

BatchStopJobRunErrorTypeDef = TypedDict(
    "BatchStopJobRunErrorTypeDef",
    {"JobName": str, "JobRunId": str, "ErrorDetail": ErrorDetailTypeDef},
    total=False,
)

BatchStopJobRunSuccessfulSubmissionTypeDef = TypedDict(
    "BatchStopJobRunSuccessfulSubmissionTypeDef", {"JobName": str, "JobRunId": str}, total=False
)

BatchStopJobRunResponseTypeDef = TypedDict(
    "BatchStopJobRunResponseTypeDef",
    {
        "SuccessfulSubmissions": List[BatchStopJobRunSuccessfulSubmissionTypeDef],
        "Errors": List[BatchStopJobRunErrorTypeDef],
    },
    total=False,
)

CancelMLTaskRunResponseTypeDef = TypedDict(
    "CancelMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
    },
    total=False,
)

CatalogEntryTypeDef = TypedDict("CatalogEntryTypeDef", {"DatabaseName": str, "TableName": str})

_RequiredCodeGenEdgeTypeDef = TypedDict(
    "_RequiredCodeGenEdgeTypeDef", {"Source": str, "Target": str}
)
_OptionalCodeGenEdgeTypeDef = TypedDict(
    "_OptionalCodeGenEdgeTypeDef", {"TargetParameter": str}, total=False
)


class CodeGenEdgeTypeDef(_RequiredCodeGenEdgeTypeDef, _OptionalCodeGenEdgeTypeDef):
    pass


_RequiredCodeGenNodeArgTypeDef = TypedDict(
    "_RequiredCodeGenNodeArgTypeDef", {"Name": str, "Value": str}
)
_OptionalCodeGenNodeArgTypeDef = TypedDict(
    "_OptionalCodeGenNodeArgTypeDef", {"Param": bool}, total=False
)


class CodeGenNodeArgTypeDef(_RequiredCodeGenNodeArgTypeDef, _OptionalCodeGenNodeArgTypeDef):
    pass


_RequiredCodeGenNodeTypeDef = TypedDict(
    "_RequiredCodeGenNodeTypeDef", {"Id": str, "NodeType": str, "Args": List[CodeGenNodeArgTypeDef]}
)
_OptionalCodeGenNodeTypeDef = TypedDict(
    "_OptionalCodeGenNodeTypeDef", {"LineNumber": int}, total=False
)


class CodeGenNodeTypeDef(_RequiredCodeGenNodeTypeDef, _OptionalCodeGenNodeTypeDef):
    pass


PhysicalConnectionRequirementsTypeDef = TypedDict(
    "PhysicalConnectionRequirementsTypeDef",
    {"SubnetId": str, "SecurityGroupIdList": List[str], "AvailabilityZone": str},
    total=False,
)

_RequiredConnectionInputTypeDef = TypedDict(
    "_RequiredConnectionInputTypeDef",
    {
        "Name": str,
        "ConnectionType": Literal["JDBC", "SFTP"],
        "ConnectionProperties": Dict[
            Literal[
                "HOST",
                "PORT",
                "USERNAME",
                "PASSWORD",
                "ENCRYPTED_PASSWORD",
                "JDBC_DRIVER_JAR_URI",
                "JDBC_DRIVER_CLASS_NAME",
                "JDBC_ENGINE",
                "JDBC_ENGINE_VERSION",
                "CONFIG_FILES",
                "INSTANCE_ID",
                "JDBC_CONNECTION_URL",
                "JDBC_ENFORCE_SSL",
                "CUSTOM_JDBC_CERT",
                "SKIP_CUSTOM_JDBC_CERT_VALIDATION",
                "CUSTOM_JDBC_CERT_STRING",
            ],
            str,
        ],
    },
)
_OptionalConnectionInputTypeDef = TypedDict(
    "_OptionalConnectionInputTypeDef",
    {
        "Description": str,
        "MatchCriteria": List[str],
        "PhysicalConnectionRequirements": PhysicalConnectionRequirementsTypeDef,
    },
    total=False,
)


class ConnectionInputTypeDef(_RequiredConnectionInputTypeDef, _OptionalConnectionInputTypeDef):
    pass


_RequiredCreateCsvClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateCsvClassifierRequestTypeDef", {"Name": str}
)
_OptionalCreateCsvClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateCsvClassifierRequestTypeDef",
    {
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": Literal["UNKNOWN", "PRESENT", "ABSENT"],
        "Header": List[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class CreateCsvClassifierRequestTypeDef(
    _RequiredCreateCsvClassifierRequestTypeDef, _OptionalCreateCsvClassifierRequestTypeDef
):
    pass


CreateDevEndpointResponseTypeDef = TypedDict(
    "CreateDevEndpointResponseTypeDef",
    {
        "EndpointName": str,
        "Status": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
        "RoleArn": str,
        "YarnEndpointAddress": str,
        "ZeppelinRemoteSparkInterpreterPort": int,
        "NumberOfNodes": int,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "GlueVersion": str,
        "NumberOfWorkers": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "ExtraPythonLibsS3Path": str,
        "ExtraJarsS3Path": str,
        "FailureReason": str,
        "SecurityConfiguration": str,
        "CreatedTimestamp": datetime,
        "Arguments": Dict[str, str],
    },
    total=False,
)

_RequiredCreateGrokClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateGrokClassifierRequestTypeDef",
    {"Classification": str, "Name": str, "GrokPattern": str},
)
_OptionalCreateGrokClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateGrokClassifierRequestTypeDef", {"CustomPatterns": str}, total=False
)


class CreateGrokClassifierRequestTypeDef(
    _RequiredCreateGrokClassifierRequestTypeDef, _OptionalCreateGrokClassifierRequestTypeDef
):
    pass


CreateJobResponseTypeDef = TypedDict("CreateJobResponseTypeDef", {"Name": str}, total=False)

CreateJsonClassifierRequestTypeDef = TypedDict(
    "CreateJsonClassifierRequestTypeDef", {"Name": str, "JsonPath": str}
)

CreateMLTransformResponseTypeDef = TypedDict(
    "CreateMLTransformResponseTypeDef", {"TransformId": str}, total=False
)

CreateScriptResponseTypeDef = TypedDict(
    "CreateScriptResponseTypeDef", {"PythonScript": str, "ScalaCode": str}, total=False
)

CreateSecurityConfigurationResponseTypeDef = TypedDict(
    "CreateSecurityConfigurationResponseTypeDef",
    {"Name": str, "CreatedTimestamp": datetime},
    total=False,
)

CreateTriggerResponseTypeDef = TypedDict("CreateTriggerResponseTypeDef", {"Name": str}, total=False)

CreateWorkflowResponseTypeDef = TypedDict(
    "CreateWorkflowResponseTypeDef", {"Name": str}, total=False
)

_RequiredCreateXMLClassifierRequestTypeDef = TypedDict(
    "_RequiredCreateXMLClassifierRequestTypeDef", {"Classification": str, "Name": str}
)
_OptionalCreateXMLClassifierRequestTypeDef = TypedDict(
    "_OptionalCreateXMLClassifierRequestTypeDef", {"RowTag": str}, total=False
)


class CreateXMLClassifierRequestTypeDef(
    _RequiredCreateXMLClassifierRequestTypeDef, _OptionalCreateXMLClassifierRequestTypeDef
):
    pass


_RequiredConnectionPasswordEncryptionTypeDef = TypedDict(
    "_RequiredConnectionPasswordEncryptionTypeDef", {"ReturnConnectionPasswordEncrypted": bool}
)
_OptionalConnectionPasswordEncryptionTypeDef = TypedDict(
    "_OptionalConnectionPasswordEncryptionTypeDef", {"AwsKmsKeyId": str}, total=False
)


class ConnectionPasswordEncryptionTypeDef(
    _RequiredConnectionPasswordEncryptionTypeDef, _OptionalConnectionPasswordEncryptionTypeDef
):
    pass


_RequiredEncryptionAtRestTypeDef = TypedDict(
    "_RequiredEncryptionAtRestTypeDef", {"CatalogEncryptionMode": Literal["DISABLED", "SSE-KMS"]}
)
_OptionalEncryptionAtRestTypeDef = TypedDict(
    "_OptionalEncryptionAtRestTypeDef", {"SseAwsKmsKeyId": str}, total=False
)


class EncryptionAtRestTypeDef(_RequiredEncryptionAtRestTypeDef, _OptionalEncryptionAtRestTypeDef):
    pass


DataCatalogEncryptionSettingsTypeDef = TypedDict(
    "DataCatalogEncryptionSettingsTypeDef",
    {
        "EncryptionAtRest": EncryptionAtRestTypeDef,
        "ConnectionPasswordEncryption": ConnectionPasswordEncryptionTypeDef,
    },
    total=False,
)

DataLakePrincipalTypeDef = TypedDict(
    "DataLakePrincipalTypeDef", {"DataLakePrincipalIdentifier": str}, total=False
)

PrincipalPermissionsTypeDef = TypedDict(
    "PrincipalPermissionsTypeDef",
    {
        "Principal": DataLakePrincipalTypeDef,
        "Permissions": List[
            Literal[
                "ALL",
                "SELECT",
                "ALTER",
                "DROP",
                "DELETE",
                "INSERT",
                "CREATE_DATABASE",
                "CREATE_TABLE",
                "DATA_LOCATION_ACCESS",
            ]
        ],
    },
    total=False,
)

_RequiredDatabaseInputTypeDef = TypedDict("_RequiredDatabaseInputTypeDef", {"Name": str})
_OptionalDatabaseInputTypeDef = TypedDict(
    "_OptionalDatabaseInputTypeDef",
    {
        "Description": str,
        "LocationUri": str,
        "Parameters": Dict[str, str],
        "CreateTableDefaultPermissions": List[PrincipalPermissionsTypeDef],
    },
    total=False,
)


class DatabaseInputTypeDef(_RequiredDatabaseInputTypeDef, _OptionalDatabaseInputTypeDef):
    pass


DeleteJobResponseTypeDef = TypedDict("DeleteJobResponseTypeDef", {"JobName": str}, total=False)

DeleteMLTransformResponseTypeDef = TypedDict(
    "DeleteMLTransformResponseTypeDef", {"TransformId": str}, total=False
)

DeleteTriggerResponseTypeDef = TypedDict("DeleteTriggerResponseTypeDef", {"Name": str}, total=False)

DeleteWorkflowResponseTypeDef = TypedDict(
    "DeleteWorkflowResponseTypeDef", {"Name": str}, total=False
)

DevEndpointCustomLibrariesTypeDef = TypedDict(
    "DevEndpointCustomLibrariesTypeDef",
    {"ExtraPythonLibsS3Path": str, "ExtraJarsS3Path": str},
    total=False,
)

CloudWatchEncryptionTypeDef = TypedDict(
    "CloudWatchEncryptionTypeDef",
    {"CloudWatchEncryptionMode": Literal["DISABLED", "SSE-KMS"], "KmsKeyArn": str},
    total=False,
)

JobBookmarksEncryptionTypeDef = TypedDict(
    "JobBookmarksEncryptionTypeDef",
    {"JobBookmarksEncryptionMode": Literal["DISABLED", "CSE-KMS"], "KmsKeyArn": str},
    total=False,
)

S3EncryptionTypeDef = TypedDict(
    "S3EncryptionTypeDef",
    {"S3EncryptionMode": Literal["DISABLED", "SSE-KMS", "SSE-S3"], "KmsKeyArn": str},
    total=False,
)

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "S3Encryption": List[S3EncryptionTypeDef],
        "CloudWatchEncryption": CloudWatchEncryptionTypeDef,
        "JobBookmarksEncryption": JobBookmarksEncryptionTypeDef,
    },
    total=False,
)

CatalogImportStatusTypeDef = TypedDict(
    "CatalogImportStatusTypeDef",
    {"ImportCompleted": bool, "ImportTime": datetime, "ImportedBy": str},
    total=False,
)

GetCatalogImportStatusResponseTypeDef = TypedDict(
    "GetCatalogImportStatusResponseTypeDef",
    {"ImportStatus": CatalogImportStatusTypeDef},
    total=False,
)

_RequiredCsvClassifierTypeDef = TypedDict("_RequiredCsvClassifierTypeDef", {"Name": str})
_OptionalCsvClassifierTypeDef = TypedDict(
    "_OptionalCsvClassifierTypeDef",
    {
        "CreationTime": datetime,
        "LastUpdated": datetime,
        "Version": int,
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": Literal["UNKNOWN", "PRESENT", "ABSENT"],
        "Header": List[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class CsvClassifierTypeDef(_RequiredCsvClassifierTypeDef, _OptionalCsvClassifierTypeDef):
    pass


_RequiredGrokClassifierTypeDef = TypedDict(
    "_RequiredGrokClassifierTypeDef", {"Name": str, "Classification": str, "GrokPattern": str}
)
_OptionalGrokClassifierTypeDef = TypedDict(
    "_OptionalGrokClassifierTypeDef",
    {"CreationTime": datetime, "LastUpdated": datetime, "Version": int, "CustomPatterns": str},
    total=False,
)


class GrokClassifierTypeDef(_RequiredGrokClassifierTypeDef, _OptionalGrokClassifierTypeDef):
    pass


_RequiredJsonClassifierTypeDef = TypedDict(
    "_RequiredJsonClassifierTypeDef", {"Name": str, "JsonPath": str}
)
_OptionalJsonClassifierTypeDef = TypedDict(
    "_OptionalJsonClassifierTypeDef",
    {"CreationTime": datetime, "LastUpdated": datetime, "Version": int},
    total=False,
)


class JsonClassifierTypeDef(_RequiredJsonClassifierTypeDef, _OptionalJsonClassifierTypeDef):
    pass


_RequiredXMLClassifierTypeDef = TypedDict(
    "_RequiredXMLClassifierTypeDef", {"Name": str, "Classification": str}
)
_OptionalXMLClassifierTypeDef = TypedDict(
    "_OptionalXMLClassifierTypeDef",
    {"CreationTime": datetime, "LastUpdated": datetime, "Version": int, "RowTag": str},
    total=False,
)


class XMLClassifierTypeDef(_RequiredXMLClassifierTypeDef, _OptionalXMLClassifierTypeDef):
    pass


ClassifierTypeDef = TypedDict(
    "ClassifierTypeDef",
    {
        "GrokClassifier": GrokClassifierTypeDef,
        "XMLClassifier": XMLClassifierTypeDef,
        "JsonClassifier": JsonClassifierTypeDef,
        "CsvClassifier": CsvClassifierTypeDef,
    },
    total=False,
)

GetClassifierResponseTypeDef = TypedDict(
    "GetClassifierResponseTypeDef", {"Classifier": ClassifierTypeDef}, total=False
)

GetClassifiersResponseTypeDef = TypedDict(
    "GetClassifiersResponseTypeDef",
    {"Classifiers": List[ClassifierTypeDef], "NextToken": str},
    total=False,
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "Name": str,
        "Description": str,
        "ConnectionType": Literal["JDBC", "SFTP"],
        "MatchCriteria": List[str],
        "ConnectionProperties": Dict[
            Literal[
                "HOST",
                "PORT",
                "USERNAME",
                "PASSWORD",
                "ENCRYPTED_PASSWORD",
                "JDBC_DRIVER_JAR_URI",
                "JDBC_DRIVER_CLASS_NAME",
                "JDBC_ENGINE",
                "JDBC_ENGINE_VERSION",
                "CONFIG_FILES",
                "INSTANCE_ID",
                "JDBC_CONNECTION_URL",
                "JDBC_ENFORCE_SSL",
                "CUSTOM_JDBC_CERT",
                "SKIP_CUSTOM_JDBC_CERT_VALIDATION",
                "CUSTOM_JDBC_CERT_STRING",
            ],
            str,
        ],
        "PhysicalConnectionRequirements": PhysicalConnectionRequirementsTypeDef,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "LastUpdatedBy": str,
    },
    total=False,
)

GetConnectionResponseTypeDef = TypedDict(
    "GetConnectionResponseTypeDef", {"Connection": ConnectionTypeDef}, total=False
)

GetConnectionsFilterTypeDef = TypedDict(
    "GetConnectionsFilterTypeDef",
    {"MatchCriteria": List[str], "ConnectionType": Literal["JDBC", "SFTP"]},
    total=False,
)

GetConnectionsResponseTypeDef = TypedDict(
    "GetConnectionsResponseTypeDef",
    {"ConnectionList": List[ConnectionTypeDef], "NextToken": str},
    total=False,
)

CrawlerMetricsTypeDef = TypedDict(
    "CrawlerMetricsTypeDef",
    {
        "CrawlerName": str,
        "TimeLeftSeconds": float,
        "StillEstimating": bool,
        "LastRuntimeSeconds": float,
        "MedianRuntimeSeconds": float,
        "TablesCreated": int,
        "TablesUpdated": int,
        "TablesDeleted": int,
    },
    total=False,
)

GetCrawlerMetricsResponseTypeDef = TypedDict(
    "GetCrawlerMetricsResponseTypeDef",
    {"CrawlerMetricsList": List[CrawlerMetricsTypeDef], "NextToken": str},
    total=False,
)

GetCrawlerResponseTypeDef = TypedDict(
    "GetCrawlerResponseTypeDef", {"Crawler": CrawlerTypeDef}, total=False
)

GetCrawlersResponseTypeDef = TypedDict(
    "GetCrawlersResponseTypeDef", {"Crawlers": List[CrawlerTypeDef], "NextToken": str}, total=False
)

GetDataCatalogEncryptionSettingsResponseTypeDef = TypedDict(
    "GetDataCatalogEncryptionSettingsResponseTypeDef",
    {"DataCatalogEncryptionSettings": DataCatalogEncryptionSettingsTypeDef},
    total=False,
)

_RequiredDatabaseTypeDef = TypedDict("_RequiredDatabaseTypeDef", {"Name": str})
_OptionalDatabaseTypeDef = TypedDict(
    "_OptionalDatabaseTypeDef",
    {
        "Description": str,
        "LocationUri": str,
        "Parameters": Dict[str, str],
        "CreateTime": datetime,
        "CreateTableDefaultPermissions": List[PrincipalPermissionsTypeDef],
    },
    total=False,
)


class DatabaseTypeDef(_RequiredDatabaseTypeDef, _OptionalDatabaseTypeDef):
    pass


GetDatabaseResponseTypeDef = TypedDict(
    "GetDatabaseResponseTypeDef", {"Database": DatabaseTypeDef}, total=False
)

_RequiredGetDatabasesResponseTypeDef = TypedDict(
    "_RequiredGetDatabasesResponseTypeDef", {"DatabaseList": List[DatabaseTypeDef]}
)
_OptionalGetDatabasesResponseTypeDef = TypedDict(
    "_OptionalGetDatabasesResponseTypeDef", {"NextToken": str}, total=False
)


class GetDatabasesResponseTypeDef(
    _RequiredGetDatabasesResponseTypeDef, _OptionalGetDatabasesResponseTypeDef
):
    pass


GetDataflowGraphResponseTypeDef = TypedDict(
    "GetDataflowGraphResponseTypeDef",
    {"DagNodes": List[CodeGenNodeTypeDef], "DagEdges": List[CodeGenEdgeTypeDef]},
    total=False,
)

GetDevEndpointResponseTypeDef = TypedDict(
    "GetDevEndpointResponseTypeDef", {"DevEndpoint": DevEndpointTypeDef}, total=False
)

GetDevEndpointsResponseTypeDef = TypedDict(
    "GetDevEndpointsResponseTypeDef",
    {"DevEndpoints": List[DevEndpointTypeDef], "NextToken": str},
    total=False,
)

JobBookmarkEntryTypeDef = TypedDict(
    "JobBookmarkEntryTypeDef",
    {
        "JobName": str,
        "Version": int,
        "Run": int,
        "Attempt": int,
        "PreviousRunId": str,
        "RunId": str,
        "JobBookmark": str,
    },
    total=False,
)

GetJobBookmarkResponseTypeDef = TypedDict(
    "GetJobBookmarkResponseTypeDef", {"JobBookmarkEntry": JobBookmarkEntryTypeDef}, total=False
)

GetJobResponseTypeDef = TypedDict("GetJobResponseTypeDef", {"Job": JobTypeDef}, total=False)

GetJobRunResponseTypeDef = TypedDict(
    "GetJobRunResponseTypeDef", {"JobRun": JobRunTypeDef}, total=False
)

GetJobRunsResponseTypeDef = TypedDict(
    "GetJobRunsResponseTypeDef", {"JobRuns": List[JobRunTypeDef], "NextToken": str}, total=False
)

GetJobsResponseTypeDef = TypedDict(
    "GetJobsResponseTypeDef", {"Jobs": List[JobTypeDef], "NextToken": str}, total=False
)

ExportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ExportLabelsTaskRunPropertiesTypeDef", {"OutputS3Path": str}, total=False
)

FindMatchesTaskRunPropertiesTypeDef = TypedDict(
    "FindMatchesTaskRunPropertiesTypeDef",
    {"JobId": str, "JobName": str, "JobRunId": str},
    total=False,
)

ImportLabelsTaskRunPropertiesTypeDef = TypedDict(
    "ImportLabelsTaskRunPropertiesTypeDef", {"InputS3Path": str, "Replace": bool}, total=False
)

LabelingSetGenerationTaskRunPropertiesTypeDef = TypedDict(
    "LabelingSetGenerationTaskRunPropertiesTypeDef", {"OutputS3Path": str}, total=False
)

TaskRunPropertiesTypeDef = TypedDict(
    "TaskRunPropertiesTypeDef",
    {
        "TaskType": Literal[
            "EVALUATION",
            "LABELING_SET_GENERATION",
            "IMPORT_LABELS",
            "EXPORT_LABELS",
            "FIND_MATCHES",
        ],
        "ImportLabelsTaskRunProperties": ImportLabelsTaskRunPropertiesTypeDef,
        "ExportLabelsTaskRunProperties": ExportLabelsTaskRunPropertiesTypeDef,
        "LabelingSetGenerationTaskRunProperties": LabelingSetGenerationTaskRunPropertiesTypeDef,
        "FindMatchesTaskRunProperties": FindMatchesTaskRunPropertiesTypeDef,
    },
    total=False,
)

GetMLTaskRunResponseTypeDef = TypedDict(
    "GetMLTaskRunResponseTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
        "LogGroupName": str,
        "Properties": TaskRunPropertiesTypeDef,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
    },
    total=False,
)

TaskRunTypeDef = TypedDict(
    "TaskRunTypeDef",
    {
        "TransformId": str,
        "TaskRunId": str,
        "Status": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
        "LogGroupName": str,
        "Properties": TaskRunPropertiesTypeDef,
        "ErrorString": str,
        "StartedOn": datetime,
        "LastModifiedOn": datetime,
        "CompletedOn": datetime,
        "ExecutionTime": int,
    },
    total=False,
)

GetMLTaskRunsResponseTypeDef = TypedDict(
    "GetMLTaskRunsResponseTypeDef",
    {"TaskRuns": List[TaskRunTypeDef], "NextToken": str},
    total=False,
)

ConfusionMatrixTypeDef = TypedDict(
    "ConfusionMatrixTypeDef",
    {
        "NumTruePositives": int,
        "NumFalsePositives": int,
        "NumTrueNegatives": int,
        "NumFalseNegatives": int,
    },
    total=False,
)

FindMatchesMetricsTypeDef = TypedDict(
    "FindMatchesMetricsTypeDef",
    {
        "AreaUnderPRCurve": float,
        "Precision": float,
        "Recall": float,
        "F1": float,
        "ConfusionMatrix": ConfusionMatrixTypeDef,
    },
    total=False,
)

_RequiredEvaluationMetricsTypeDef = TypedDict(
    "_RequiredEvaluationMetricsTypeDef", {"TransformType": Literal["FIND_MATCHES"]}
)
_OptionalEvaluationMetricsTypeDef = TypedDict(
    "_OptionalEvaluationMetricsTypeDef",
    {"FindMatchesMetrics": FindMatchesMetricsTypeDef},
    total=False,
)


class EvaluationMetricsTypeDef(
    _RequiredEvaluationMetricsTypeDef, _OptionalEvaluationMetricsTypeDef
):
    pass


_RequiredGlueTableTypeDef = TypedDict(
    "_RequiredGlueTableTypeDef", {"DatabaseName": str, "TableName": str}
)
_OptionalGlueTableTypeDef = TypedDict(
    "_OptionalGlueTableTypeDef", {"CatalogId": str, "ConnectionName": str}, total=False
)


class GlueTableTypeDef(_RequiredGlueTableTypeDef, _OptionalGlueTableTypeDef):
    pass


SchemaColumnTypeDef = TypedDict("SchemaColumnTypeDef", {"Name": str, "DataType": str}, total=False)

FindMatchesParametersTypeDef = TypedDict(
    "FindMatchesParametersTypeDef",
    {
        "PrimaryKeyColumnName": str,
        "PrecisionRecallTradeoff": float,
        "AccuracyCostTradeoff": float,
        "EnforceProvidedLabels": bool,
    },
    total=False,
)

_RequiredTransformParametersTypeDef = TypedDict(
    "_RequiredTransformParametersTypeDef", {"TransformType": Literal["FIND_MATCHES"]}
)
_OptionalTransformParametersTypeDef = TypedDict(
    "_OptionalTransformParametersTypeDef",
    {"FindMatchesParameters": FindMatchesParametersTypeDef},
    total=False,
)


class TransformParametersTypeDef(
    _RequiredTransformParametersTypeDef, _OptionalTransformParametersTypeDef
):
    pass


GetMLTransformResponseTypeDef = TypedDict(
    "GetMLTransformResponseTypeDef",
    {
        "TransformId": str,
        "Name": str,
        "Description": str,
        "Status": Literal["NOT_READY", "READY", "DELETING"],
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "InputRecordTables": List[GlueTableTypeDef],
        "Parameters": TransformParametersTypeDef,
        "EvaluationMetrics": EvaluationMetricsTypeDef,
        "LabelCount": int,
        "Schema": List[SchemaColumnTypeDef],
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
    },
    total=False,
)

MLTransformTypeDef = TypedDict(
    "MLTransformTypeDef",
    {
        "TransformId": str,
        "Name": str,
        "Description": str,
        "Status": Literal["NOT_READY", "READY", "DELETING"],
        "CreatedOn": datetime,
        "LastModifiedOn": datetime,
        "InputRecordTables": List[GlueTableTypeDef],
        "Parameters": TransformParametersTypeDef,
        "EvaluationMetrics": EvaluationMetricsTypeDef,
        "LabelCount": int,
        "Schema": List[SchemaColumnTypeDef],
        "Role": str,
        "GlueVersion": str,
        "MaxCapacity": float,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "NumberOfWorkers": int,
        "Timeout": int,
        "MaxRetries": int,
    },
    total=False,
)

_RequiredGetMLTransformsResponseTypeDef = TypedDict(
    "_RequiredGetMLTransformsResponseTypeDef", {"Transforms": List[MLTransformTypeDef]}
)
_OptionalGetMLTransformsResponseTypeDef = TypedDict(
    "_OptionalGetMLTransformsResponseTypeDef", {"NextToken": str}, total=False
)


class GetMLTransformsResponseTypeDef(
    _RequiredGetMLTransformsResponseTypeDef, _OptionalGetMLTransformsResponseTypeDef
):
    pass


MappingEntryTypeDef = TypedDict(
    "MappingEntryTypeDef",
    {
        "SourceTable": str,
        "SourcePath": str,
        "SourceType": str,
        "TargetTable": str,
        "TargetPath": str,
        "TargetType": str,
    },
    total=False,
)

GetMappingResponseTypeDef = TypedDict(
    "GetMappingResponseTypeDef", {"Mapping": List[MappingEntryTypeDef]}
)

GetPartitionResponseTypeDef = TypedDict(
    "GetPartitionResponseTypeDef", {"Partition": PartitionTypeDef}, total=False
)

GetPartitionsResponseTypeDef = TypedDict(
    "GetPartitionsResponseTypeDef",
    {"Partitions": List[PartitionTypeDef], "NextToken": str},
    total=False,
)

GetPlanResponseTypeDef = TypedDict(
    "GetPlanResponseTypeDef", {"PythonScript": str, "ScalaCode": str}, total=False
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {"PolicyInJson": str, "PolicyHash": str, "CreateTime": datetime, "UpdateTime": datetime},
    total=False,
)

SecurityConfigurationTypeDef = TypedDict(
    "SecurityConfigurationTypeDef",
    {
        "Name": str,
        "CreatedTimeStamp": datetime,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)

GetSecurityConfigurationResponseTypeDef = TypedDict(
    "GetSecurityConfigurationResponseTypeDef",
    {"SecurityConfiguration": SecurityConfigurationTypeDef},
    total=False,
)

GetSecurityConfigurationsResponseTypeDef = TypedDict(
    "GetSecurityConfigurationsResponseTypeDef",
    {"SecurityConfigurations": List[SecurityConfigurationTypeDef], "NextToken": str},
    total=False,
)

_RequiredTableTypeDef = TypedDict("_RequiredTableTypeDef", {"Name": str})
_OptionalTableTypeDef = TypedDict(
    "_OptionalTableTypeDef",
    {
        "DatabaseName": str,
        "Description": str,
        "Owner": str,
        "CreateTime": datetime,
        "UpdateTime": datetime,
        "LastAccessTime": datetime,
        "LastAnalyzedTime": datetime,
        "Retention": int,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "PartitionKeys": List[ColumnTypeDef],
        "ViewOriginalText": str,
        "ViewExpandedText": str,
        "TableType": str,
        "Parameters": Dict[str, str],
        "CreatedBy": str,
        "IsRegisteredWithLakeFormation": bool,
    },
    total=False,
)


class TableTypeDef(_RequiredTableTypeDef, _OptionalTableTypeDef):
    pass


GetTableResponseTypeDef = TypedDict("GetTableResponseTypeDef", {"Table": TableTypeDef}, total=False)

TableVersionTypeDef = TypedDict(
    "TableVersionTypeDef", {"Table": TableTypeDef, "VersionId": str}, total=False
)

GetTableVersionResponseTypeDef = TypedDict(
    "GetTableVersionResponseTypeDef", {"TableVersion": TableVersionTypeDef}, total=False
)

GetTableVersionsResponseTypeDef = TypedDict(
    "GetTableVersionsResponseTypeDef",
    {"TableVersions": List[TableVersionTypeDef], "NextToken": str},
    total=False,
)

GetTablesResponseTypeDef = TypedDict(
    "GetTablesResponseTypeDef", {"TableList": List[TableTypeDef], "NextToken": str}, total=False
)

GetTagsResponseTypeDef = TypedDict("GetTagsResponseTypeDef", {"Tags": Dict[str, str]}, total=False)

GetTriggerResponseTypeDef = TypedDict(
    "GetTriggerResponseTypeDef", {"Trigger": TriggerTypeDef}, total=False
)

GetTriggersResponseTypeDef = TypedDict(
    "GetTriggersResponseTypeDef", {"Triggers": List[TriggerTypeDef], "NextToken": str}, total=False
)

ResourceUriTypeDef = TypedDict(
    "ResourceUriTypeDef",
    {"ResourceType": Literal["JAR", "FILE", "ARCHIVE"], "Uri": str},
    total=False,
)

UserDefinedFunctionTypeDef = TypedDict(
    "UserDefinedFunctionTypeDef",
    {
        "FunctionName": str,
        "ClassName": str,
        "OwnerName": str,
        "OwnerType": Literal["USER", "ROLE", "GROUP"],
        "CreateTime": datetime,
        "ResourceUris": List[ResourceUriTypeDef],
    },
    total=False,
)

GetUserDefinedFunctionResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionResponseTypeDef",
    {"UserDefinedFunction": UserDefinedFunctionTypeDef},
    total=False,
)

GetUserDefinedFunctionsResponseTypeDef = TypedDict(
    "GetUserDefinedFunctionsResponseTypeDef",
    {"UserDefinedFunctions": List[UserDefinedFunctionTypeDef], "NextToken": str},
    total=False,
)

GetWorkflowResponseTypeDef = TypedDict(
    "GetWorkflowResponseTypeDef", {"Workflow": WorkflowTypeDef}, total=False
)

GetWorkflowRunPropertiesResponseTypeDef = TypedDict(
    "GetWorkflowRunPropertiesResponseTypeDef", {"RunProperties": Dict[str, str]}, total=False
)

GetWorkflowRunResponseTypeDef = TypedDict(
    "GetWorkflowRunResponseTypeDef", {"Run": WorkflowRunTypeDef}, total=False
)

GetWorkflowRunsResponseTypeDef = TypedDict(
    "GetWorkflowRunsResponseTypeDef",
    {"Runs": List[WorkflowRunTypeDef], "NextToken": str},
    total=False,
)

JobUpdateTypeDef = TypedDict(
    "JobUpdateTypeDef",
    {
        "Description": str,
        "LogUri": str,
        "Role": str,
        "ExecutionProperty": ExecutionPropertyTypeDef,
        "Command": JobCommandTypeDef,
        "DefaultArguments": Dict[str, str],
        "Connections": ConnectionsListTypeDef,
        "MaxRetries": int,
        "AllocatedCapacity": int,
        "Timeout": int,
        "MaxCapacity": float,
        "WorkerType": Literal["Standard", "G.1X", "G.2X"],
        "NumberOfWorkers": int,
        "SecurityConfiguration": str,
        "NotificationProperty": NotificationPropertyTypeDef,
        "GlueVersion": str,
    },
    total=False,
)

ListCrawlersResponseTypeDef = TypedDict(
    "ListCrawlersResponseTypeDef", {"CrawlerNames": List[str], "NextToken": str}, total=False
)

ListDevEndpointsResponseTypeDef = TypedDict(
    "ListDevEndpointsResponseTypeDef",
    {"DevEndpointNames": List[str], "NextToken": str},
    total=False,
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef", {"JobNames": List[str], "NextToken": str}, total=False
)

ListTriggersResponseTypeDef = TypedDict(
    "ListTriggersResponseTypeDef", {"TriggerNames": List[str], "NextToken": str}, total=False
)

ListWorkflowsResponseTypeDef = TypedDict(
    "ListWorkflowsResponseTypeDef", {"Workflows": List[str], "NextToken": str}, total=False
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "Jdbc": List[CodeGenNodeArgTypeDef],
        "S3": List[CodeGenNodeArgTypeDef],
        "DynamoDB": List[CodeGenNodeArgTypeDef],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PartitionInputTypeDef = TypedDict(
    "PartitionInputTypeDef",
    {
        "Values": List[str],
        "LastAccessTime": datetime,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "Parameters": Dict[str, str],
        "LastAnalyzedTime": datetime,
    },
    total=False,
)

PropertyPredicateTypeDef = TypedDict(
    "PropertyPredicateTypeDef",
    {
        "Key": str,
        "Value": str,
        "Comparator": Literal[
            "EQUALS", "GREATER_THAN", "LESS_THAN", "GREATER_THAN_EQUALS", "LESS_THAN_EQUALS"
        ],
    },
    total=False,
)

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef", {"PolicyHash": str}, total=False
)

ResetJobBookmarkResponseTypeDef = TypedDict(
    "ResetJobBookmarkResponseTypeDef", {"JobBookmarkEntry": JobBookmarkEntryTypeDef}, total=False
)

SearchTablesResponseTypeDef = TypedDict(
    "SearchTablesResponseTypeDef", {"NextToken": str, "TableList": List[TableTypeDef]}, total=False
)

SegmentTypeDef = TypedDict("SegmentTypeDef", {"SegmentNumber": int, "TotalSegments": int})

SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef", {"FieldName": str, "Sort": Literal["ASC", "DESC"]}, total=False
)

StartExportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartExportLabelsTaskRunResponseTypeDef", {"TaskRunId": str}, total=False
)

StartImportLabelsTaskRunResponseTypeDef = TypedDict(
    "StartImportLabelsTaskRunResponseTypeDef", {"TaskRunId": str}, total=False
)

StartJobRunResponseTypeDef = TypedDict("StartJobRunResponseTypeDef", {"JobRunId": str}, total=False)

StartMLEvaluationTaskRunResponseTypeDef = TypedDict(
    "StartMLEvaluationTaskRunResponseTypeDef", {"TaskRunId": str}, total=False
)

StartMLLabelingSetGenerationTaskRunResponseTypeDef = TypedDict(
    "StartMLLabelingSetGenerationTaskRunResponseTypeDef", {"TaskRunId": str}, total=False
)

StartTriggerResponseTypeDef = TypedDict("StartTriggerResponseTypeDef", {"Name": str}, total=False)

StartWorkflowRunResponseTypeDef = TypedDict(
    "StartWorkflowRunResponseTypeDef", {"RunId": str}, total=False
)

StopTriggerResponseTypeDef = TypedDict("StopTriggerResponseTypeDef", {"Name": str}, total=False)

_RequiredTableInputTypeDef = TypedDict("_RequiredTableInputTypeDef", {"Name": str})
_OptionalTableInputTypeDef = TypedDict(
    "_OptionalTableInputTypeDef",
    {
        "Description": str,
        "Owner": str,
        "LastAccessTime": datetime,
        "LastAnalyzedTime": datetime,
        "Retention": int,
        "StorageDescriptor": StorageDescriptorTypeDef,
        "PartitionKeys": List[ColumnTypeDef],
        "ViewOriginalText": str,
        "ViewExpandedText": str,
        "TableType": str,
        "Parameters": Dict[str, str],
    },
    total=False,
)


class TableInputTypeDef(_RequiredTableInputTypeDef, _OptionalTableInputTypeDef):
    pass


TaskRunFilterCriteriaTypeDef = TypedDict(
    "TaskRunFilterCriteriaTypeDef",
    {
        "TaskRunType": Literal[
            "EVALUATION",
            "LABELING_SET_GENERATION",
            "IMPORT_LABELS",
            "EXPORT_LABELS",
            "FIND_MATCHES",
        ],
        "Status": Literal[
            "STARTING", "RUNNING", "STOPPING", "STOPPED", "SUCCEEDED", "FAILED", "TIMEOUT"
        ],
        "StartedBefore": datetime,
        "StartedAfter": datetime,
    },
    total=False,
)

TaskRunSortCriteriaTypeDef = TypedDict(
    "TaskRunSortCriteriaTypeDef",
    {
        "Column": Literal["TASK_RUN_TYPE", "STATUS", "STARTED"],
        "SortDirection": Literal["DESCENDING", "ASCENDING"],
    },
)

TransformFilterCriteriaTypeDef = TypedDict(
    "TransformFilterCriteriaTypeDef",
    {
        "Name": str,
        "TransformType": Literal["FIND_MATCHES"],
        "Status": Literal["NOT_READY", "READY", "DELETING"],
        "GlueVersion": str,
        "CreatedBefore": datetime,
        "CreatedAfter": datetime,
        "LastModifiedBefore": datetime,
        "LastModifiedAfter": datetime,
        "Schema": List[SchemaColumnTypeDef],
    },
    total=False,
)

TransformSortCriteriaTypeDef = TypedDict(
    "TransformSortCriteriaTypeDef",
    {
        "Column": Literal["NAME", "TRANSFORM_TYPE", "STATUS", "CREATED", "LAST_MODIFIED"],
        "SortDirection": Literal["DESCENDING", "ASCENDING"],
    },
)

TriggerUpdateTypeDef = TypedDict(
    "TriggerUpdateTypeDef",
    {
        "Name": str,
        "Description": str,
        "Schedule": str,
        "Actions": List[ActionTypeDef],
        "Predicate": PredicateTypeDef,
    },
    total=False,
)

_RequiredUpdateCsvClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateCsvClassifierRequestTypeDef", {"Name": str}
)
_OptionalUpdateCsvClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateCsvClassifierRequestTypeDef",
    {
        "Delimiter": str,
        "QuoteSymbol": str,
        "ContainsHeader": Literal["UNKNOWN", "PRESENT", "ABSENT"],
        "Header": List[str],
        "DisableValueTrimming": bool,
        "AllowSingleColumn": bool,
    },
    total=False,
)


class UpdateCsvClassifierRequestTypeDef(
    _RequiredUpdateCsvClassifierRequestTypeDef, _OptionalUpdateCsvClassifierRequestTypeDef
):
    pass


_RequiredUpdateGrokClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateGrokClassifierRequestTypeDef", {"Name": str}
)
_OptionalUpdateGrokClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateGrokClassifierRequestTypeDef",
    {"Classification": str, "GrokPattern": str, "CustomPatterns": str},
    total=False,
)


class UpdateGrokClassifierRequestTypeDef(
    _RequiredUpdateGrokClassifierRequestTypeDef, _OptionalUpdateGrokClassifierRequestTypeDef
):
    pass


UpdateJobResponseTypeDef = TypedDict("UpdateJobResponseTypeDef", {"JobName": str}, total=False)

_RequiredUpdateJsonClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateJsonClassifierRequestTypeDef", {"Name": str}
)
_OptionalUpdateJsonClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateJsonClassifierRequestTypeDef", {"JsonPath": str}, total=False
)


class UpdateJsonClassifierRequestTypeDef(
    _RequiredUpdateJsonClassifierRequestTypeDef, _OptionalUpdateJsonClassifierRequestTypeDef
):
    pass


UpdateMLTransformResponseTypeDef = TypedDict(
    "UpdateMLTransformResponseTypeDef", {"TransformId": str}, total=False
)

UpdateTriggerResponseTypeDef = TypedDict(
    "UpdateTriggerResponseTypeDef", {"Trigger": TriggerTypeDef}, total=False
)

UpdateWorkflowResponseTypeDef = TypedDict(
    "UpdateWorkflowResponseTypeDef", {"Name": str}, total=False
)

_RequiredUpdateXMLClassifierRequestTypeDef = TypedDict(
    "_RequiredUpdateXMLClassifierRequestTypeDef", {"Name": str}
)
_OptionalUpdateXMLClassifierRequestTypeDef = TypedDict(
    "_OptionalUpdateXMLClassifierRequestTypeDef",
    {"Classification": str, "RowTag": str},
    total=False,
)


class UpdateXMLClassifierRequestTypeDef(
    _RequiredUpdateXMLClassifierRequestTypeDef, _OptionalUpdateXMLClassifierRequestTypeDef
):
    pass


UserDefinedFunctionInputTypeDef = TypedDict(
    "UserDefinedFunctionInputTypeDef",
    {
        "FunctionName": str,
        "ClassName": str,
        "OwnerName": str,
        "OwnerType": Literal["USER", "ROLE", "GROUP"],
        "ResourceUris": List[ResourceUriTypeDef],
    },
    total=False,
)
