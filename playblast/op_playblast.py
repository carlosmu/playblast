import bpy

from .user_prefs import PB_Prefs

##############################################
#   MAIN OPERATOR
##############################################

class PL_OT_playblast(bpy.types.Operator):
    """Improves viewport render animation user experience"""
    bl_idname = "pl.playblast"
    bl_label = "Playblast"  
    bl_options = {'REGISTER', 'UNDO'}
 
    # Prevents operator appearing in unsupported editors
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True 


    ##############################################
    #   Playblast functionality
    ##############################################
    def execute(self, context): 
        # pb_autoplay = context.preferences.addons[__package__].preferences.pb_output
        pb_format = context.preferences.addons[__package__].preferences.pb_format
        pb_container = context.preferences.addons[__package__].preferences.pb_container
        pb_audio = context.preferences.addons[__package__].preferences.pb_audio
        pb_resolution = context.preferences.addons[__package__].preferences.pb_resolution
        pb_stamp = context.preferences.addons[__package__].preferences.pb_stamp
        pb_autoplay = context.preferences.addons[__package__].preferences.pb_autoplay

        # Save file render settings
        scene =  bpy.context.scene.name_full # Scene
        output = bpy.data.scenes[scene].render.filepath # Output path
        format = bpy.data.scenes[scene].render.image_settings.file_format # Output file format
        container = bpy.data.scenes[scene].render.ffmpeg.format # Output file container
        audio = bpy.data.scenes[scene].render.ffmpeg.audio_codec
        resolution = bpy.data.scenes[scene].render.resolution_percentage
        stamp = bpy.data.scenes[scene].render.use_stamp # Use Stamp

        # Overwrite file settings
        bpy.data.scenes[scene].render.filepath = '//'
        bpy.data.scenes[scene].render.image_settings.file_format = pb_format
        if pb_format == 'FFMPEG':
            bpy.data.scenes[scene].render.ffmpeg.format = pb_container
            bpy.data.scenes[scene].render.ffmpeg.audio_codec = pb_audio
        bpy.data.scenes[scene].render.resolution_percentage = pb_resolution
        bpy.data.scenes[scene].render.use_stamp = pb_stamp

        bpy.ops.render.opengl(animation=True)

        if pb_autoplay:
            bpy.ops.render.play_rendered_anim()

        # Recover previous file settings
        bpy.data.scenes[scene].render.filepath = output
        bpy.data.scenes[scene].render.image_settings.file_format = format
        bpy.data.scenes[scene].render.ffmpeg.format = container
        bpy.data.scenes[scene].render.ffmpeg.audio_codec = audio
        bpy.data.scenes[scene].render.resolution_percentage = resolution
        bpy.data.scenes[scene].render.use_stamp = stamp

        return{'FINISHED'}

##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(PL_OT_playblast)
        
def unregister():
    bpy.utils.unregister_class(PL_OT_playblast)