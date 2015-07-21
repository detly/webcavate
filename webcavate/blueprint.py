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
from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash, session
import sqlalchemy.orm.exc as sql_exc

import webcavate.state
from webcavate.state import WebcavateState
from webcavate import forms

from dumat.excavate import render_room

HELP_TEXT = """\
Web interface to the dungeon excavator."""

webcavate_bp = Blueprint(
    'webcavate',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/webcavate')

# Workflow is:
#  1. Upload floor texture.
#  2. Upload wall texture.
#  3. Upload floorplan.
#  4. Set tile size and output format and submit for processing.

def format_key(data):
    """
    Converts the database key to a formatted string, where each byte is
    represented as hexadecimal.
    """
    return ' '.join('{:02X}'.format(byte) for byte in data)

def make_the_thing_exist(session):
    """
    If the session contains a valid ID for a state, return the state. Otherwise
    create a new state, update the session with the ID, and return the new
    state. 
    """
    # If the browser doesn't remember a session, make a new one
    create_state = False

    if 'state' not in session:
        create_state = True
    else:
        state_key = session['state']

        state_query = WebcavateState.query.filter_by(key = state_key)
        
        try:
            state = state_query.one()
        except sql_exc.NoResultFound:
            create_state = True

        # sql_exc.MultipleResultsFound is actually an error, and should be
        # handled properly.

    if create_state:
        state = WebcavateState()
        session['state'] = state.key
        state.save()
        state.session().commit()

    assert(state != None)
    assert(session['state'] == state.key)

    return state


@webcavate_bp.route("/")
def root():
    """ Web interface landing page. """
    webcavate_state = make_the_thing_exist(session)
    key_string = format_key(webcavate_state.key)

    if webcavate_state.status == webcavate.state.STATUS_SETUP:
        if webcavate_state.floor_path is None:
            return render_template('floor.html', form=forms.FloorTextureForm(), key_string=key_string)
        elif webcavate_state.wall_path is None:
            return render_template('wall.html', form=forms.WallTextureForm(), key_string=key_string)
        elif webcavate_state.plan_path is None:
            return render_template('plan.html', form=forms.FloorplansForm(), key_string=key_string)
        else:
            return render_template('settings.html', form=forms.SettingsForm(), key_string=key_string)
    else:
        return render_template('progress.html', key_string=key_string)

@webcavate_bp.route("/set/floor", methods=("GET", "POST"))
def set_floor():
    form = forms.FloorTextureForm(request.form)

    if form.validate_on_submit():
        flash("Feature not supported.")
    else:
        flash("The given data wasn't valid.")

    return redirect(url_for('.root'))

@webcavate_bp.route("/error")
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


@webcavate_bp.route("/map.svg", methods=['POST'])
def map_svg():
    return make_map(request, format='svg')


@webcavate_bp.route("/map.png", methods=['POST'])
def map_png():
    return make_map(request, format='png')


@webcavate_bp.route("/map.jpg", methods=['POST'])
def map_jpg():
    return make_map(request, format='jpg')


@webcavate_bp.route("/map", methods=['POST'])
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
