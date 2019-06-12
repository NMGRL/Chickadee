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
from sqlalchemy.ext.declarative import declared_attr

from app.server import db

# adapted from https://codereview.stackexchange.com/questions/182733/base-26-letters-and-base-10-using-recursion
BASE = 26
A_UPPERCASE = ord('A')


def alphas(n):
    a = ''
    if n is not None and n >= 0:
        def decompose(n):
            while n:
                n, rem = divmod(n, BASE)
                yield rem

        digits = reversed([chr(A_UPPERCASE + part) for part in decompose(n)])
        a = ''.join(digits)
    return a


def alpha_to_int(l):
    return sum((ord(li) - A_UPPERCASE) * BASE ** i for i, li in enumerate(reversed(l.upper())))


class Base(object):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__


class Named(object):
    name = db.Column(db.String(80))


class SampleTbl(Base, Named, db.Model):
    projectID = db.Column(db.Integer, db.ForeignKey('ProjectTbl.id'))
    materialID = db.Column(db.Integer, db.ForeignKey('MaterialTbl.id'))

    project = db.relationship('ProjectTbl', backref=db.backref('samples', lazy=True))
    material = db.relationship('MaterialTbl', backref=db.backref('materials', lazy=True))


class ProjectTbl(Base, Named, db.Model):
    principal_investigatorID = db.Column(db.Integer, db.ForeignKey('PrincipalInvestigatorTbl.id'))

    principal_investigator = db.relationship('PrincipalInvestigatorTbl', backref=db.backref('projects', lazy=True))


class MaterialTbl(Base, Named, db.Model):
    grainsize = db.Column(db.String(80))


class PrincipalInvestigatorTbl(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(120))
    first_initial = db.Column(db.String(120))

    @property
    def full_name(self):
        name = self.last_name
        if self.first_initial:
            name = '{}, {}'.format(name, self.first_initial)
        return name


class AnalysisTbl(Base, db.Model):
    timestamp = db.Column(db.DateTime)
    aliquot = db.Column(db.Integer)
    increment = db.Column(db.Integer, nullable=True)
    analysis_type = db.Column(db.String(80))

    irradiation_positionID = db.Column(db.Integer, db.ForeignKey('IrradiationPositionTbl.id'))
    irradiation_position = db.relationship('IrradiationPositionTbl')

    @property
    def step(self):
        inc = self.increment
        if inc is not None:
            s = alphas(inc)
        else:
            s = ''
        return s

    @property
    def runid(self):
        return '{}-{}{}'.format(self.irradiation_position.identifier, self.aliquot, self.step)

    @property
    def irradiation_info(self):

        level = self.irradiation_position.level
        irrad = level.irradiation

        return '{}{} {}'.format(irrad.name, level.name, self.irradiation_position.position)


class IrradiationPositionTbl(Base, db.Model):
    identifier = db.Column(db.String(80))
    position = db.Column(db.Integer)

    levelID = db.Column(db.Integer, db.ForeignKey('LevelTbl.id'))
    level = db.relationship('LevelTbl')

    sampleID = db.Column(db.Integer, db.ForeignKey('SampleTbl.id'))
    sample = db.relationship('SampleTbl')


class IrradiationTbl(Base, Named, db.Model):
    pass


class LevelTbl(Base, Named, db.Model):
    irradiationID = db.Column(db.Integer, db.ForeignKey('IrradiationTbl.id'))
    irradiation = db.relationship('IrradiationTbl')

# ============= EOF =============================================
