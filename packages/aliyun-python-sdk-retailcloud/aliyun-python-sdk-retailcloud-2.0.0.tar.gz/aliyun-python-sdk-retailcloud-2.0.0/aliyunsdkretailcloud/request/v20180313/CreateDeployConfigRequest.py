# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest

class CreateDeployConfigRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'retailcloud', '2018-03-13', 'CreateDeployConfig','retailcloud')

	def get_CodePath(self):
		return self.get_query_params().get('CodePath')

	def set_CodePath(self,CodePath):
		self.add_query_param('CodePath',CodePath)

	def get_AppId(self):
		return self.get_query_params().get('AppId')

	def set_AppId(self,AppId):
		self.add_query_param('AppId',AppId)

	def get_ConfigMap(self):
		return self.get_query_params().get('ConfigMap')

	def set_ConfigMap(self,ConfigMap):
		self.add_query_param('ConfigMap',ConfigMap)

	def get_StatefulSet(self):
		return self.get_query_params().get('StatefulSet')

	def set_StatefulSet(self,StatefulSet):
		self.add_query_param('StatefulSet',StatefulSet)

	def get_EnvType(self):
		return self.get_query_params().get('EnvType')

	def set_EnvType(self,EnvType):
		self.add_query_param('EnvType',EnvType)

	def get_Name(self):
		return self.get_query_params().get('Name')

	def set_Name(self,Name):
		self.add_query_param('Name',Name)

	def get_Deployment(self):
		return self.get_query_params().get('Deployment')

	def set_Deployment(self,Deployment):
		self.add_query_param('Deployment',Deployment)