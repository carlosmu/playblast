import bpy
import os

# All pb_ variables come from user prefs, don't overwrite them

##############################################
#   MAIN OPERATOR
##############################################

def warning(self, context):
    self.layout.label(text="Please save your .blend file first")
def codecs_error(self, context):
    self.layout.label(text="An error occurred with codecs, try again or choose another container/codec")
def videoplayer_error(self, context):
    self.layout.label(text="An error occurred with videoplayer, check your aplication videoplayer preferences")

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

        # If file is not saved, show warning message
        if bpy.data.is_saved:       
            self.playblast(context)
        else:
            context.window_manager.popup_menu(warning, title="File not saved", icon='ERROR')
        return{'FINISHED'}

    def playblast(self, context):
        
        prefs = context.preferences.addons[__package__].preferences

        #################################
        # Save current file render settings
        #################################
        file_scene =  bpy.context.scene.name_full # Scene
        file_output = bpy.data.scenes[file_scene].render.filepath # Output path
        file_format = bpy.data.scenes[file_scene].render.image_settings.file_format # Output file format
        if file_format == 'FFMPEG': # Only save container and audio in FFMPEG format
            file_container = bpy.data.scenes[file_scene].render.ffmpeg.format # Output file container
            file_audio = bpy.data.scenes[file_scene].render.ffmpeg.audio_codec
            file_video_codec = bpy.data.scenes[file_scene].render.ffmpeg.codec
        file_resolution = bpy.data.scenes[file_scene].render.resolution_percentage
        file_stamp = bpy.data.scenes[file_scene].render.use_stamp # Use Stamp
        file_stamp_font_size = bpy.data.scenes[file_scene].render.stamp_font_size
        file_transparent = bpy.data.scenes[file_scene].render.film_transparent # Film Transparent
        file_overlays = bpy.context.space_data.overlay.show_overlays # Overlays
        file_bone_overlays = bpy.context.space_data.overlay.show_bones # Bone overlays

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
        output = output + prefix

        #################################
        # Overwrite file settings
        #################################
        bpy.data.scenes[file_scene].render.filepath = output

        bpy.data.scenes[file_scene].render.image_settings.file_format = prefs.pb_format
        if prefs.pb_format == 'FFMPEG':
            bpy.data.scenes[file_scene].render.ffmpeg.format = prefs.pb_container
            bpy.data.scenes[file_scene].render.ffmpeg.codec = prefs.pb_video_codec
            bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = prefs.pb_audio
        bpy.data.scenes[file_scene].render.resolution_percentage = prefs.pb_resolution
        bpy.data.scenes[file_scene].render.use_stamp = prefs.pb_stamp
        if prefs.pb_stamp:
            bpy.data.scenes[file_scene].render.stamp_font_size = prefs.pb_stamp_font_size
        if prefs.pb_show_environment:
            bpy.data.scenes[file_scene].render.film_transparent = False
        # Overlays
        if prefs.pb_overlays == 'ALL':
            bpy.context.space_data.overlay.show_overlays = False
        elif prefs.pb_overlays == 'BONES':
            bpy.context.space_data.overlay.show_bones = False
        else:
            pass
        
        # Try to create the video, but mainly protect the user's data
        try:
            bpy.ops.render.opengl(animation=True)
            if prefs.pb_autoplay:
                try:
                    bpy.ops.render.play_rendered_anim() 
                except: 
                    context.window_manager.popup_menu(videoplayer_error, title="Video player error", icon='ERROR')     
        except:
            context.window_manager.popup_menu(codecs_error, title="Codecs error", icon='ERROR')    
        finally:
            #################################
            # Recover previous file settings
            #################################
            bpy.data.scenes[file_scene].render.filepath = file_output
            bpy.data.scenes[file_scene].render.image_settings.file_format = file_format
            if file_format == 'FFMPEG':
                bpy.data.scenes[file_scene].render.ffmpeg.format = file_container
                bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = file_audio
                bpy.data.scenes[file_scene].render.ffmpeg.codec = file_video_codec
            bpy.data.scenes[file_scene].render.resolution_percentage = file_resolution
            bpy.data.scenes[file_scene].render.use_stamp = file_stamp
            bpy.data.scenes[file_scene].render.stamp_font_size = file_stamp_font_size
            bpy.data.scenes[file_scene].render.film_transparent = file_transparent
            bpy.context.space_data.overlay.show_overlays = file_overlays
            bpy.context.space_data.overlay.show_bones = file_bone_overlays

##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(PL_OT_playblast)
        
def unregister():
    bpy.utils.unregister_class(PL_OT_playblast)