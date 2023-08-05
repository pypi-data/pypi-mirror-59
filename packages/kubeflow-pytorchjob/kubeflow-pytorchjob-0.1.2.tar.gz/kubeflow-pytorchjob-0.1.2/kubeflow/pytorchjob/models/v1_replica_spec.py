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
    pytorch

    Python SDK for PyTorch-Operator  # noqa: E501

    OpenAPI spec version: v0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from kubernetes.client import V1PodTemplateSpec  # noqa: F401,E501


class V1ReplicaSpec(object):
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
        'replicas': 'int',
        'restart_policy': 'str',
        'template': 'V1PodTemplateSpec'
    }

    attribute_map = {
        'replicas': 'replicas',
        'restart_policy': 'restartPolicy',
        'template': 'template'
    }

    def __init__(self, replicas=None, restart_policy=None, template=None):  # noqa: E501
        """V1ReplicaSpec - a model defined in Swagger"""  # noqa: E501

        self._replicas = None
        self._restart_policy = None
        self._template = None
        self.discriminator = None

        if replicas is not None:
            self.replicas = replicas
        if restart_policy is not None:
            self.restart_policy = restart_policy
        if template is not None:
            self.template = template

    @property
    def replicas(self):
        """Gets the replicas of this V1ReplicaSpec.  # noqa: E501

        Replicas is the desired number of replicas of the given template. If unspecified, defaults to 1.  # noqa: E501

        :return: The replicas of this V1ReplicaSpec.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this V1ReplicaSpec.

        Replicas is the desired number of replicas of the given template. If unspecified, defaults to 1.  # noqa: E501

        :param replicas: The replicas of this V1ReplicaSpec.  # noqa: E501
        :type: int
        """

        self._replicas = replicas

    @property
    def restart_policy(self):
        """Gets the restart_policy of this V1ReplicaSpec.  # noqa: E501

        Restart policy for all replicas within the job. One of Always, OnFailure, Never and ExitCode. Default to Never.  # noqa: E501

        :return: The restart_policy of this V1ReplicaSpec.  # noqa: E501
        :rtype: str
        """
        return self._restart_policy

    @restart_policy.setter
    def restart_policy(self, restart_policy):
        """Sets the restart_policy of this V1ReplicaSpec.

        Restart policy for all replicas within the job. One of Always, OnFailure, Never and ExitCode. Default to Never.  # noqa: E501

        :param restart_policy: The restart_policy of this V1ReplicaSpec.  # noqa: E501
        :type: str
        """

        self._restart_policy = restart_policy

    @property
    def template(self):
        """Gets the template of this V1ReplicaSpec.  # noqa: E501

        Template is the object that describes the pod that will be created for this replica. RestartPolicy in PodTemplateSpec will be overide by RestartPolicy in ReplicaSpec  # noqa: E501

        :return: The template of this V1ReplicaSpec.  # noqa: E501
        :rtype: V1PodTemplateSpec
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this V1ReplicaSpec.

        Template is the object that describes the pod that will be created for this replica. RestartPolicy in PodTemplateSpec will be overide by RestartPolicy in ReplicaSpec  # noqa: E501

        :param template: The template of this V1ReplicaSpec.  # noqa: E501
        :type: V1PodTemplateSpec
        """

        self._template = template

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
        if issubclass(V1ReplicaSpec, dict):
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
        if not isinstance(other, V1ReplicaSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
