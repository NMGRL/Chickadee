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
from flask_restful import Resource, Api
from flask import Blueprint, request, jsonify

from models import SampleTbl, ProjectTbl, MaterialTbl, PrincipalInvestigatorTbl

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


class NameResource(Resource):
    def _get_results(self, model):
        args = request.args
        if args.get('all') == '1':
            q = model.query
        else:
            name = args.get('name')
            if name:
                q = model.query.filter_by(name=name)
            else:
                q = self._handle_get_results(args)

        return q.all()

    def get(self):
        results = self._get_results(self._model_klass)
        return jsonify([self._make_result(result) for result in results])

    def _make_result(self, ri):
        raise NotImplementedError

    def _handle_get_results(self):
        raise NotImplementedError


class Sample(NameResource):
    _model_klass = SampleTbl

    def _make_result(self, ri):
        return {'id': ri.id, 'name': ri.name,
                'material': {'name': ri.material.name, 'grainsize': ri.material.grainsize},
                'project': {'name': ri.project.name, 'principal investigator':
                    ri.project.principal_investigator.full_name}}

    def _handle_get_results(self, args):
        project = args.get('project')
        if project:
            q = SampleTbl.query
            q = q.join(ProjectTbl)
            q = q.filter(ProjectTbl.name == project)
            return q


class Project(NameResource):
    _model_klass = ProjectTbl

    def _make_result(self, ri):
        return {'id': ri.id, 'name': ri.name, 'principal_investigator': ri.principal_investigator.full_name}


class Material(NameResource):
    _model_klass = MaterialTbl

    def _make_result(self, ri):
        return {'id': ri.id, 'name': ri.name, 'grainsize': ri.grainsize}


class PrincipalInvestigator(NameResource):
    _model_klass = PrincipalInvestigatorTbl

    def _make_result(self, ri):
        return {'id': ri.id, 'name': ri.full_name, 'last_name': ri.last_name, 'first_initial': ri.first_initial}


api.add_resource(Sample, '/api/sample')
api.add_resource(Project, '/api/project')
api.add_resource(Material, '/api/material')
api.add_resource(PrincipalInvestigator, '/api/principal_investigator')
# ============= EOF =============================================
