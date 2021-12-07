import bpy

class PL_OT_open_preferences(bpy.types.Operator):
    """Open Addon Preferences"""
    bl_idname = "playblast.open_preferences"
    bl_label = "Preferences"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = "Playblast"

        return{'FINISHED'}

##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(PL_OT_open_preferences)


def unregister():
    bpy.utils.unregister_class(PL_OT_open_preferences)