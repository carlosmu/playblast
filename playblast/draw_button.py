import bpy

##############################################
# CONTEXT MENU BUTTON
##############################################

def playblast_ui_context_menu(self, context):
    prefs = context.preferences.addons[__package__].preferences

    layout = self.layout
    if prefs.pb_enable_context_menu:
        layout.separator()
        if prefs.pb_enable_context_menu_playblast:
            layout.operator("playblast.playblast", icon='FILE_MOVIE')
        if prefs.pb_enable_context_menu_replay:
            layout.operator("playblast.player", icon='PLAY')
        if prefs.pb_enable_context_menu_filebrowser:
            layout.operator("playblast.open_filebrowser", icon='FILEBROWSER')


##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.types.VIEW3D_MT_object_context_menu.append(playblast_ui_context_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(playblast_ui_context_menu)