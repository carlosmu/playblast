import bpy


class PL_PT_popover(bpy.types.Panel):
    """Playblast Popover for main menu"""
    bl_label = "Playblast Popover"
    bl_idname = "playblast.popover"
    # bl_options = {'INSTANCED'}
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        col = layout.column(align=True)
        col.operator("playblast.playblast", icon='FILE_MOVIE')

        row = col.row(align=True)
        row.operator("playblast.player", icon='PLAY')
        row.operator("playblast.open_filebrowser", icon='FILEBROWSER', text="Open Folder")
        
        col.separator()
        col.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER', text="Add Turnaround Camera")

        col.separator()
        col.operator("playblast.open_preferences", icon='PREFERENCES')       
        

def popover(self, context):
    self.layout.popover("playblast.popover", text="", icon='FILE_MOVIE')

def register():
    bpy.utils.register_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(popover)


def unregister():
    bpy.utils.unregister_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover)