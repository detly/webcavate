# Copyright 2015 Jason Heeris, jason.heeris@gmail.com
# 
# This file is part of the dungeon excavator web interface ("webcavate").
#
# Webcavate is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Webcavate is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# webcavate. If not, see <http://www.gnu.org/licenses/>.

# Debugging is on.
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Session lifetime in seconds.
PERMANENT_SESSION_LIFETIME = 300

# Number of application threads.
THREADS_PER_PAGE = 1

# General security and secret stuff.
CSRF_ENABLED     = True
CSRF_SESSION_KEY = 'f\x86M\xc1k\xfa\x10\xe3\xe7\xed\xb4\xaa\x9eI\xb8\x0fz\xe1Q\xd5\x86\xd9>\x1f'
SECRET_KEY       = '\x9f\t\x8c\xfak\x82\xde%\x7fO\xfa\x02t\xccs\xd6\x9e\\\x1b\xe4k\x89i\xc5'
