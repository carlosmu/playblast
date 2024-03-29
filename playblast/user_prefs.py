import bpy
import os

##############################################
#    USER PREFERENCES
##############################################
class PB_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Define properties
    pb_output_options: bpy.props.EnumProperty(
        name="Output Path Folder",
        description="Select your preferred folder output",
        items=[
            ('PROYECT_FOLDER', 'Project folder', ''),
            ('SYSTEM_FOLDER', 'System folder', ''),
            ('PROYECT_RENDER_SETTINGS', "Don't overwrite file output", '')],
        default="PROYECT_FOLDER",
    )
    pb_system_folder: bpy.props.StringProperty(
        name="System folder",
        description="System output path for playblast files",
        default="//",
        subtype='FILE_PATH',
    )
    pb_subfolder: bpy.props.BoolProperty(
        name="Subfolder",
        description="User defined subfolder",
        default=True,
    )
    pb_subfolder_name: bpy.props.StringProperty(
        name="Subfolder Custom Name",
        description="Set a subfolder Name",
        default="Playblast",
    )
    pb_playblast_name: bpy.props.EnumProperty(
        name="Playblast Name",
        description="Set a name for generated video file, based on project or custom name",
        items=[
            ('FILENAME', 'Same as filename', ''),
            ('CUSTOM_NAME', 'Custom name', '')],
        default="FILENAME",
    )
    pb_custom_name: bpy.props.StringProperty(
        name="Custom Name",
        description="Set a custom name for video file",
        default="Playblast",
    )
    pb_separator: bpy.props.EnumProperty(
        name="Separator",
        description="Set a custom separator (between name, version, framerange, etc.)",
        items=[
            ('UNDERSCORE', '_ (Underscore)', ''),
            ('DASH', '- (Dash)', ''),
            ('DOT', '. (Dot)', ''),
            ('SPACE', ' (Space)', '')],
        default='DASH',
    )
    pb_framerange: bpy.props.BoolProperty(
        name="Framerange",
        description="Print Framerange in Playblast Name",
        default=False,
    )
    pb_format: bpy.props.EnumProperty(
        name="File Format",
        description="File format to save the playblast",
        items=[
            ('AVI_JPEG', 'AVI JPEG', ''),
            ('AVI_RAW', 'AVI RAW', ''),
            ('FFMPEG', 'FFmpeg Video', '')],
        default="FFMPEG",
    )
    pb_container: bpy.props.EnumProperty(
        name="Container",
        description="Playblast file container",
        items=[
            ('MPEG4', 'MPEG-4', ''),
            ('AVI', 'AVI', ''),
            ('QUICKTIME', 'Quicktime', ''),
            ('MKV', 'Matroska', '')],
        default="MPEG4",
    )
    pb_video_codec: bpy.props.EnumProperty(
        name="Video Codec",
        description="Video codec",
        items=[
            ('H264', 'H264', ''),
            ('QTRLE', 'QT rle / QT Animation', '')],
        default="H264",
    )
    pb_gop: bpy.props.IntProperty(
        name="Keyframe Interval",
        description="Distance between keyframes, also known as GOP size; influences file size and seekability",
        default=18,
    )
    pb_audio: bpy.props.EnumProperty(
        name="Audio Codec",
        description="Audio codec",
        items=[
            ('NONE', 'No Audio', ''),
            ('AAC', 'AAC', ''),
            ('MP3', 'MP3', '')],
        default="NONE",
    )
    pb_resize_method: bpy.props.EnumProperty(
        name="Resize Method",
        description="Method for resize the current file resolution",
        items=[
            ('PERCENTAGE', 'Resolution Percentage', ''),
            ('MAX_HEIGHT', 'Resolution Y (Max height)', ''),
            ('NONE', 'Keep project resolution', '')],
        default='PERCENTAGE',
    )
    pb_resize_percentage: bpy.props.IntProperty(
        name="Resolution Percentage",
        description="H.264 codec requires both the height and width to be divisible by 2",
        default=50,
        min=0, soft_min=10, soft_max=100, max=200,
        subtype='PERCENTAGE',
    )
    pb_resize_max_height: bpy.props.IntProperty(
        name="Resolution Y (Max height) in pixels",
        description="Max value for Resolution-Y in pixels. Resolution-X will be adjusted automatically ",
        min=128, max=2048,
        default=540,
    )
    pb_stamp: bpy.props.BoolProperty(
        name="Stamp Metadata",
        description="Render the stamp info text in the rendered video",
        default=False,
    )
    pb_stamp_font_size: bpy.props.IntProperty(
        name="Stamp Font Size",
        description="Size of the font used when rendering stamp text",
        default=12,
    )
    pb_overlays: bpy.props.EnumProperty(
        name="Overlays",
        description="Hide overlays",
        items=[
            ('ALL', 'Hide all overlays', ''),
            ('BONES', 'Hide only bones', ''),
            ('ALL_EXCEPT_BACKGROUND_IMAGES', 'Hide all, except camera background images', ''),
            ('NONE', "Don't overwrite scene settings", '')],
        default="ALL",
    )
    pb_show_environment: bpy.props.BoolProperty(
        name="Show Environment",
        description="Disable the film transparent render setting",
        default=True,
    )
    pb_autoplay: bpy.props.BoolProperty(
        name="Autoplay",
        description="Autoplay the video when processing is finished",
        default=True,
    )
    # Context Menu options
    pb_enable_context_menu: bpy.props.BoolProperty(
        name="Context Menu Popover",
        description="Enable Popover on Right Click (or W) Object Context Menu",
        default=False,
    )
    # Main Menu Popover
    pb_enable_3dview_menu: bpy.props.BoolProperty(
        name="Main Menu Popover",
        description="Enable Popover for appear on 3d View Main Menu",
        default=True,
    )

    ##############################################
    #    DRAW FUNCTION
    ##############################################

    def draw(self, context):

        layout = self.layout
        layout.use_property_split = True

        prefs = context.preferences.addons[__package__].preferences

        ###### OUTPUT SETTINGS #################################################
        maincol = layout.column(align=True)

        box = maincol.box() # MAIN COLUMN
        box.label(text="OUTPUT", icon="FILE_FOLDER")

        col = box.column(align=True)
        # Folder
        col.prop(self, "pb_output_options", text="Folder")

        # If options is system folder, choose path
        if prefs.pb_output_options == 'SYSTEM_FOLDER':
            col.prop(self, "pb_system_folder")

        # Subfolder
        row = box.row()
        row.prop(self, "pb_subfolder")
        # If subfolder is disable, disable label edition
        if prefs.pb_subfolder:
            row.prop(self, "pb_subfolder_name", text="")
        box.separator()

        # Set playblast name
        col = box.column(align=True)

        row = col.row()
        row.prop(self, "pb_playblast_name")
        if prefs.pb_playblast_name == 'CUSTOM_NAME':
            row.prop(self, "pb_custom_name", text="")

        box.prop(self, "pb_separator", text="Separator")
        box.prop(self, "pb_framerange", text="Stamp framerange in filename")
        box.separator()


        ###### VIDEO SETTINGS #################################################
        box = maincol.box() # MAIN COLUMN
        box.label(text="VIDEO SETTINGS", icon="FILE_MOVIE")
        # Set format
        col = box.column(align=True)
        col.prop(self, "pb_format")
        # If format is FFMPEG, set container and audio
        if prefs.pb_format == 'FFMPEG':
            col.prop(self, "pb_container")
            col.prop(self, "pb_video_codec")
            col.prop(self, "pb_audio")
            box.prop(self, "pb_gop")

        # Set resolution
        row = box.row()
        row.prop(self, "pb_resize_method")
        if prefs.pb_resize_method == 'PERCENTAGE':
            row.prop(self, "pb_resize_percentage", text="")
        elif prefs.pb_resize_method == 'MAX_HEIGHT':
            row.prop(self, "pb_resize_max_height", text="")
        else:
            pass
        
        col = box.column(align=True)
        row = col.row()
        # Enable Stamp
        row.prop(self, "pb_stamp")
        if prefs.pb_stamp:
            row.prop(self, "pb_stamp_font_size", text="Font Size")
        # Show Environment
        col.prop(self, "pb_show_environment")
        box.prop(self, "pb_overlays")
        box.separator()

        
        row = maincol.row(align=True)
        row.use_property_split = False
        ###### UI SETTINGS #################################################
        box = row.box()
        box.label(text="USER INTERFACE", icon='MOD_BUILD')
        col = box.column()
        # Enable on Main Menu
        col.prop(self, "pb_enable_3dview_menu", text="Main Menu Popover")
        # Enable Button on Context
        col.prop(self, "pb_enable_context_menu", text="Context Menu Popover")
        col.separator()

        ###### BEHAVIOR SETTINGS #################################################
        box = row.box()
        box.label(text="BEHAVIOR", icon='AUTO')
        col = box.column()
        # Enable Autoplay
        col.prop(self, "pb_autoplay")
        col.label(text="")
        col.separator()

####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PB_Prefs)

def unregister():
    bpy.utils.unregister_class(PB_Prefs)