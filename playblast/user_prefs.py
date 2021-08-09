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
        name = "Output Path Folder",
        description = "Select your preferred folder output",        
        items = [
            ('PROYECT_FOLDER', 'Project folder', ''),
            ('SYSTEM_FOLDER', 'System folder', ''),
            ('PROYECT_RENDER_SETTINGS', "Don't overwrite file output", '')],
        default = "PROYECT_FOLDER",
    )
    pb_system_folder : bpy.props.StringProperty(
        name = "System folder",
        description = "System output path for playblast files",
        default = "//",
        subtype = 'FILE_PATH',
    )
    pb_subfolder : bpy.props.BoolProperty(
        name = "Subfolder",
        description = "User defined subfolder",
        default = True,
    )
    pb_subfolder_name : bpy.props.StringProperty(
        name = "Subfolder Custom Name",
        description = "Set a subfolder Name",
        default = "Playblast",
    )
    pb_prefix_options : bpy.props.EnumProperty(
        name = "Prefix Options",
        description = "Set a prefix for video name",        
        items = [
            ('FILE_NAME', 'File name', ''),
            ('CUSTOM_PREFIX', 'Custom prefix', ''),
            ('NONE', 'No prefix needed', '')],
        default = "FILE_NAME",
    )
    pb_custom_prefix : bpy.props.StringProperty(
        name = "Custom prefix",
        description = "Set a custom prefix for video file",
        default = "Playblast",
    )
    pb_separator : bpy.props.StringProperty(
        name = "Prefix Separator",
        description = "Set a custom prefix separator (use only system supported characters, for example underscore, middle dash, or dot)",
        default = "-",
    )
    pb_format : bpy.props.EnumProperty(
        name = "File Format",
        description = "File format to save the playblast",        
        items = [
            ('AVI_JPEG', 'AVI JPEG', ''),
            ('AVI_RAW', 'AVI RAW', ''),
            ('FFMPEG', 'FFmpeg Video', '')],
        default = "FFMPEG",
    )
    pb_container : bpy.props.EnumProperty(
        name = "Container",
        description = "Playblast file container",        
        items = [
            ('MPEG4', 'MPEG-4', ''),
            ('AVI', 'AVI', ''),
            ('QUICKTIME', 'Quicktime', ''),
            ('MKV', 'Matroska', '')],
        default = "MPEG4",
    )
    pb_video_codec : bpy.props.EnumProperty(
        name = "Video Codec",
        description = "Video codec",        
        items = [
            ('H264', 'H264', ''),
            ('QTRLE', 'QT rle / QT Animation', '')],
        default = "H264",
    )
    pb_gop : bpy.props.IntProperty(
        name = "Keyframe Interval",
        description = "Distance between keyframes, also known as GOP size; influences file size and seekability",
        default = 18,
    )
    pb_audio : bpy.props.EnumProperty(
        name = "Audio Codec",
        description = "Audio codec",
        items = [ 
            ('NONE', 'No Audio', ''),
            ('AAC', 'AAC', ''),
            ('MP3', 'MP3', '')],
        default = "NONE",
    )
    pb_resize_method : bpy.props.EnumProperty(
        name = "Resize Method",
        description = "Method for resize the current file resolution",
        items = [
            ('PERCENTAGE', 'Resolution Percentage', ''),
            ('MAX_HEIGHT', 'Resolution Y (Max height)', ''),
            ('NONE', 'Keep file resolution', '')],
            default = 'PERCENTAGE',
    )
    pb_resize_percentage : bpy.props.IntProperty(
        name = "Resolution Percentage",
        description = "H.264 codec requires both the height and width to be divisible by 2",
        default = 50,
        min = 0, soft_min = 10, soft_max = 100, max =200,
        subtype='PERCENTAGE',
    )
    pb_resize_max_height : bpy.props.IntProperty(
        name = "Resolution Y (Max height) in pixels",
        description = "Max value for Resolution-Y in pixels. Resolution-X will be adjusted automatically ",
        min = 128, max = 2048,
        default = 540,
    )
    pb_stamp : bpy.props.BoolProperty(
        name = "Stamp Metadata",
        description = "Render the stamp info text in the rendered video",
        default = False,
    )   
    pb_stamp_font_size : bpy.props.IntProperty(
        name = "Stamp Font Size",
        description="Size of the font used when rendering stamp text",
        default = 12,
    )
    pb_overlays : bpy.props.EnumProperty(
        name = "Overlays",
        description = "Hide overlays",
        items = [ 
            ('ALL', 'Hide all overlays', ''),
            ('BONES', 'Hide only bones', ''),
            ('NONE', "Don't overwrite scene settings", '')],
        default = "ALL",
    )
    pb_show_environment : bpy.props.BoolProperty(
        name = "Show Environment",
        description = "Disable the film transparent render setting",
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
        default = True,
    )    
    
    ##############################################
    #    DRAW FUNCTION
    ##############################################
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        prefs = context.preferences.addons[__package__].preferences

        box = layout.box()

        box.label(text="Output", icon = "FILE_FOLDER")

        # Folder
        box.prop(self, "pb_output_options", text = "Folder")       

        # If options is system folder, choose path
        if prefs.pb_output_options == 'SYSTEM_FOLDER' :
            box.prop(self, "pb_system_folder")             
        
        # Subfolder
        row = box.row()
        row.prop(self, "pb_subfolder")        
        # If subfolder is disable, disable label edition
        if prefs.pb_subfolder:
            row.prop(self, "pb_subfolder_name", text = "")
        box.separator() 

        # Set prefix
        row = box.row()
        row.prop(self, "pb_prefix_options", text = "Name Prefix")
        if prefs.pb_prefix_options == 'CUSTOM_PREFIX':
            row.prop(self, "pb_custom_prefix", text = "")

        if prefs.pb_prefix_options != 'NONE':
            row = box.row()
            row.prop(self, "pb_separator", text = "Separator")
            row.label(text="")
        box.separator()
        
        box.label(text="Video Settings", icon = "FILE_MOVIE")
        # Set format
        box.prop(self, "pb_format")        
        # If format is FFMPEG, set container and audio
        if prefs.pb_format == 'FFMPEG':
            box.prop(self, "pb_container")
            box.prop(self, "pb_video_codec")
            box.prop(self, "pb_gop")
            box.prop(self, "pb_audio")
        box.separator()

        # Set resolution
        row = box.row()
        row.prop(self, "pb_resize_method")
        if prefs.pb_resize_method == 'PERCENTAGE':
            row.prop(self, "pb_resize_percentage", text="")
            box.separator()
        elif prefs.pb_resize_method == 'MAX_HEIGHT':
            row.prop(self, "pb_resize_max_height", text="")
            box.separator()
        else:
            pass    

        row = box.row()
        # Enable Stamp
        row.prop(self, "pb_stamp")
        if prefs.pb_stamp:
            row.prop(self, "pb_stamp_font_size", text="Font Size")
        # Show Environment
        box.prop(self, "pb_show_environment")
        row = box.row()
        row.prop(self, "pb_overlays")
        box.separator()

        box.label(text="Show UI Buttons", icon = 'SHADERFX')
        # Enable Button on Context
        box.prop(self, "pb_enable_context_menu")
        row = box.row()
        # Enable Button on 3dview Menu
        row.prop(self, "pb_enable_3dview_menu")
        if prefs.pb_enable_3dview_menu:
            row.prop(self, "pb_icon_only")
        box.separator()

        box.label(text="Behavior", icon = 'AUTO')
        # Enable Autoplay
        box.prop(self, "pb_autoplay")        
        box.separator()


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PB_Prefs) 
        
def unregister():
    bpy.utils.unregister_class(PB_Prefs)