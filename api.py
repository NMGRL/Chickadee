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
import os

from flask_restful import Resource, Api
from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from models import SampleTbl, ProjectTbl, MaterialTbl, PrincipalInvestigatorTbl, AnalysisTbl, IrradiationPositionTbl

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix='/api/v1')


def auth(func):
    # disable authorization for browswer based api testing only
    if os.getenv('JWT_ENABLED') == '1':
        return jwt_required()(func)
    else:
        return func


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

    @auth
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


class Analysis(Resource):
    @auth
    def get(self):
        args = request.args
        project = args.get('project')
        sample = args.get('sample')
        material = args.get('material')

        def make_result(r):
            return {'RunID': r.runid,
                    'Identifier': r.irradiation_position.identifier,
                    'Aliquot': r.aliquot,
                    'Increment': (r.increment,r.step),
                    'RunDate': r.timestamp.isoformat(),
                    'Sample': r.irradiation_position.sample.name,
                    'Material': r.irradiation_position.sample.material.name,
                    'IrradiationInfo': r.irradiation_info}

        q = AnalysisTbl.query
        q = q.join(IrradiationPositionTbl)
        q = q.join(SampleTbl)
        if project:
            q = q.join(ProjectTbl)
            q = q.filter(ProjectTbl.name == project)
            q = q.filter(AnalysisTbl.analysis_type == 'unknown')

        if sample:
            q = q.filter(SampleTbl.name == sample)

        if material:
            q = q.join(MaterialTbl)
            q = q.filter(MaterialTbl.name == material)

        results = q.all()

        return [make_result(ri) for ri in results]


api.add_resource(Sample, '/sample')
api.add_resource(Project, '/project')
api.add_resource(Material, '/material')
api.add_resource(PrincipalInvestigator, '/principal_investigator')
api.add_resource(Analysis, '/analysis')
# ============= EOF =============================================
