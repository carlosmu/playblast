import bpy

class PL_OT_increase_version(bpy.types.Operator):
    """Increase Version Number"""
    bl_idname = "playblast.increase_version"
    bl_label = "Increase Version"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):
        context.scene.version_number += 1
        return{'FINISHED'}

class PL_OT_decrease_version(bpy.types.Operator):
    """Decrease Version Number"""
    bl_idname = "playblast.decrease_version"
    bl_label = "Decrease Version"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):
        context.scene.version_number -= 1
        return{'FINISHED'}

##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(PL_OT_increase_version)
    bpy.utils.register_class(PL_OT_decrease_version)


def unregister():
    bpy.utils.unregister_class(PL_OT_increase_version)
    bpy.utils.unregister_class(PL_OT_decrease_version)