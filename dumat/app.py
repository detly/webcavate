"""
Copyright 2014 Jason Heeris, jason.heeris@gmail.com

This file is part of the dungeon excavator web interface ("webcavate").

Webcavate is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Webcavate is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
webcavate. If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import uuid

from flask import Flask, render_template, request, make_response, redirect, url_for, flash

from dungeon.excavate import render_room

HELP_TEXT = """\
Web interface to the dungeon excavator."""

app = Flask('dungeon.web')
app.secret_key = str(uuid.uuid4())

@app.route("/")
def root():
    """ Web interface landing page. """
    return render_template('index.html')


@app.route("/error")
def error():
    """ Display errors. """
    return render_template('error.html')


def make_map(request, format):
    tile_size = int(request.form['size'])
    wall_file = request.files['walls']
    floor_file = request.files['floor']
    floorplan_file = request.files['floorplan']

    try:
        room_data, content_type = render_room(
            floor_file.read(),
            wall_file.read(),
            floorplan_file.read(),
            tile_size,
            format
        )
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('error'))

    # Create response
    response = make_response(room_data)
    response.headers['Content-Type'] = content_type
    return response


@app.route("/map.svg", methods=['POST'])
def map_svg():
    return make_map(request, format='svg')


@app.route("/map.png", methods=['POST'])
def map_png():
    return make_map(request, format='png')


@app.route("/map.jpg", methods=['POST'])
def map_jpg():
    return make_map(request, format='jpg')


@app.route("/map", methods=['POST'])
def process():
    """ Process submitted form data. """
    format = request.form['format']

    try:
        node = {
            'png': 'map_png',
            'svg': 'map_svg',
            'jpg': 'map_jpg',
        }[format]
    except KeyError:
        flash("The output format you selected is not supported.")
        return redirect(url_for('error'))
    else:
        return redirect(url_for(node, _method='POST'), code=307)


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

    app.run(port=args.port, host=args.host, debug=False)
