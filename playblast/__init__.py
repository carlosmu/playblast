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
    "name" : "Playblast",
    "author" : "carlosmu <carlos.damian.munoz@gmail.com>",    
    "blender" : (2, 83, 0),
    "version" : (0, 4, 0),
    "category" : "Animation",
    "location" : "3D View Main Menu",
    "description" : "Improves viewport render animation user experience",
    "warning" : "",
    "doc_url" : "",
    "tracker_url" : "https://blendermarket.com/creators/carlosmu",
}

import bpy

from . import draw_button
from . import op_playblast
from . import user_prefs

####################################
# REGISTER/UNREGISTER
####################################
def register():
    draw_button.register()
    op_playblast.register() 
    user_prefs.register()   
        
def unregister():
    draw_button.unregister()
    op_playblast.unregister() 
    user_prefs.unregister() 