# ===============================================================================
# Copyright 2019 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
__api_version__ = 1

from flask_restful import Api
from flask import Blueprint

from app.api.resources import Sample, Project, Material, PrincipalInvestigator, Analysis

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix='/api/v{}'.format(__api_version__))

api.add_resource(Sample, '/sample')
api.add_resource(Project, '/project')
api.add_resource(Material, '/material')
api.add_resource(PrincipalInvestigator, '/principal_investigator')
api.add_resource(Analysis, '/analysis')
# ============= EOF =============================================
