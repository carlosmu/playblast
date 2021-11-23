
import bpy
import os
import pathlib


def not_saved(self, context):
    self.layout.label(text="Please save your blend file first.")
def folder_popup(self, context):
    self.layout.label(text="Make a new playblast to solve the issue.")

class PL_OT_open_filebrowser(bpy.types.Operator):
    """Open file browser that contains the Playblast Files"""
    bl_idname = "playblast.open_filebrowser"
    bl_label = "Open Playblast folder"
    bl_options = {'REGISTER', 'UNDO'}

    # Prevents operator appearing in unsupported editors
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):

        if not bpy.data.is_saved:
            context.window_manager.popup_menu(not_saved, title="File not saved", icon='ERROR')
        else:
            prefs = context.preferences.addons[__package__].preferences

            # Get scene and file render output
            file_scene = bpy.context.scene.name_full
            file_output = bpy.data.scenes[file_scene].render.filepath

            # Get filename
            file_name = ""
            file_name = bpy.path.basename(bpy.data.filepath)
            file_name = os.path.splitext(file_name)[0]

            # Define Prefix
            prefix = ""
            if prefs.pb_prefix_options == 'FILE_NAME':
                prefix = file_name + prefs.pb_separator
            elif prefs.pb_prefix_options == 'CUSTOM_PREFIX':
                prefix = prefs.pb_custom_prefix + prefs.pb_separator
            else:
                pass

            # Define Output Path
            output = ""
            subfolder = ""
            subfolder = prefs.pb_subfolder_name + "/"

            if prefs.pb_output_options == 'PROYECT_FOLDER':
                if prefs.pb_subfolder:
                    output = "//" + subfolder
                else:
                    output = "//"
            elif prefs.pb_output_options == 'SYSTEM_FOLDER':
                if prefs.pb_subfolder:
                    output = prefs.pb_system_folder + subfolder
                else:
                    output = prefs.pb_system_folder
            else:
                if prefs.pb_subfolder:
                    output = file_output + subfolder
                else:
                    output = file_output

            # Add prefix to output
            output_dir = output
            output = output + prefix

            # Absolute path
            sane_path = lambda p: os.path.abspath(bpy.path.abspath(p))
            abs_output = sane_path(output)

            # Only folder Absolute path
            abs_output_dir = sane_path(output_dir)

            try:
                bpy.ops.wm.path_open(filepath=str(pathlib.Path(abs_output).parent))
            except:
                title = f"Dir: {abs_output_dir} not found."
                context.window_manager.popup_menu(folder_popup, title=title, icon='ERROR')

        return{'FINISHED'}

    
##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(PL_OT_open_filebrowser)

def unregister():
    bpy.utils.unregister_class(PL_OT_open_filebrowser)