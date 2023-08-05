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

class UpdateProjectRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'imm', '2017-09-06', 'UpdateProject','imm')

	def get_Project(self):
		return self.get_query_params().get('Project')

	def set_Project(self,Project):
		self.add_query_param('Project',Project)

	def get_NewServiceRole(self):
		return self.get_query_params().get('NewServiceRole')

	def set_NewServiceRole(self,NewServiceRole):
		self.add_query_param('NewServiceRole',NewServiceRole)

	def get_NewCU(self):
		return self.get_query_params().get('NewCU')

	def set_NewCU(self,NewCU):
		self.add_query_param('NewCU',NewCU)