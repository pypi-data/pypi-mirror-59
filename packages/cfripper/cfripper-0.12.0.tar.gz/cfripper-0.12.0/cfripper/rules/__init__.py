"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from cfripper.rules.base_rules import PrincipalCheckingRule
from cfripper.rules.cloudformation_authentication import CloudFormationAuthenticationRule
from cfripper.rules.cross_account_trust import (
    CrossAccountCheckingRule,
    CrossAccountTrustRule,
    KMSKeyCrossAccountTrustRule,
    S3CrossAccountTrustRule,
)
from cfripper.rules.ebs_volume_has_sse import EBSVolumeHasSSERule
from cfripper.rules.hardcoded_RDS_password import HardcodedRDSPasswordRule
from cfripper.rules.iam_managed_policy_wildcard_action import IAMManagedPolicyWildcardActionRule
from cfripper.rules.iam_roles import (
    IAMRolesOverprivilegedRule,
    IAMRoleWildcardActionOnPermissionsPolicyRule,
    IAMRoleWildcardActionOnTrustPolicyRule,
)
from cfripper.rules.kms_key_wildcard_principal import KMSKeyWildcardPrincipal
from cfripper.rules.managed_policy_on_user import ManagedPolicyOnUserRule
from cfripper.rules.policy_on_user import PolicyOnUserRule
from cfripper.rules.privilege_escalation import PrivilegeEscalationRule
from cfripper.rules.s3_bucket_policy import S3BucketPolicyPrincipalRule, S3BucketPolicyWildcardActionRule
from cfripper.rules.s3_public_access import S3BucketPublicReadAclAndListStatementRule, S3BucketPublicReadWriteAclRule
from cfripper.rules.security_group import (
    SecurityGroupIngressOpenToWorld,
    SecurityGroupMissingEgressRule,
    SecurityGroupOpenToWorldRule,
)
from cfripper.rules.sns_topic_policy_not_principal import SNSTopicPolicyNotPrincipalRule
from cfripper.rules.sqs_queue_policy import (
    SQSQueuePolicyNotPrincipalRule,
    SQSQueuePolicyPublicRule,
    SQSQueuePolicyWildcardActionRule,
)
from cfripper.rules.wildcard_principals import (
    FullWildcardPrincipalRule,
    GenericWildcardPrincipalRule,
    PartialWildcardPrincipalRule,
)

DEFAULT_RULES = {
    "CrossAccountTrustRule": CrossAccountTrustRule,
    "EBSVolumeHasSSERule": EBSVolumeHasSSERule,
    "FullWildcardPrincipal": FullWildcardPrincipalRule,
    "HardcodedRDSPasswordRule": HardcodedRDSPasswordRule,
    "IAMRolesOverprivilegedRule": IAMRolesOverprivilegedRule,
    "KMSKeyCrossAccountTrustRule": KMSKeyCrossAccountTrustRule,
    "KMSKeyWildcardPrincipal": KMSKeyWildcardPrincipal,
    "ManagedPolicyOnUserRule": ManagedPolicyOnUserRule,
    "PartialWildcardPrincipal": PartialWildcardPrincipalRule,
    "PolicyOnUserRule": PolicyOnUserRule,
    "PrivilegeEscalationRule": PrivilegeEscalationRule,
    "S3BucketPolicyPrincipalRule": S3BucketPolicyPrincipalRule,
    "S3BucketPublicReadAclAndListStatementRule": S3BucketPublicReadAclAndListStatementRule,
    "S3BucketPublicReadWriteAclRule": S3BucketPublicReadWriteAclRule,
    "S3CrossAccountTrustRule": S3CrossAccountTrustRule,
    "SecurityGroupIngressOpenToWorld": SecurityGroupIngressOpenToWorld,
    "SecurityGroupOpenToWorldRule": SecurityGroupOpenToWorldRule,
    "SNSTopicPolicyNotPrincipalRule": SNSTopicPolicyNotPrincipalRule,
    "SQSQueuePolicyNotPrincipalRule": SQSQueuePolicyNotPrincipalRule,
    "SQSQueuePolicyPublicRule": SQSQueuePolicyPublicRule,
}

NON_DEFAULT_RULES = {
    "CloudFormationAuthenticationRule": CloudFormationAuthenticationRule,
    "GenericWildcardPrincipalRule": GenericWildcardPrincipalRule,
    "IAMManagedPolicyWildcardActionRule": IAMManagedPolicyWildcardActionRule,
    "IAMRoleWildcardActionOnPermissionsPolicyRule": IAMRoleWildcardActionOnPermissionsPolicyRule,
    "IAMRoleWildcardActionOnTrustPolicyRule": IAMRoleWildcardActionOnTrustPolicyRule,
    "S3BucketPolicyWildcardActionRule": S3BucketPolicyWildcardActionRule,
    "SecurityGroupMissingEgressRule": SecurityGroupMissingEgressRule,
    "SQSQueuePolicyWildcardActionRule": SQSQueuePolicyWildcardActionRule,
}

BASE_CLASSES = {
    "CrossAccountCheckingRule": CrossAccountCheckingRule,
    "PrincipalCheckingRule": PrincipalCheckingRule,
}
