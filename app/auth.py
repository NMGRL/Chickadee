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


class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='{}')".format(self.id)


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


def verify(user, pwd):
    if not (user and pwd) or user != 'ADMIN':
        return False

    if os.getenv('ADMIN_PASSWORD') == pwd:
        return User(id=123)


# ============= EOF =============================================
