import bpy

##############################################
## DRAW BUTTON
##############################################
def playblast_ui(self, context):
    layout = self.layout     
    layout.operator("pl.playblast", icon='FILE_MOVIE') 

##############################################
## REGISTER/UNREGISTER
##############################################
def register():
    bpy.types.VIEW3D_MT_editor_menus.prepend(playblast_ui) 
        
def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(playblast_ui) 