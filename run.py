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
import argparse

from flask import Flask, session
from flask_alchy import Alchy

HELP_TEXT = """\
Web interface to the dungeon excavator."""

# The WSGI thingo.
app = Flask(__name__)

# The configuration.
app.config.from_object('config')

# The database.
db = Alchy(app, Model=DumatModel)

# The dumat module.
app.register_blueprint(dumat_app)

# Let there be data.
db.create_all()

# Make sessions have a timeout.
@app.before_request
def make_session_permanent():
    session.permanent = True

def main():
    """ Parse arguments and get things going for the web interface """
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    
    parser.add_argument(
        '-p', '--port',
        help="Port to serve the interface on.",
        type=int,
        default=5050
    )

    parser.add_argument(
        '-a', '--host',
        help="Host to server the interface on.",
    )

    args = parser.parse_args()

    app.run(port=args.port, host=args.host, debug=True)

if __name__ == '__main__':
    main()
