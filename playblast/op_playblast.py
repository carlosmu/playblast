import bpy
import os

# All pb_ variables come from user prefs, don't overwrite them

##############################################
#   MAIN OPERATOR
##############################################

def warning(self, context):
    self.layout.label(text="Please save your blend file first")
def codecs_error(self, context):
    self.layout.label(text="Set resolution divisible by 2, or choose another container/codec combination")
def videoplayer_error(self, context):
    self.layout.label(text="Check your aplication videoplayer preferences")

class PL_OT_playblast(bpy.types.Operator):
    """Quick viewport render of the animation range"""
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
        file_scene =  bpy.context.scene.name_full # Scene Name
        file_output = bpy.data.scenes[file_scene].render.filepath # Output path
        file_format = bpy.data.scenes[file_scene].render.image_settings.file_format # Output file format
        if file_format == 'FFMPEG': # Only save container and audio in FFMPEG format
            file_container = bpy.data.scenes[file_scene].render.ffmpeg.format # Video Container
            file_video_codec = bpy.data.scenes[file_scene].render.ffmpeg.codec # Video Codec
            file_gop = bpy.data.scenes[file_scene].render.ffmpeg.gopsize # GOP
            file_audio = bpy.data.scenes[file_scene].render.ffmpeg.audio_codec # Audio codec
        file_color_mode = bpy.data.scenes[file_scene].render.image_settings.color_mode # Color Mode
        file_color_depth = bpy.data.scenes[file_scene].render.image_settings.color_depth # Color Depth
        file_resolution_x = bpy.data.scenes[file_scene].render.resolution_x # X Resolution
        file_resolution_y = bpy.data.scenes[file_scene].render.resolution_y # Y Resolution
        file_resolution_percentage = bpy.data.scenes[file_scene].render.resolution_percentage # Resolution Percentage
        file_stamp = bpy.data.scenes[file_scene].render.use_stamp # Use Stamp
        file_stamp_font_size = bpy.data.scenes[file_scene].render.stamp_font_size # Stamp font size
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

        # Define resolution x and y, and force divisible
        if prefs.pb_resize_method == 'PERCENTAGE':
            divisor = 100 / prefs.pb_resize_percentage # Simple division needed, for precision
            resolution_x = int(file_resolution_x // divisor)
            resolution_y = int(file_resolution_y // divisor)
            resolution_x = self.force_divisible(resolution_x)
            resolution_y = self.force_divisible(resolution_y)
        elif prefs.pb_resize_method == 'MAX_HEIGHT': 
            divisor = file_resolution_y / prefs.pb_resize_max_height # Simple division needed, for precision
            resolution_x = int(file_resolution_x // divisor)
            resolution_y = int(file_resolution_y // divisor)
            resolution_x = self.force_divisible(resolution_x)
            resolution_y = self.force_divisible(resolution_y)
        else:
            pass

        #################################
        # Overwrite file settings
        #################################
        bpy.data.scenes[file_scene].render.filepath = output

        bpy.data.scenes[file_scene].render.image_settings.file_format = prefs.pb_format

        if prefs.pb_format == 'FFMPEG':
            bpy.data.scenes[file_scene].render.ffmpeg.format = prefs.pb_container
            bpy.data.scenes[file_scene].render.ffmpeg.codec = prefs.pb_video_codec
            bpy.data.scenes[file_scene].render.ffmpeg.gopsize = prefs.pb_gop
            bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = prefs.pb_audio

        if prefs.pb_resize_method == 'PERCENTAGE' or prefs.pb_resize_method == 'MAX_HEIGHT':
            bpy.data.scenes[file_scene].render.resolution_x = resolution_x
            bpy.data.scenes[file_scene].render.resolution_y = resolution_y
            bpy.data.scenes[file_scene].render.resolution_percentage = 100 # Prevents unwanted resizing

        bpy.data.scenes[file_scene].render.use_stamp = prefs.pb_stamp
        if prefs.pb_stamp:
            bpy.data.scenes[file_scene].render.stamp_font_size = prefs.pb_stamp_font_size
        
        if prefs.pb_show_environment:
            bpy.data.scenes[file_scene].render.film_transparent = False
        
        if prefs.pb_overlays == 'ALL':
            bpy.context.space_data.overlay.show_overlays = False
        
        if prefs.pb_overlays == 'BONES':
            bpy.context.space_data.overlay.show_bones = False
        
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
                bpy.data.scenes[file_scene].render.ffmpeg.codec = file_video_codec
                bpy.data.scenes[file_scene].render.ffmpeg.gopsize = file_gop
                bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = file_audio
            bpy.data.scenes[file_scene].render.image_settings.color_mode = file_color_mode
            bpy.data.scenes[file_scene].render.image_settings.color_depth = file_color_depth
            bpy.data.scenes[file_scene].render.resolution_x = file_resolution_x
            bpy.data.scenes[file_scene].render.resolution_y = file_resolution_y
            bpy.data.scenes[file_scene].render.resolution_percentage = file_resolution_percentage
            bpy.data.scenes[file_scene].render.use_stamp = file_stamp
            bpy.data.scenes[file_scene].render.stamp_font_size = file_stamp_font_size
            bpy.data.scenes[file_scene].render.film_transparent = file_transparent
            bpy.context.space_data.overlay.show_overlays = file_overlays
            bpy.context.space_data.overlay.show_bones = file_bone_overlays

    def force_divisible(self, number):
        if number % 2 != 0:
            print("Resolution value", number, "is not divisible by 2")
            self.report({'INFO'}, "Resolution value " + str(number) + " is not divisible by 2")
            number += 1
            self.report({'INFO'}, "Playblast addon changed that value to " + str(number))
            print("Playblast addon changed that value to", number)
        else:
            pass

        return number            
        

##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(PL_OT_playblast)
        
def unregister():
    bpy.utils.unregister_class(PL_OT_playblast)