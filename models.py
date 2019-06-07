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
from application import db


class SampleTbl(db.Model):
    __tablename__ = 'SampleTbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    projectID = db.Column(db.Integer, db.ForeignKey('ProjectTbl.id'))
    materialID = db.Column(db.Integer, db.ForeignKey('MaterialTbl.id'))

    project = db.relationship('ProjectTbl', backref=db.backref('samples', lazy=True))
    material = db.relationship('MaterialTbl', backref=db.backref('materials', lazy=True))


class ProjectTbl(db.Model):
    __tablename__ = 'ProjectTbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    principal_investigatorID = db.Column(db.Integer, db.ForeignKey('PrincipalInvestigatorTbl.id'))

    principal_investigator = db.relationship('PrincipalInvestigatorTbl', backref=db.backref('projects', lazy=True))


class MaterialTbl(db.Model):
    __tablename__ = 'MaterialTbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    grainsize = db.Column(db.String(80))


class PrincipalInvestigatorTbl(db.Model):
    __tablename__ = 'PrincipalInvestigatorTbl'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(120))
    first_initial = db.Column(db.String(120))

    @property
    def full_name(self):
        name = self.last_name
        if self.first_initial:
            name = '{}, {}'.format(name, self.first_initial)
        return name

# ============= EOF =============================================
