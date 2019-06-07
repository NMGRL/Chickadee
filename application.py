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
from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy


class Chickadee(Flask):
    def __init__(self, *args, **kw):
        super(Chickadee, self).__init__(*args, **kw)
        self.jinja_options = dict(Flask.jinja_options)
        # self.jinja_options['extensions'] = ['jinja2_highlight.HighlightExtension']


app = Chickadee(__name__)

user = getenv('ARGONSERVER_DB_USER')
pwd = getenv('ARGONSERVER_DB_PWD')
host = getenv('ARGONSERVER_HOST')
name = 'pychrondvc_samplesubmit'

uri = 'mysql+pymysql://{}:{}@{}/{}?connect_timeout=3'.format(user, pwd, host, name)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# ============= EOF =============================================
