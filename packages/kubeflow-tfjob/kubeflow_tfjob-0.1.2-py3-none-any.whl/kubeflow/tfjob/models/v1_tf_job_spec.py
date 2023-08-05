# Copyright 2019 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    tfjob

    Python SDK for TF-Operator  # noqa: E501

    OpenAPI spec version: v0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from kubeflow.tfjob.models.v1_replica_spec import V1ReplicaSpec  # noqa: F401,E501


class V1TFJobSpec(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'active_deadline_seconds': 'int',
        'backoff_limit': 'int',
        'clean_pod_policy': 'str',
        'tf_replica_specs': 'dict(str, V1ReplicaSpec)',
        'ttl_seconds_after_finished': 'int'
    }

    attribute_map = {
        'active_deadline_seconds': 'activeDeadlineSeconds',
        'backoff_limit': 'backoffLimit',
        'clean_pod_policy': 'cleanPodPolicy',
        'tf_replica_specs': 'tfReplicaSpecs',
        'ttl_seconds_after_finished': 'ttlSecondsAfterFinished'
    }

    def __init__(self, active_deadline_seconds=None, backoff_limit=None, clean_pod_policy=None, tf_replica_specs=None, ttl_seconds_after_finished=None):  # noqa: E501
        """V1TFJobSpec - a model defined in Swagger"""  # noqa: E501

        self._active_deadline_seconds = None
        self._backoff_limit = None
        self._clean_pod_policy = None
        self._tf_replica_specs = None
        self._ttl_seconds_after_finished = None
        self.discriminator = None

        if active_deadline_seconds is not None:
            self.active_deadline_seconds = active_deadline_seconds
        if backoff_limit is not None:
            self.backoff_limit = backoff_limit
        if clean_pod_policy is not None:
            self.clean_pod_policy = clean_pod_policy
        self.tf_replica_specs = tf_replica_specs
        if ttl_seconds_after_finished is not None:
            self.ttl_seconds_after_finished = ttl_seconds_after_finished

    @property
    def active_deadline_seconds(self):
        """Gets the active_deadline_seconds of this V1TFJobSpec.  # noqa: E501

        Specifies the duration (in seconds) since startTime during which the job can remain active before it is terminated. Must be a positive integer. This setting applies only to pods where restartPolicy is OnFailure or Always.  # noqa: E501

        :return: The active_deadline_seconds of this V1TFJobSpec.  # noqa: E501
        :rtype: int
        """
        return self._active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, active_deadline_seconds):
        """Sets the active_deadline_seconds of this V1TFJobSpec.

        Specifies the duration (in seconds) since startTime during which the job can remain active before it is terminated. Must be a positive integer. This setting applies only to pods where restartPolicy is OnFailure or Always.  # noqa: E501

        :param active_deadline_seconds: The active_deadline_seconds of this V1TFJobSpec.  # noqa: E501
        :type: int
        """

        self._active_deadline_seconds = active_deadline_seconds

    @property
    def backoff_limit(self):
        """Gets the backoff_limit of this V1TFJobSpec.  # noqa: E501

        Number of retries before marking this job as failed.  # noqa: E501

        :return: The backoff_limit of this V1TFJobSpec.  # noqa: E501
        :rtype: int
        """
        return self._backoff_limit

    @backoff_limit.setter
    def backoff_limit(self, backoff_limit):
        """Sets the backoff_limit of this V1TFJobSpec.

        Number of retries before marking this job as failed.  # noqa: E501

        :param backoff_limit: The backoff_limit of this V1TFJobSpec.  # noqa: E501
        :type: int
        """

        self._backoff_limit = backoff_limit

    @property
    def clean_pod_policy(self):
        """Gets the clean_pod_policy of this V1TFJobSpec.  # noqa: E501

        Defines the policy for cleaning up pods after the TFJob completes. Defaults to Running.  # noqa: E501

        :return: The clean_pod_policy of this V1TFJobSpec.  # noqa: E501
        :rtype: str
        """
        return self._clean_pod_policy

    @clean_pod_policy.setter
    def clean_pod_policy(self, clean_pod_policy):
        """Sets the clean_pod_policy of this V1TFJobSpec.

        Defines the policy for cleaning up pods after the TFJob completes. Defaults to Running.  # noqa: E501

        :param clean_pod_policy: The clean_pod_policy of this V1TFJobSpec.  # noqa: E501
        :type: str
        """

        self._clean_pod_policy = clean_pod_policy

    @property
    def tf_replica_specs(self):
        """Gets the tf_replica_specs of this V1TFJobSpec.  # noqa: E501

        A map of TFReplicaType (type) to ReplicaSpec (value). Specifies the TF cluster configuration. For example,   {     \"PS\": ReplicaSpec,     \"Worker\": ReplicaSpec,   }  # noqa: E501

        :return: The tf_replica_specs of this V1TFJobSpec.  # noqa: E501
        :rtype: dict(str, V1ReplicaSpec)
        """
        return self._tf_replica_specs

    @tf_replica_specs.setter
    def tf_replica_specs(self, tf_replica_specs):
        """Sets the tf_replica_specs of this V1TFJobSpec.

        A map of TFReplicaType (type) to ReplicaSpec (value). Specifies the TF cluster configuration. For example,   {     \"PS\": ReplicaSpec,     \"Worker\": ReplicaSpec,   }  # noqa: E501

        :param tf_replica_specs: The tf_replica_specs of this V1TFJobSpec.  # noqa: E501
        :type: dict(str, V1ReplicaSpec)
        """
        if tf_replica_specs is None:
            raise ValueError("Invalid value for `tf_replica_specs`, must not be `None`")  # noqa: E501

        self._tf_replica_specs = tf_replica_specs

    @property
    def ttl_seconds_after_finished(self):
        """Gets the ttl_seconds_after_finished of this V1TFJobSpec.  # noqa: E501

        Defines the TTL for cleaning up finished TFJobs (temporary before kubernetes adds the cleanup controller). It may take extra ReconcilePeriod seconds for the cleanup, since reconcile gets called periodically. Defaults to infinite.  # noqa: E501

        :return: The ttl_seconds_after_finished of this V1TFJobSpec.  # noqa: E501
        :rtype: int
        """
        return self._ttl_seconds_after_finished

    @ttl_seconds_after_finished.setter
    def ttl_seconds_after_finished(self, ttl_seconds_after_finished):
        """Sets the ttl_seconds_after_finished of this V1TFJobSpec.

        Defines the TTL for cleaning up finished TFJobs (temporary before kubernetes adds the cleanup controller). It may take extra ReconcilePeriod seconds for the cleanup, since reconcile gets called periodically. Defaults to infinite.  # noqa: E501

        :param ttl_seconds_after_finished: The ttl_seconds_after_finished of this V1TFJobSpec.  # noqa: E501
        :type: int
        """

        self._ttl_seconds_after_finished = ttl_seconds_after_finished

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1TFJobSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1TFJobSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
