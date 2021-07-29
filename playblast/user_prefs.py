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
        description = "Render the stamp info text in the rendered image",
        default = True,
    )
    pb_autoplay : bpy.props.BoolProperty(
        name = "Autoplay",
        description = "Autoplay the Playblast video",
        default = True,
    )


    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "pb_format")
        layout.prop(self, "pb_container")
        layout.prop(self, "pb_audio")
        layout.prop(self, "pb_resolution")
        layout.prop(self, "pb_stamp")
        layout.prop(self, "pb_autoplay")
        layout.separator()




####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PB_Prefs) 
        
def unregister():
    bpy.utils.unregister_class(PB_Prefs)