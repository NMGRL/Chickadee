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


from datetime import datetime
from http import HTTPStatus

from flask import request, jsonify
from flask_restful import Resource, marshal_with, fields

from app.api.base_resource import LAST_NAME, FIRST_INITIAL, GRAINSIZE, PROJECT, MATERIAL, NAME, \
    PRINCIPAL_INVESTIGATOR, \
    SAMPLE, ID, auth, NameResource, BaseResource
from app.api.models import SampleTbl, MaterialTbl, PrincipalInvestigatorTbl, ProjectTbl, AnalysisTbl, \
    IrradiationPositionTbl


class Sample(NameResource):
    _model_klass = SampleTbl
    _description = 'Route giving access to samples'

    def _get_marshal_fields(self):
        return {'name': fields.String}

    def _precondition(self, q, data):
        name = data.get(NAME)
        if name:
            material = data.get(MATERIAL)
            if material:
                mname = material.get(NAME)
                grainsize = material.get(GRAINSIZE)
                qq = MaterialTbl.query.filter_by(name=mname)
                qq = qq.filter_by(grainsize=grainsize)
                if not qq.all():
                    return

            project = data.get(PROJECT)
            if project:
                pname = project.get(NAME)
                principal_investigator = project.get(PRINCIPAL_INVESTIGATOR)
                if principal_investigator:
                    last_name = principal_investigator.get(LAST_NAME)
                    first_initial = principal_investigator.get(FIRST_INITIAL)
                    qq = PrincipalInvestigatorTbl.query
                    qq = qq.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
                    qq = qq.filter(PrincipalInvestigatorTbl.last_name == last_name)

                    if not qq.all():
                        return

                    qq = ProjectTbl.query
                    qq = qq.filter(ProjectTbl.name == pname)
                    qq = qq.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
                    qq = qq.filter(PrincipalInvestigatorTbl.last_name == last_name)
                    if not qq.all():
                        return

                    q = q.join(MaterialTbl)
                    q = q.join(ProjectTbl)
                    q = q.join(PrincipalInvestigatorTbl)
                    q = q.filter(SampleTbl.name == name)
                    q = q.filter(MaterialTbl.name == mname)
                    q = q.filter(MaterialTbl.grainsize == grainsize)
                    q = q.filter(ProjectTbl.name == pname)
                    q = q.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
                    q = q.filter(PrincipalInvestigatorTbl.last_name == last_name)

                    return q.all()

    def _create(self, data):
        obj = SampleTbl(name=data.get(NAME))

        material = data.get(MATERIAL)
        obj.material = MaterialTbl(name=material.get(NAME),
                                   grainsize=material.get(GRAINSIZE))

        project = data.get(PROJECT)
        proj = ProjectTbl(name=project.get(NAME))

        principal_investigator = project.get(PRINCIPAL_INVESTIGATOR)
        proj.principal_investigator = PrincipalInvestigatorTbl(last_name=principal_investigator.get(LAST_NAME),
                                                               first_initial=principal_investigator.get(FIRST_INITIAL))
        obj.project = proj

        return obj

    def _make_result(self, ri):
        return {ID: ri.id,
                NAME: ri.name,
                MATERIAL: {NAME: ri.material.name,
                           GRAINSIZE: ri.material.grainsize},
                PROJECT: {NAME: ri.project.name,
                          PRINCIPAL_INVESTIGATOR: ri.project.principal_investigator.full_name}}

    def _handle_get_results(self, q, args):
        project = args.get(PROJECT)
        if project:
            q = q.join(ProjectTbl)
            q = q.filter(ProjectTbl.name == project)
            return q

    def _get_parameters(self):
        return {NAME: 'Sample name',
                PROJECT: 'Project name'}

    def _get_example(self):
        return 'sample?project=Toba'

    def _get_fields(self):
        return {ID: 'Sample ID',
                MATERIAL: 'Material name',
                GRAINSIZE: 'Material grainsize',
                PROJECT: 'Project name',
                PRINCIPAL_INVESTIGATOR: 'Principal Investigator name'}


class Project(NameResource):
    _model_klass = ProjectTbl
    _description = 'Route giving access to projects'

    def _get_marshal_fields(self):
        return {NAME: fields.String}

    def _precondition(self, q, data):
        name = data.get(NAME)
        if name:
            principal_investigator = data.get(PRINCIPAL_INVESTIGATOR)
            if principal_investigator:

                # does principal investigator exist
                last_name = principal_investigator.get(LAST_NAME)
                first_initial = principal_investigator.get(FIRST_INITIAL)
                qq = PrincipalInvestigatorTbl.query
                qq = qq.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
                qq = qq.filter(PrincipalInvestigatorTbl.last_name == last_name)

                if not qq.all():
                    return

                q = q.join(PrincipalInvestigatorTbl)
                q = q.filter(ProjectTbl.name == name)
                q = q.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
                q = q.filter(PrincipalInvestigatorTbl.last_name == last_name)

                return q.all()

    def _create(self, data):
        obj = ProjectTbl(name=data.get(NAME),
                         checkin_date=datetime.now().date(),
                         comment=data.get('comment'))

        data = data.get(PRINCIPAL_INVESTIGATOR)
        obj.principal_investigator = PrincipalInvestigatorTbl(last_name=data.get(LAST_NAME),
                                                              first_initial=data.get(FIRST_INITIAL))
        return obj

    def _make_result(self, ri):
        return {ID: ri.id, NAME: ri.name, PRINCIPAL_INVESTIGATOR: ri.principal_investigator.full_name}

    def _get_parameters(self):
        return {NAME: 'project name'}

    def _get_example(self):
        return 'project?name=Toba'

    def _get_fields(self):
        return {ID: 'Project ID',
                NAME: 'Project name',
                PRINCIPAL_INVESTIGATOR: 'Principal Investigator name'}


class Material(NameResource):
    _model_klass = MaterialTbl
    _description = 'Route giving access to materials'

    def _get_marshal_fields(self):
        return {NAME: fields.String,
                GRAINSIZE: fields.String}

    def _precondition(self, q, data):
        name = data.get(NAME)
        if name:
            q = q.filter_by(name=name)

            grainsize = data.get(GRAINSIZE)
            if grainsize:
                q = q.filter_by(grainsize=GRAINSIZE)
            return q.all()

    def _create(self, data):
        return self._model_klass(name=data.get(NAME), grainsize=data.get(GRAINSIZE))

    def _make_result(self, ri):
        return {ID: ri.id,
                NAME: ri.name,
                GRAINSIZE: ri.grainsize}

    def _get_parameters(self):
        return {NAME: 'material name'}

    def _get_example(self):
        return 'material?name=Sanidine'

    def _get_fields(self):
        return {ID: 'Material ID',
                NAME: 'Material name',
                GRAINSIZE: GRAINSIZE}


class PrincipalInvestigator(NameResource):
    _model_klass = PrincipalInvestigatorTbl
    _description = 'Route giving access to materials'

    def _get_marshal_fields(self):
        return {LAST_NAME: fields.String,
                FIRST_INITIAL: fields.String}

    def _precondition(self, q, data):
        last_name = data.get(LAST_NAME)
        if last_name:
            q = q.filter_by(last_name=last_name)
            first_initial = data.get(FIRST_INITIAL)
            if first_initial:
                q = q.filter_by(first_initial=first_initial)

            return q.all()

    def _create(self, data):
        return self._model_klass(last_name=data.get(LAST_NAME),
                                 first_initial=data.get(FIRST_INITIAL))

    def _make_result(self, ri):
        return {ID: ri.id,
                'full_name': ri.full_name,
                LAST_NAME: ri.last_name,
                FIRST_INITIAL: ri.first_initial}

    def _handle_get_results(self, q, args):
        last_name = args.get(LAST_NAME)
        if last_name:
            q = q.filter(PrincipalInvestigatorTbl.last_name == last_name)

        first_initial = args.get(FIRST_INITIAL)
        if first_initial:
            q = q.filter(PrincipalInvestigatorTbl.first_initial == first_initial)
        return q

    def _get_parameters(self):
        return {LAST_NAME: 'principal investigator name'}

    def _get_example(self):
        return 'principal_investigator?name=Mcintosh,W'

    def _get_fields(self):
        return {ID: 'Principal Investigator ID',
                'full name': 'Principal Investigator Full name (i.e. Last Name, First Initial)',
                LAST_NAME: 'Last name',
                FIRST_INITIAL: 'First initial'}


class Analysis(BaseResource):
    _description = 'Route giving access to analyses'

    @auth
    def post(self):
        return '', HTTPStatus.FORBIDDEN

    @auth
    def get(self):
        args = request.args
        project = args.get(PROJECT)
        sample = args.get(SAMPLE)
        material = args.get(MATERIAL)

        def make_result(r):
            return {'RunID': r.runid,
                    'Identifier': r.irradiation_position.identifier,
                    'Aliquot': r.aliquot,
                    'Increment': (r.increment, r.step),
                    'RunDate': r.timestamp.isoformat(),
                    'Sample': r.irradiation_position.sample.name,
                    'Material': r.irradiation_position.sample.material.name,
                    'IrradiationInfo': r.irradiation_info}

        q = AnalysisTbl.query
        q = q.join(IrradiationPositionTbl)
        q = q.join(SampleTbl)

        has_args = False
        if project:
            has_args = True
            q = q.join(ProjectTbl)
            q = q.filter(ProjectTbl.name == project)
            q = q.filter(AnalysisTbl.analysis_type == 'unknown')

        if sample:
            has_args = True
            q = q.filter(SampleTbl.name == sample)

        if material:
            has_args = True
            q = q.join(MaterialTbl)
            q = q.filter(MaterialTbl.name == material)

        if has_args:
            resp = jsonify([make_result(ri) for ri in q.all()])
        else:
            resp = self._handle_get_doc()

        return resp

    def _get_parameters(self):
        return {PROJECT: 'Project name',
                SAMPLE: 'Sample name',
                MATERIAL: 'Material name'}

    def _get_example(self):
        return 'analysis?project=Toba'

    def _get_fields(self):
        return {'RunID': 'Analysis RunID. Unique identifier for the analysis <Identifier>-<Aliquot>[<Step>]',
                'Identifier': 'Identifier. Unique identifier for an irradiation position',
                'Aliquot': 'Aliquot',
                'Increment': 'Increment: Numerical value for a step in an increment heating experiment',
                'RunDate': 'DateTime when analysis was saved',
                'Sample': 'Sample name',
                'Material': 'Material name',
                'IrradiationInfo': 'Irradiation identifier <IrradiationName><Level> <Position>'}
# ============= EOF =============================================
