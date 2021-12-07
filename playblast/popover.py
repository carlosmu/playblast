import bpy
    
class PL_PT_popover(bpy.types.Panel):
    """Playblast Popover for main menu"""
    bl_label = "Playblast Options"
    bl_idname = "playblast.popover"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.scale_y = 1.25
        col.operator("playblast.playblast", icon='FILE_MOVIE')

        row = col.row(align=True)
        row.operator("playblast.player", icon='PLAY')
        row.operator("playblast.open_filebrowser", icon='FILEBROWSER', text="Open Folder")
        
        layout.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER', text="Add Turnaround Camera")

        layout.operator("playblast.open_preferences", icon='PREFERENCES')       
        

def popover(self, context):
    prefs = context.preferences.addons[__package__].preferences
    if prefs.pb_enable_3dview_menu:
        if bpy.context.area.show_menus:
            self.layout.popover("playblast.popover", text="", icon='FILE_MOVIE')
        else:
            self.layout.popover("playblast.popover", icon='FILE_MOVIE')

####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(popover)

def unregister():
    bpy.utils.unregister_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover)