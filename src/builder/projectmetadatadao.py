# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import sqlite3

from .projectmetadatadto import ProjectMetaDataDto


class ProjectMetaDataDao(object):

    def __init__(self):
        self.connection = None

    def create_model(self):
        c = self.connection.cursor()
        command = ('CREATE TABLE IF NOT EXISTS projects ('
                   'name TEXT PRIMARY KEY,'
                   'last_fetch TIMESTAMP,'
                   'last_translation_update TIMESTAMP,'
                   'words INTEGER,'
                   'checksum TEXT'
                   ');')
        c.execute(command)

        command = 'CREATE INDEX IF NOT EXISTS [ix_name] ON [projects] ([name]);'
        c.execute(command)
        self.connection.commit()

    def open(self, database_name):
        self.connection = sqlite3.connect(database_name,
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        self.create_model()

    def put(self, dto):
        c = self.connection.cursor()
        command = (u"INSERT OR REPLACE INTO 'projects' VALUES ('{0}', '{1}', "
                   u"'{2}', {3}, '{4}');")
        command = command.format(dto.name, dto.last_fetch,
                                 dto.last_translation_update, dto.words,
                                 dto.checksum)
        c.execute(command)
        self.connection.commit()

    def get(self, name):
        c = self.connection.cursor()
        command = u"SELECT * FROM projects WHERE name='{0}'".format(name)
        result = c.execute(command)
        row = result.fetchone()

        if row is None:
            return None

        dto = ProjectMetaDataDto(row[0])
        dto.last_fetch = row[1]
        dto.last_translation_update = row[2]
        dto.words = row[3]
        dto.checksum = row[4]
        return dto

    def dump(self):
        c = self.connection.cursor()
        command = u'SELECT * FROM projects'
        result = c.execute(command)
        print('Database rows')
        for row in result:
            print (row)

    def close(self):
        self.connection.close()
