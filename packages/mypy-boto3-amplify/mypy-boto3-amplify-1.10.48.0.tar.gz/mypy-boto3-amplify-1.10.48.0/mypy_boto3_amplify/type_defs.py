"""
Main interface for amplify service type definitions.

Usage::

    from mypy_boto3.amplify.type_defs import AutoBranchCreationConfigTypeDef

    data: AutoBranchCreationConfigTypeDef = {...}
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
    "AutoBranchCreationConfigTypeDef",
    "CustomRuleTypeDef",
    "ProductionBranchTypeDef",
    "AppTypeDef",
    "CreateAppResultTypeDef",
    "BackendEnvironmentTypeDef",
    "CreateBackendEnvironmentResultTypeDef",
    "BranchTypeDef",
    "CreateBranchResultTypeDef",
    "CreateDeploymentResultTypeDef",
    "SubDomainSettingTypeDef",
    "SubDomainTypeDef",
    "DomainAssociationTypeDef",
    "CreateDomainAssociationResultTypeDef",
    "WebhookTypeDef",
    "CreateWebhookResultTypeDef",
    "DeleteAppResultTypeDef",
    "DeleteBackendEnvironmentResultTypeDef",
    "DeleteBranchResultTypeDef",
    "DeleteDomainAssociationResultTypeDef",
    "JobSummaryTypeDef",
    "DeleteJobResultTypeDef",
    "DeleteWebhookResultTypeDef",
    "GenerateAccessLogsResultTypeDef",
    "GetAppResultTypeDef",
    "GetArtifactUrlResultTypeDef",
    "GetBackendEnvironmentResultTypeDef",
    "GetBranchResultTypeDef",
    "GetDomainAssociationResultTypeDef",
    "StepTypeDef",
    "JobTypeDef",
    "GetJobResultTypeDef",
    "GetWebhookResultTypeDef",
    "ListAppsResultTypeDef",
    "ArtifactTypeDef",
    "ListArtifactsResultTypeDef",
    "ListBackendEnvironmentsResultTypeDef",
    "ListBranchesResultTypeDef",
    "ListDomainAssociationsResultTypeDef",
    "ListJobsResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWebhooksResultTypeDef",
    "PaginatorConfigTypeDef",
    "StartDeploymentResultTypeDef",
    "StartJobResultTypeDef",
    "StopJobResultTypeDef",
    "UpdateAppResultTypeDef",
    "UpdateBranchResultTypeDef",
    "UpdateDomainAssociationResultTypeDef",
    "UpdateWebhookResultTypeDef",
)

AutoBranchCreationConfigTypeDef = TypedDict(
    "AutoBranchCreationConfigTypeDef",
    {
        "stage": Literal["PRODUCTION", "BETA", "DEVELOPMENT", "EXPERIMENTAL", "PULL_REQUEST"],
        "framework": str,
        "enableAutoBuild": bool,
        "environmentVariables": Dict[str, str],
        "basicAuthCredentials": str,
        "enableBasicAuth": bool,
        "buildSpec": str,
        "enablePullRequestPreview": bool,
        "pullRequestEnvironmentName": str,
    },
    total=False,
)

_RequiredCustomRuleTypeDef = TypedDict("_RequiredCustomRuleTypeDef", {"source": str, "target": str})
_OptionalCustomRuleTypeDef = TypedDict(
    "_OptionalCustomRuleTypeDef", {"status": str, "condition": str}, total=False
)


class CustomRuleTypeDef(_RequiredCustomRuleTypeDef, _OptionalCustomRuleTypeDef):
    pass


ProductionBranchTypeDef = TypedDict(
    "ProductionBranchTypeDef",
    {"lastDeployTime": datetime, "status": str, "thumbnailUrl": str, "branchName": str},
    total=False,
)

_RequiredAppTypeDef = TypedDict(
    "_RequiredAppTypeDef",
    {
        "appId": str,
        "appArn": str,
        "name": str,
        "description": str,
        "repository": str,
        "platform": Literal["WEB"],
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "defaultDomain": str,
        "enableBranchAutoBuild": bool,
        "enableBasicAuth": bool,
    },
)
_OptionalAppTypeDef = TypedDict(
    "_OptionalAppTypeDef",
    {
        "tags": Dict[str, str],
        "iamServiceRoleArn": str,
        "basicAuthCredentials": str,
        "customRules": List[CustomRuleTypeDef],
        "productionBranch": ProductionBranchTypeDef,
        "buildSpec": str,
        "enableAutoBranchCreation": bool,
        "autoBranchCreationPatterns": List[str],
        "autoBranchCreationConfig": AutoBranchCreationConfigTypeDef,
    },
    total=False,
)


class AppTypeDef(_RequiredAppTypeDef, _OptionalAppTypeDef):
    pass


CreateAppResultTypeDef = TypedDict("CreateAppResultTypeDef", {"app": AppTypeDef})

_RequiredBackendEnvironmentTypeDef = TypedDict(
    "_RequiredBackendEnvironmentTypeDef",
    {
        "backendEnvironmentArn": str,
        "environmentName": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
_OptionalBackendEnvironmentTypeDef = TypedDict(
    "_OptionalBackendEnvironmentTypeDef",
    {"stackName": str, "deploymentArtifacts": str},
    total=False,
)


class BackendEnvironmentTypeDef(
    _RequiredBackendEnvironmentTypeDef, _OptionalBackendEnvironmentTypeDef
):
    pass


CreateBackendEnvironmentResultTypeDef = TypedDict(
    "CreateBackendEnvironmentResultTypeDef", {"backendEnvironment": BackendEnvironmentTypeDef}
)

_RequiredBranchTypeDef = TypedDict(
    "_RequiredBranchTypeDef",
    {
        "branchArn": str,
        "branchName": str,
        "description": str,
        "stage": Literal["PRODUCTION", "BETA", "DEVELOPMENT", "EXPERIMENTAL", "PULL_REQUEST"],
        "displayName": str,
        "enableNotification": bool,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "enableAutoBuild": bool,
        "customDomains": List[str],
        "framework": str,
        "activeJobId": str,
        "totalNumberOfJobs": str,
        "enableBasicAuth": bool,
        "ttl": str,
        "enablePullRequestPreview": bool,
    },
)
_OptionalBranchTypeDef = TypedDict(
    "_OptionalBranchTypeDef",
    {
        "tags": Dict[str, str],
        "thumbnailUrl": str,
        "basicAuthCredentials": str,
        "buildSpec": str,
        "associatedResources": List[str],
        "pullRequestEnvironmentName": str,
        "destinationBranch": str,
        "sourceBranch": str,
        "backendEnvironmentArn": str,
    },
    total=False,
)


class BranchTypeDef(_RequiredBranchTypeDef, _OptionalBranchTypeDef):
    pass


CreateBranchResultTypeDef = TypedDict("CreateBranchResultTypeDef", {"branch": BranchTypeDef})

_RequiredCreateDeploymentResultTypeDef = TypedDict(
    "_RequiredCreateDeploymentResultTypeDef",
    {"fileUploadUrls": Dict[str, str], "zipUploadUrl": str},
)
_OptionalCreateDeploymentResultTypeDef = TypedDict(
    "_OptionalCreateDeploymentResultTypeDef", {"jobId": str}, total=False
)


class CreateDeploymentResultTypeDef(
    _RequiredCreateDeploymentResultTypeDef, _OptionalCreateDeploymentResultTypeDef
):
    pass


SubDomainSettingTypeDef = TypedDict("SubDomainSettingTypeDef", {"prefix": str, "branchName": str})

SubDomainTypeDef = TypedDict(
    "SubDomainTypeDef",
    {"subDomainSetting": SubDomainSettingTypeDef, "verified": bool, "dnsRecord": str},
)

_RequiredDomainAssociationTypeDef = TypedDict(
    "_RequiredDomainAssociationTypeDef",
    {
        "domainAssociationArn": str,
        "domainName": str,
        "enableAutoSubDomain": bool,
        "domainStatus": Literal[
            "PENDING_VERIFICATION",
            "IN_PROGRESS",
            "AVAILABLE",
            "PENDING_DEPLOYMENT",
            "FAILED",
            "CREATING",
            "REQUESTING_CERTIFICATE",
            "UPDATING",
        ],
        "statusReason": str,
        "subDomains": List[SubDomainTypeDef],
    },
)
_OptionalDomainAssociationTypeDef = TypedDict(
    "_OptionalDomainAssociationTypeDef", {"certificateVerificationDNSRecord": str}, total=False
)


class DomainAssociationTypeDef(
    _RequiredDomainAssociationTypeDef, _OptionalDomainAssociationTypeDef
):
    pass


CreateDomainAssociationResultTypeDef = TypedDict(
    "CreateDomainAssociationResultTypeDef", {"domainAssociation": DomainAssociationTypeDef}
)

WebhookTypeDef = TypedDict(
    "WebhookTypeDef",
    {
        "webhookArn": str,
        "webhookId": str,
        "webhookUrl": str,
        "branchName": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)

CreateWebhookResultTypeDef = TypedDict("CreateWebhookResultTypeDef", {"webhook": WebhookTypeDef})

DeleteAppResultTypeDef = TypedDict("DeleteAppResultTypeDef", {"app": AppTypeDef})

DeleteBackendEnvironmentResultTypeDef = TypedDict(
    "DeleteBackendEnvironmentResultTypeDef", {"backendEnvironment": BackendEnvironmentTypeDef}
)

DeleteBranchResultTypeDef = TypedDict("DeleteBranchResultTypeDef", {"branch": BranchTypeDef})

DeleteDomainAssociationResultTypeDef = TypedDict(
    "DeleteDomainAssociationResultTypeDef", {"domainAssociation": DomainAssociationTypeDef}
)

_RequiredJobSummaryTypeDef = TypedDict(
    "_RequiredJobSummaryTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "commitId": str,
        "commitMessage": str,
        "commitTime": datetime,
        "startTime": datetime,
        "status": Literal[
            "PENDING", "PROVISIONING", "RUNNING", "FAILED", "SUCCEED", "CANCELLING", "CANCELLED"
        ],
        "jobType": Literal["RELEASE", "RETRY", "MANUAL", "WEB_HOOK"],
    },
)
_OptionalJobSummaryTypeDef = TypedDict(
    "_OptionalJobSummaryTypeDef", {"endTime": datetime}, total=False
)


class JobSummaryTypeDef(_RequiredJobSummaryTypeDef, _OptionalJobSummaryTypeDef):
    pass


DeleteJobResultTypeDef = TypedDict("DeleteJobResultTypeDef", {"jobSummary": JobSummaryTypeDef})

DeleteWebhookResultTypeDef = TypedDict("DeleteWebhookResultTypeDef", {"webhook": WebhookTypeDef})

GenerateAccessLogsResultTypeDef = TypedDict(
    "GenerateAccessLogsResultTypeDef", {"logUrl": str}, total=False
)

GetAppResultTypeDef = TypedDict("GetAppResultTypeDef", {"app": AppTypeDef})

GetArtifactUrlResultTypeDef = TypedDict(
    "GetArtifactUrlResultTypeDef", {"artifactId": str, "artifactUrl": str}
)

GetBackendEnvironmentResultTypeDef = TypedDict(
    "GetBackendEnvironmentResultTypeDef", {"backendEnvironment": BackendEnvironmentTypeDef}
)

GetBranchResultTypeDef = TypedDict("GetBranchResultTypeDef", {"branch": BranchTypeDef})

GetDomainAssociationResultTypeDef = TypedDict(
    "GetDomainAssociationResultTypeDef", {"domainAssociation": DomainAssociationTypeDef}
)

_RequiredStepTypeDef = TypedDict(
    "_RequiredStepTypeDef",
    {
        "stepName": str,
        "startTime": datetime,
        "status": Literal[
            "PENDING", "PROVISIONING", "RUNNING", "FAILED", "SUCCEED", "CANCELLING", "CANCELLED"
        ],
        "endTime": datetime,
    },
)
_OptionalStepTypeDef = TypedDict(
    "_OptionalStepTypeDef",
    {
        "logUrl": str,
        "artifactsUrl": str,
        "testArtifactsUrl": str,
        "testConfigUrl": str,
        "screenshots": Dict[str, str],
        "statusReason": str,
        "context": str,
    },
    total=False,
)


class StepTypeDef(_RequiredStepTypeDef, _OptionalStepTypeDef):
    pass


JobTypeDef = TypedDict("JobTypeDef", {"summary": JobSummaryTypeDef, "steps": List[StepTypeDef]})

GetJobResultTypeDef = TypedDict("GetJobResultTypeDef", {"job": JobTypeDef})

GetWebhookResultTypeDef = TypedDict("GetWebhookResultTypeDef", {"webhook": WebhookTypeDef})

_RequiredListAppsResultTypeDef = TypedDict(
    "_RequiredListAppsResultTypeDef", {"apps": List[AppTypeDef]}
)
_OptionalListAppsResultTypeDef = TypedDict(
    "_OptionalListAppsResultTypeDef", {"nextToken": str}, total=False
)


class ListAppsResultTypeDef(_RequiredListAppsResultTypeDef, _OptionalListAppsResultTypeDef):
    pass


ArtifactTypeDef = TypedDict("ArtifactTypeDef", {"artifactFileName": str, "artifactId": str})

_RequiredListArtifactsResultTypeDef = TypedDict(
    "_RequiredListArtifactsResultTypeDef", {"artifacts": List[ArtifactTypeDef]}
)
_OptionalListArtifactsResultTypeDef = TypedDict(
    "_OptionalListArtifactsResultTypeDef", {"nextToken": str}, total=False
)


class ListArtifactsResultTypeDef(
    _RequiredListArtifactsResultTypeDef, _OptionalListArtifactsResultTypeDef
):
    pass


_RequiredListBackendEnvironmentsResultTypeDef = TypedDict(
    "_RequiredListBackendEnvironmentsResultTypeDef",
    {"backendEnvironments": List[BackendEnvironmentTypeDef]},
)
_OptionalListBackendEnvironmentsResultTypeDef = TypedDict(
    "_OptionalListBackendEnvironmentsResultTypeDef", {"nextToken": str}, total=False
)


class ListBackendEnvironmentsResultTypeDef(
    _RequiredListBackendEnvironmentsResultTypeDef, _OptionalListBackendEnvironmentsResultTypeDef
):
    pass


_RequiredListBranchesResultTypeDef = TypedDict(
    "_RequiredListBranchesResultTypeDef", {"branches": List[BranchTypeDef]}
)
_OptionalListBranchesResultTypeDef = TypedDict(
    "_OptionalListBranchesResultTypeDef", {"nextToken": str}, total=False
)


class ListBranchesResultTypeDef(
    _RequiredListBranchesResultTypeDef, _OptionalListBranchesResultTypeDef
):
    pass


_RequiredListDomainAssociationsResultTypeDef = TypedDict(
    "_RequiredListDomainAssociationsResultTypeDef",
    {"domainAssociations": List[DomainAssociationTypeDef]},
)
_OptionalListDomainAssociationsResultTypeDef = TypedDict(
    "_OptionalListDomainAssociationsResultTypeDef", {"nextToken": str}, total=False
)


class ListDomainAssociationsResultTypeDef(
    _RequiredListDomainAssociationsResultTypeDef, _OptionalListDomainAssociationsResultTypeDef
):
    pass


_RequiredListJobsResultTypeDef = TypedDict(
    "_RequiredListJobsResultTypeDef", {"jobSummaries": List[JobSummaryTypeDef]}
)
_OptionalListJobsResultTypeDef = TypedDict(
    "_OptionalListJobsResultTypeDef", {"nextToken": str}, total=False
)


class ListJobsResultTypeDef(_RequiredListJobsResultTypeDef, _OptionalListJobsResultTypeDef):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

_RequiredListWebhooksResultTypeDef = TypedDict(
    "_RequiredListWebhooksResultTypeDef", {"webhooks": List[WebhookTypeDef]}
)
_OptionalListWebhooksResultTypeDef = TypedDict(
    "_OptionalListWebhooksResultTypeDef", {"nextToken": str}, total=False
)


class ListWebhooksResultTypeDef(
    _RequiredListWebhooksResultTypeDef, _OptionalListWebhooksResultTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

StartDeploymentResultTypeDef = TypedDict(
    "StartDeploymentResultTypeDef", {"jobSummary": JobSummaryTypeDef}
)

StartJobResultTypeDef = TypedDict("StartJobResultTypeDef", {"jobSummary": JobSummaryTypeDef})

StopJobResultTypeDef = TypedDict("StopJobResultTypeDef", {"jobSummary": JobSummaryTypeDef})

UpdateAppResultTypeDef = TypedDict("UpdateAppResultTypeDef", {"app": AppTypeDef})

UpdateBranchResultTypeDef = TypedDict("UpdateBranchResultTypeDef", {"branch": BranchTypeDef})

UpdateDomainAssociationResultTypeDef = TypedDict(
    "UpdateDomainAssociationResultTypeDef", {"domainAssociation": DomainAssociationTypeDef}
)

UpdateWebhookResultTypeDef = TypedDict("UpdateWebhookResultTypeDef", {"webhook": WebhookTypeDef})
