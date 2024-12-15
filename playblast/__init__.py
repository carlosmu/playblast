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

bl_info = {
    "name": "Playblast",
    "author": "carlosmu <carlos.damian.munoz@gmail.com>",
    "blender": (3, 6, 0),
    "version": (1, 3, 1),
    "category": "Animation",
    "location": "3D View Main Menu and/or Right Click Context Menu",
    "description": "This addon allows you to keep renders options and playblast options separately",
    "warning": "",
    "doc_url": "https://blendermarket.com/products/playblast",
    "tracker_url": "https://blendermarket.com/creators/carlosmu",
}

import bpy
import importlib

####################################
# IMPORT MODULES
####################################

from . import keymap
from . import op_open_filebrowser
from . import op_open_preferences
from . import op_playblast
from . import op_player
from . import op_turnaround_camera
from . import op_version_numbering
from . import pt_popover
from . import user_prefs

# For reaload modules when updating addon
if "bpy" in locals():    
    importlib.reload(keymap)
    importlib.reload(op_open_filebrowser)
    importlib.reload(op_open_preferences)
    importlib.reload(op_playblast)
    importlib.reload(op_player)
    importlib.reload(op_turnaround_camera)
    importlib.reload(op_version_numbering)
    importlib.reload(pt_popover)
    importlib.reload(user_prefs)


####################################
# REGISTER/UNREGISTER
####################################


def register():
    keymap.register()
    op_open_filebrowser.register()
    op_open_preferences.register()
    op_playblast.register()
    op_player.register()
    op_turnaround_camera.register()
    op_version_numbering.register()
    pt_popover.register()
    user_prefs.register()


def unregister():
    keymap.unregister()
    op_open_filebrowser.unregister()
    op_open_preferences.unregister()
    op_playblast.unregister()
    op_player.unregister()
    op_turnaround_camera.unregister()
    op_version_numbering.unregister()
    pt_popover.unregister()
    user_prefs.unregister()