import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty

##############################################
#    USER PREFERENCES 
##############################################

class PB_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

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

        pb_format = context.preferences.addons[__package__].preferences.pb_format
        pb_enable_3dview_menu = context.preferences.addons[__package__].preferences.pb_enable_3dview_menu

        layout.prop(self, "pb_format")
        if pb_format == 'FFMPEG':
            layout.prop(self, "pb_container")
            layout.prop(self, "pb_audio")
        layout.prop(self, "pb_resolution")
        layout.prop(self, "pb_stamp")
        layout.prop(self, "pb_autoplay")
        
        layout.label(text = "Enable UI Buttons:")
        row = layout.row()
        row.prop(self, "pb_enable_3dview_menu")
        if pb_enable_3dview_menu:
            row.prop(self, "pb_icon_only")
        layout.prop(self, "pb_enable_context_menu")
        layout.separator()




####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PB_Prefs) 
        
def unregister():
    bpy.utils.unregister_class(PB_Prefs)