import bpy
import os

# All pb_ variables come from user prefs, don't overwrite them

##############################################
#   MAIN OPERATOR
##############################################

def warning(self, context):
    self.layout.label(text="Please save your blend file first")

def codecs_error(self, context):
    self.layout.label(
        text="Set resolution divisible by 2, or choose another container/codec combination")

def videoplayer_error(self, context):
    self.layout.label(text="Check your aplication videoplayer preferences")

class PL_OT_playblast(bpy.types.Operator):
    """Quick viewport render of the animation framerange using the addon settings"""
    bl_idname = "playblast.playblast"
    bl_label = "Playblast"
    bl_options = {'REGISTER', 'UNDO'}

    # Prevents operator appearing in unsupported editors
    @classmethod
    def poll(cls, context):
        if context.area != None:
            if context.area.ui_type == 'VIEW_3D':
                return True

    ##############################################
    #   Playblast functionality
    ##############################################
    def execute(self, context):

        # If file is not saved, show warning message
        if bpy.data.is_saved:
            self.playblast(context)
        else:
            context.window_manager.popup_menu(
                warning, title="File not saved", icon='ERROR')
        return{'FINISHED'}

    def playblast(self, context):

        prefs = context.preferences.addons[__package__].preferences

        #################################
        # Save current file render settings
        #################################
        file_extension = bpy.context.scene.render.use_file_extension

        file_scene = bpy.context.scene.name_full  # Scene Name
        # Output path
        file_output = bpy.data.scenes[file_scene].render.filepath
        # Output file format
        file_format = bpy.data.scenes[file_scene].render.image_settings.file_format
        if file_format == 'FFMPEG':  # Only save container and audio in FFMPEG format
            # Video Container
            file_container = bpy.data.scenes[file_scene].render.ffmpeg.format
            # Video Codec
            file_video_codec = bpy.data.scenes[file_scene].render.ffmpeg.codec
            file_gop = bpy.data.scenes[file_scene].render.ffmpeg.gopsize  # GOP
            # Audio codec
            file_audio = bpy.data.scenes[file_scene].render.ffmpeg.audio_codec
        # Color Mode
        file_color_mode = bpy.data.scenes[file_scene].render.image_settings.color_mode
        # Color Depth
        file_color_depth = bpy.data.scenes[file_scene].render.image_settings.color_depth
        # Media Type (Blender 5.0+)
        file_media_type = None
        if bpy.app.version >= (5, 0, 0):
            file_media_type = bpy.data.scenes[file_scene].render.image_settings.media_type
        # X Resolution
        file_resolution_x = bpy.data.scenes[file_scene].render.resolution_x
        # Y Resolution
        file_resolution_y = bpy.data.scenes[file_scene].render.resolution_y
        # Resolution Percentage
        file_resolution_percentage = bpy.data.scenes[file_scene].render.resolution_percentage
        file_stamp = bpy.data.scenes[file_scene].render.use_stamp  # Use Stamp
        # Stamp font size
        file_stamp_font_size = bpy.data.scenes[file_scene].render.stamp_font_size
        # Film Transparent
        file_transparent = bpy.data.scenes[file_scene].render.film_transparent
        # Overlays
        file_overlays = bpy.context.space_data.overlay.show_overlays
        file_bone_overlays = bpy.context.space_data.overlay.show_bones
        file_extras_olverlays = bpy.context.space_data.overlay.show_extras
        file_floor_overlays = bpy.context.space_data.overlay.show_floor
        file_axis_x_overlays = bpy.context.space_data.overlay.show_axis_x
        file_axis_y_overlay = bpy.context.space_data.overlay.show_axis_y
        file_axis_z_olverlay = bpy.context.space_data.overlay.show_axis_z
        file_text_overlay = bpy.context.space_data.overlay.show_text
        if bpy.app.version >= (2, 90, 0):
            file_stats_overlay = bpy.context.space_data.overlay.show_stats
        file_cursor_overlay = bpy.context.space_data.overlay.show_cursor
        file_annotation_overlay = bpy.context.space_data.overlay.show_annotation
        file_relationship_lines_overlay = bpy.context.space_data.overlay.show_relationship_lines
        file_outline_selected_overlay = bpy.context.space_data.overlay.show_outline_selected
        file_motion_paths_overlay = bpy.context.space_data.overlay.show_motion_paths
        file_object_origins_overlay = bpy.context.space_data.overlay.show_object_origins
        file_wireframes_overlay = bpy.context.space_data.overlay.show_wireframes
        file_face_orientation_overlay = bpy.context.space_data.overlay.show_face_orientation
        file_reconstruction_overlay = bpy.context.space_data.show_reconstruction

        # Get filename
        file_name = ""
        file_name = bpy.path.basename(bpy.data.filepath)
        file_name = os.path.splitext(file_name)[0]

        # Define Separator
        if prefs.pb_separator == 'UNDERSCORE':
            separator = "_"
        elif prefs.pb_separator == 'DASH':
            separator = "-"
        elif prefs.pb_separator == 'DOT':
            separator = "."
        else:
            separator = " "
        
        # Define Playblast Name
        playblast_name = ""
        if prefs.pb_playblast_name == 'FILENAME':
            playblast_name = file_name
        elif prefs.pb_playblast_name == 'CUSTOM_NAME':
            playblast_name = prefs.pb_custom_name
        else:
            pass

        # Framerange
        framerange = f'{separator}{context.scene.frame_start:0>4}{separator}{context.scene.frame_end:0>4}'

        if prefs.pb_framerange:
            name = playblast_name + framerange
        else:
            name = playblast_name

        # Custom Version
        version_number = str(context.scene.version_number)
        version = f'{separator}v{version_number:0>3}'
        
        # Apply version
        if context.scene.enable_version and context.scene.enable_overrides:
            name = name + version

        # Extension
        bpy.context.scene.render.use_file_extension = False

        if prefs.pb_container == 'MPEG4':
            extension = ".mp4"
        elif prefs.pb_container == 'AVI':
            extension = ".avi"
        elif prefs.pb_container == 'QUICKTIME':
            extension = ".mov"
        else:
            extension = ".mkv"
            
        name = name + extension        
        

        # Define Output Path
        output = ""
        subfolder = ""
        subfolder = prefs.pb_subfolder_name + "/"

        # Override Folder
        if context.scene.enable_folder and context.scene.enable_overrides:
            output = context.scene.custom_folder
        else:
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

        # Add name to output
        output = output + name

        # Override Resolution Scale Method
        if context.scene.enable_resolution and context.scene.enable_overrides:
            if context.scene.override_resize_method == 'PERCENTAGE':
                divisor = 100 / context.scene.override_resolution_percentage
            elif context.scene.override_resize_method == 'MAX_HEIGHT':
                divisor = file_resolution_y / context.scene.override_resolution_max_height
            else:
                divisor = 1
        else:
            if prefs.pb_resize_method == 'PERCENTAGE':
                divisor = 100 / prefs.pb_resize_percentage
            elif prefs.pb_resize_method == 'MAX_HEIGHT':
                divisor = file_resolution_y / prefs.pb_resize_max_height
            else:
                divisor = 1

        # Asign new resolution
        resolution_x = int(file_resolution_x // divisor)
        resolution_y = int(file_resolution_y // divisor)
        resolution_x = self.force_divisible(resolution_x)
        resolution_y = self.force_divisible(resolution_y)
        
        #################################
        # Overwrite file settings
        #################################
        bpy.data.scenes[file_scene].render.filepath = output

        if bpy.app.version >= (5, 0, 0):
            # Blender 5.0+ - Set media type to VIDEO first
            bpy.context.scene.render.image_settings.media_type = 'VIDEO'
            # Blender 5.0+ - Always set format and codec
            bpy.context.scene.render.ffmpeg.format = prefs.pb_container
            bpy.context.scene.render.ffmpeg.codec = prefs.pb_video_codec
            # Blender 5.0+ uses PNG for video rendering through compositor
            # bpy.data.scenes[file_scene].render.image_settings.file_format = 'PNG'
            # Video rendering settings for Blender 5.0+
            # if hasattr(bpy.data.scenes[file_scene].render, 'use_multiview'):
            #     bpy.data.scenes[file_scene].render.ffmpeg.gopsize = prefs.pb_gop
            #     bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = prefs.pb_audio
        else:
            # Pre-Blender 5.0
            bpy.data.scenes[file_scene].render.image_settings.file_format = prefs.pb_format
            if prefs.pb_format == 'FFMPEG':
                bpy.data.scenes[file_scene].render.ffmpeg.format = prefs.pb_container
                bpy.data.scenes[file_scene].render.ffmpeg.codec = prefs.pb_video_codec
                bpy.data.scenes[file_scene].render.ffmpeg.gopsize = prefs.pb_gop
                bpy.data.scenes[file_scene].render.ffmpeg.audio_codec = prefs.pb_audio

        # if prefs.pb_resize_method == 'PERCENTAGE' or prefs.pb_resize_method == 'MAX_HEIGHT':
        bpy.data.scenes[file_scene].render.resolution_x = resolution_x
        bpy.data.scenes[file_scene].render.resolution_y = resolution_y
        # Prevents unwanted resizing
        bpy.data.scenes[file_scene].render.resolution_percentage = 100

        bpy.data.scenes[file_scene].render.use_stamp = prefs.pb_stamp
        if prefs.pb_stamp:
            bpy.data.scenes[file_scene].render.stamp_font_size = prefs.pb_stamp_font_size

        if prefs.pb_show_environment:
            bpy.data.scenes[file_scene].render.film_transparent = False

        # Override Overlays
        if context.scene.enable_overlays and context.scene.enable_overrides:
            overlays = context.scene.hide_overlays
        else:
            overlays = prefs.pb_overlays

        # Overlays settings
        if overlays == 'ALL':
            bpy.context.space_data.overlay.show_overlays = False

        if overlays == 'BONES':
            bpy.context.space_data.overlay.show_bones = False

        if overlays == 'ALL_EXCEPT_BACKGROUND_IMAGES':         
            bpy.context.space_data.overlay.show_floor = False
            bpy.context.space_data.overlay.show_axis_x = False
            bpy.context.space_data.overlay.show_axis_y = False
            bpy.context.space_data.overlay.show_axis_z = False
            bpy.context.space_data.overlay.show_text = False
            if bpy.app.version >= (2, 90, 0):
                bpy.context.space_data.overlay.show_stats = False
            bpy.context.space_data.overlay.show_cursor = False
            bpy.context.space_data.overlay.show_annotation = False
            bpy.context.space_data.overlay.show_bones = False
            bpy.context.space_data.overlay.show_relationship_lines = False
            bpy.context.space_data.overlay.show_outline_selected = False
            bpy.context.space_data.overlay.show_extras = False
            bpy.context.space_data.overlay.show_motion_paths = False
            bpy.context.space_data.overlay.show_object_origins = False 
            bpy.context.space_data.overlay.show_wireframes = False
            bpy.context.space_data.overlay.show_face_orientation = False
            bpy.context.space_data.show_reconstruction = False     

        # Try to create the video, but mainly protect the user's data
        try:
            if bpy.app.version >= (5, 0, 0):
                bpy.ops.render.render(animation=True)
            else:
                bpy.ops.render.opengl(animation=True)
            if prefs.pb_autoplay:
                try:
                    bpy.ops.render.play_rendered_anim()
                except:
                    context.window_manager.popup_menu(
                        videoplayer_error, title="Video player error", icon='ERROR')
        except:
            context.window_manager.popup_menu(
                codecs_error, title="Codecs error", icon='ERROR')
        finally:
            #################################
            # Recover previous file settings
            #################################
            bpy.context.scene.render.use_file_extension = file_extension
            bpy.data.scenes[file_scene].render.filepath = file_output
            bpy.data.scenes[file_scene].render.image_settings.file_format = file_format
            # Restore media type (Blender 5.0+)
            if bpy.app.version >= (5, 0, 0):
                bpy.data.scenes[file_scene].render.image_settings.media_type = file_media_type
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
            # Overlays
            bpy.context.space_data.overlay.show_overlays = file_overlays
            bpy.context.space_data.overlay.show_bones = file_bone_overlays
            bpy.context.space_data.overlay.show_extras = file_extras_olverlays
            bpy.context.space_data.overlay.show_floor = file_floor_overlays
            bpy.context.space_data.overlay.show_axis_x = file_axis_x_overlays
            bpy.context.space_data.overlay.show_axis_y = file_axis_y_overlay
            bpy.context.space_data.overlay.show_axis_z = file_axis_z_olverlay
            bpy.context.space_data.overlay.show_text = file_text_overlay
            if bpy.app.version >= (2, 90, 0):
                bpy.context.space_data.overlay.show_stats = file_stats_overlay
            bpy.context.space_data.overlay.show_cursor = file_cursor_overlay
            bpy.context.space_data.overlay.show_annotation = file_annotation_overlay
            bpy.context.space_data.overlay.show_relationship_lines = file_relationship_lines_overlay
            bpy.context.space_data.overlay.show_outline_selected = file_outline_selected_overlay
            bpy.context.space_data.overlay.show_motion_paths = file_motion_paths_overlay
            bpy.context.space_data.overlay.show_object_origins = file_object_origins_overlay
            bpy.context.space_data.overlay.show_wireframes = file_wireframes_overlay
            bpy.context.space_data.overlay.show_face_orientation = file_face_orientation_overlay
            bpy.context.space_data.show_reconstruction = file_reconstruction_overlay

    def force_divisible(self, number):
        if number % 2 != 0:
            print("Resolution value", number, "is not divisible by 2")
            self.report({'INFO'}, "Resolution value " +
                        str(number) + " is not divisible by 2")
            number += 1
            self.report(
                {'INFO'}, "Playblast addon changed that value to " + str(number))
            print("Playblast addon changed that value to", number)
        else:
            pass

        return number


##############################################
# Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(PL_OT_playblast)

def unregister():
    bpy.utils.unregister_class(PL_OT_playblast)