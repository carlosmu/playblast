# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

####################################
# IMPORT MODULES
####################################

from . import draw_button
from . import op_playblast
from . import op_player
from . import op_turnaround_camera
from . import op_open_filebrowser
from . import op_open_preferences
from . import op_version_numbering
from . import popover
from . import user_prefs
from . import keymap

bl_info = {
    "name": "Playblast",
    "author": "carlosmu <carlos.damian.munoz@gmail.com>",
    "blender": (2, 83, 0),
    "version": (1, 2, 3),
    "category": "Animation",
    "location": "3D View Main Menu and/or Right Click Context Menu",
    "description": "Improves viewport render animation user experience",
    "warning": "",
    "doc_url": "https://blendermarket.com/products/playblast",
    "tracker_url": "https://blendermarket.com/creators/carlosmu",
}

####################################
# REGISTER/UNREGISTER
####################################


def register():
    draw_button.register()
    op_playblast.register()
    op_player.register()
    op_turnaround_camera.register()
    op_open_filebrowser.register()
    op_open_preferences.register()
    op_version_numbering.register()
    popover.register()
    user_prefs.register()
    keymap.register()


def unregister():
    draw_button.unregister()
    op_playblast.unregister()
    op_player.unregister()
    op_turnaround_camera.unregister()
    op_open_filebrowser.unregister()
    op_open_preferences.unregister()
    op_version_numbering.unregister()
    popover.unregister()
    user_prefs.unregister()
    keymap.unregister()