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
""" Forms for the dungeon excavator web interface. """
from flask_wtf import Form
from wtforms.fields import FileField, SubmitField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets.html5 import NumberInput

class BetterNumberInput(NumberInput):

    def __init__(self, step=None, min=None, max=None):
        super().__init__(step)
        self.min = min
        self.max = max

    def __call__(self, field, **kwargs):
        if self.min is not None:
            kwargs.setdefault('min', self.min)
        
        if self.max is not None:
            kwargs.setdefault('max', self.max)

        return super().__call__(field, **kwargs)

class IncrementalForm(Form):
    submit = SubmitField("Next…")

class FloorTextureForm(IncrementalForm):
    texture = FileField(
        "Select the floor texture. This will be tiled (repeated) underneath the"
        " other texture. It should be a PNG image.")

class WallTextureForm(IncrementalForm):
    texture = FileField(
        "Select the wall texture. This will be tiled everywhere the floor "
        "isn't. It should be a PNG image.")

class FloorplanForm(IncrementalForm):
    texture = FileField(
        "Select the floorplan. This should be a black and white image — any "
        "common bitmap format, eg. PNG, JPG, BMP; or an SVG image. If "
        "it&rsquo;s a bitmap image, it should be black where you want the floor"
        " to show and white or transparent everywhere else. If it&rsquo;s an "
        "SVG image, the first path in the file will be used.")

class SettingsForm(Form):
    size = IntegerField(
        "In the images, how many pixels represent a single tile? This will be "
        "used to scale visual effects such as lighting and the border.",
        default=100,
        widget=BetterNumberInput(step=1, min=0)
        )

    format = SelectField(
        "What format do you want the result in? PNG/JPEG is good for immediate"
        "use eg. uploading to a TRPG service (JPEG is much smaller, so good for"
        "maps bigger than about 1000px in any direction), whereas SVG is good"
        "for further editing (eg. in Inkscape).",
        choices=(
            ('png', "PNG"),
            ('jpg', "JPEG"),
            ('svg', "SVG"))
        )

    submit = SubmitField("Generate map…")
