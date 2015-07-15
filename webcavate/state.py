# Copyright 2015 Jason Heeris, jason.heeris@gmail.com
# 
# This file is part of the dungeon excavator web interface ("Dumat").
#
# Dumat is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Dumat is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Dumat. If not, see <http://www.gnu.org/licenses/>.
"""
Dumat's state has a unique identifier, three input files, a flag that indicates
whether it's processing, and a name for the session.
"""
from uuid import uuid4

from alchy import ModelBase, make_declarative_base
from sqlalchemy import orm, Column, types, sql

Model = make_declarative_base(Base=ModelBase)

class DumatState(Model):

    __tablename__ = 'dumat'

    id      = Column(types.Integer()        , primary_key=True)
    key     = Column(types.BINARY(length=16), nullable=False, unique=True)
    name    = Column(types.UnicodeText())

    floor_path  = Column(types.UnicodeText())
    wall_path   = Column(types.UnicodeText())
    map_path    = Column(types.UnicodeText())
    result_path = Column(types.UnicodeText())

    processing = Column(types.Boolean(), nullable=False)

    touched = Column(
        types.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now())

    def __init__(self):
        self.key = uuid4().bytes
        self.one = False
        self.two = False