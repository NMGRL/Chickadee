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
from http import HTTPStatus

from flask import request, jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, marshal_with
from app.api import __api_version__
from app.server import db

LAST_NAME = 'last_name'
FIRST_INITIAL = 'first_initial'
GRAINSIZE = 'grainsize'
PROJECT = 'project'
MATERIAL = 'material'
NAME = 'name'
PRINCIPAL_INVESTIGATOR = 'principal_investigator'
SAMPLE = 'sample'
ID = 'id'


def auth(func):
    # disable authorization for browswer based api testing only
    if os.getenv('JWT_ENABLED') == '1':
        return jwt_required()(func)
    else:
        return func


class BaseResource(Resource):
    _description = 'No description'

    def _get_marshal_fields(self):
        return

    def _get_description(self):
        return self._description

    def _get_parameters(self):
        return

    def _get_example(self):
        return

    def _get_fields(self):
        return

    def _handle_get_doc(self):
        return {'success': {'v': __api_version__,
                            'description': self._get_description(),
                            'options': {'parameters': self._get_parameters()},
                            'example': 'api/{}/{}'.format(__api_version__, self._get_example()),
                            'fields': self._get_fields()}}

    @auth
    def get(self):
        return self._get_hook()

    @auth
    def post(self):
        mf = self._get_marshal_fields()
        if mf:
            func = marshal_with(mf)

        return func(self._post_hook())


class NameResource(BaseResource):
    def _get_results(self, model):
        args = request.args

        q = None
        if args.get('all') == '1':
            q = model.query
        else:
            name = args.get(NAME)
            if name:
                q = model.query
                q = self._handle_get_results(q, args)
                q = q.filter(model.name == name)

        if q is None:
            ret = self._handle_get_doc()
        else:
            ret = q.all()
        return ret

    def _get_hook(self):
        results = self._get_results(self._model_klass)
        if isinstance(results, list):
            results = [self._make_result(result) for result in results]

        return jsonify(results)

    def _make_result(self, ri):
        raise NotImplementedError

    def _handle_get_results(self, q, args):
        return q

    def _precondition(self, q, data):
        pass

    def _create(self, data):
        pass

    def _post_hook(self):
        data = request.get_json(force=True)
        q = self._model_klass.query
        pc = self._precondition(q, data)
        if pc is None:
            return '', HTTPStatus.BAD_REQUEST
        elif pc:
            return '', HTTPStatus.PRECONDITION_FAILED

        obj = self._create(data)
        db.session.add(obj)
        db.session.commit()
        return obj, HTTPStatus.CREATED

# ============= EOF =============================================
