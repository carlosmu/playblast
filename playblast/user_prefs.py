import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty

##############################################
#    USER PREFERENCES 
##############################################

class PB_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Define properties
    pb_output_options : bpy.props.EnumProperty(
        name = "Output Path Options",
        description = "Select your preferred file output",        
        items = [
            ('PROYECT_FOLDER', 'Project folder', ''),
            ('SYSTEM_FOLDER', 'System folder', ''),
            ('PROYECT_RENDER_SETTINGS', 'Mantain file render settings', '')],
        default = "PROYECT_FOLDER",
    )
    pb_system_folder : bpy.props.StringProperty(
        name = "System folder",
        description = "System output path for playblast files",
        default = "//Playblast/",
        subtype = 'FILE_PATH',
    )
    pb_subfolder : bpy.props.BoolProperty(
        name = "Subfolder",
        description = "User defined subfolder",
        default = True,
    )
    pb_subfolder_name : bpy.props.StringProperty(
        name = "Name",
        description = "Set a subfolder Name",
        default = "Playblast",
    )
    pb_prefix : bpy.props.StringProperty(
        name = "Prefix for video name",
        description = "Set a prefix for video file",
        default = "Playblast-",
    )
    pb_format : bpy.props.EnumProperty(
        name = "Format",
        description = "File format to save the playblast",        
        items = [
            ('AVI_JPEG', 'AVI JPEG', ''),
            ('AVI_RAW', 'AVI JPEG', ''),
            ('FFMPEG', 'FFmpeg Video', '')],
        default = "FFMPEG",
    )
    pb_container : bpy.props.EnumProperty(
        name = "Container",
        description = "Playblast file container",        
        items = [
            ('MPEG1', 'MPEG-1', ''),
            ('MPEG2', 'MPEG-2', ''),
            ('MPEG4', 'MPEG-4', ''),
            ('AVI', 'AVI', ''),
            ('QUICKTIME', 'Quicktime', ''),
            ('DV', 'DV', ''),
            ('OGG', 'Ogg', ''),
            ('MKV', 'Matroska', ''),
            ('FLASH', 'Flash', ''),
            ('WEBM', 'WebM', '')],
        default = "MPEG4",
    )
    pb_audio : bpy.props.EnumProperty(
        name = "Audio",
        description = "Audio codec to use",
        items = [ 
            ('NONE', 'No Audio', ''),
            ('AAC', 'AAC', ''),
            ('AC3', 'AC3', ''),
            ('FLAC', 'FLAC', ''),
            ('MP2', 'MP2', ''),
            ('MP3', 'MP3', ''),
            ('OPUS', 'OPUS', ''),
            ('PCM', 'PCM', ''),
            ('VORBIS', 'VORBIS', '')],
        default = "MP3",
    )
    pb_resolution : bpy.props.IntProperty(
        name = "Resolution %",
        description = "Percentage scale for render resolution",
        default = 50,
        min = 1, soft_min = 1, soft_max = 100, max =200,
    )
    pb_stamp : bpy.props.BoolProperty(
        name = "Stamp Metadata",
        description = "Render the stamp info text in the rendered video",
        default = True,
    )
    pb_autoplay : bpy.props.BoolProperty(
        name = "Autoplay",
        description = "Autoplay the video when processing is finished",
        default = True,
    )
    pb_enable_3dview_menu : bpy.props.BoolProperty(
        name = "Main Menu",
        description = "Enable UI Button for appear on 3d View Main Menu",
        default = True,
    )
    pb_enable_context_menu : bpy.props.BoolProperty(
        name = "Context Menu",
        description = "Enable UI Button on Right Click (or W) Object Context Menu",
        default = True,
    )
    pb_icon_only : bpy.props.BoolProperty(
        name = "Icon Only",
        description = 'Hide the word "Playblast" on Main Menu Button',
        default = False,
    )

    


    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True
        layout.scale_y = 1.2

        pb_subfolder = context.preferences.addons[__package__].preferences.pb_subfolder
        pb_format = context.preferences.addons[__package__].preferences.pb_format
        pb_enable_3dview_menu = context.preferences.addons[__package__].preferences.pb_enable_3dview_menu
        pb_output_options = context.preferences.addons[__package__].preferences.pb_output_options

        # Output options
        layout.prop(self, "pb_output_options")
        
        # If options is system folder, choose path
        if pb_output_options == 'SYSTEM_FOLDER' :
            layout.prop(self, "pb_system_folder")  
        
        row = layout.row()
        row.prop(self, "pb_subfolder")
        # If subfolder is true, set subfolder name
        if pb_subfolder:
             row.prop(self, "pb_subfolder_name")
        
        # Set prefix
        layout.prop(self, "pb_prefix")

        # Set format
        layout.prop(self, "pb_format")
        
        # If format is FFMPEG, set container and audio
        if pb_format == 'FFMPEG':
            layout.prop(self, "pb_container")
            layout.prop(self, "pb_audio")

        # Set resolution
        layout.prop(self, "pb_resolution")

        # Enable Stamp
        layout.prop(self, "pb_stamp")

        # Enable Autoplay
        layout.prop(self, "pb_autoplay")

        # Enable Buttons
        layout.label(text="Enable UI Buttons on:")
        layout.prop(self, "pb_enable_context_menu")
        row = layout.row()
        row.prop(self, "pb_enable_3dview_menu")
        if pb_enable_3dview_menu:
            row.prop(self, "pb_icon_only")
        layout.separator()


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PB_Prefs) 
        
def unregister():
    bpy.utils.unregister_class(PB_Prefs)