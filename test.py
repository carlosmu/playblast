import bpy

# Save file settings
file_output = bpy.data.scenes["Scene"].render.filepath
file_format = bpy.context.scene.render.image_settings.file_format
file_encoding_container = bpy.context.scene.render.ffmpeg.format



# Overwrite file settings
bpy.data.scenes["Scene"].render.filepath = '//'
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'


bpy.ops.render.opengl(animation=True)
bpy.ops.render.play_rendered_anim()

# Recover previous file settings
bpy.data.scenes["Scene"].render.filepath = file_output
bpy.context.scene.render.image_settings.file_format = file_format
bpy.context.scene.render.ffmpeg.format = file_encoding_container
