# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from moziris.api.enums import Color
from moziris.api.settings import Settings
from moziris.api.rectangle import Rectangle


class HighlightRectangle(Rectangle):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Color = None,
        thickness: int = None,
    ):
        Rectangle.__init__(self, x, y, width, height)

        if thickness is None:
            thickness = Settings.highlight_thickness

        if color is None:
            color = Settings.highlight_color

        self.color = color
        self.thickness = thickness
