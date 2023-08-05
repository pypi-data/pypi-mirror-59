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


from __future__ import absolute_import

import unittest

from kubeflow import pytorchjob
from kubeflow.pytorchjob.models.v1_py_torch_job import V1PyTorchJob  # noqa: E501
from kubeflow.pytorchjob.rest import ApiException


class TestV1PyTorchJob(unittest.TestCase):
    """V1PyTorchJob unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testV1PyTorchJob(self):
        """Test V1PyTorchJob"""
        # FIXME: construct object with mandatory attributes with example values
        # model = pytorchjob.models.v1_py_torch_job.V1PyTorchJob()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
