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
from flask import render_template

from flask import Flask
from os import getenv

from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from app.auth import verify, identity


user = getenv('ARGONSERVER_DB_USER')
pwd = getenv('ARGONSERVER_DB_PWD')
host = getenv('ARGONSERVER_HOST')
dbname = getenv('PYCHRON_DB_NAME')

uri = 'mysql+pymysql://{}:{}@{}/{}?connect_timeout=3'.format(user, pwd, host, dbname)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

db = SQLAlchemy(app)
jwt = JWT(app, verify, identity)


@app.route('/')
def index():
    return render_template('index.html')


from app.api import api_blueprint
app.register_blueprint(api_blueprint)

# ============= EOF =============================================


