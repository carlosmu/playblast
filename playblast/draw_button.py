import bpy

##############################################
# MAIN MENU BUTTON
##############################################


def playblast_ui_main_menu(self, context):

    prefs = context.preferences.addons[__package__].preferences

    layout = self.layout
    layout.separator()
    if prefs.pb_enable_3dview_menu:
        if prefs.pb_icon_only:
            if prefs.pb_enable_3dview_menu_playblast:
                layout.operator("playblast.playblast", icon='FILE_MOVIE', text="")
            if prefs.pb_enable_3dview_menu_replay:
                layout.operator("playblast.player", icon='PLAY', text="")
            layout.operator("playblast.copy_path", icon='FILEBROWSER', text="")
        else:
            if prefs.pb_enable_3dview_menu_playblast:
                layout.operator("playblast.playblast", icon='FILE_MOVIE')
            if prefs.pb_enable_3dview_menu_replay:
                layout.operator("playblast.player", icon='PLAY')
            layout.operator("playblast.copy_path", icon='FILEBROWSER')

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
        layout.operator("playblast.copy_path", icon='FILEBROWSER')
        if prefs.pb_enable_context_menu_turnaround:
            layout.operator_context = "INVOKE_DEFAULT"  # Used for display popup on creation
            layout.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER', text="Add Turnaround Camera")

##############################################
# ADD OBJECT MENU BUTTON
##############################################


def playblast_ui_add_menu(self, context):

    prefs = context.preferences.addons[__package__].preferences

    layout = self.layout
    if prefs.pb_enable_add_menu:
        layout.separator()
        layout.operator_context = "INVOKE_DEFAULT"  # Used for display popup on creation
        layout.operator("playblast.turnaround_camera",
                        icon='CON_CAMERASOLVER', text="Turnaround Camera")


##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.types.VIEW3D_MT_editor_menus.append(playblast_ui_main_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(playblast_ui_context_menu)
    bpy.types.VIEW3D_MT_add.append(playblast_ui_add_menu)


def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(playblast_ui_main_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(playblast_ui_context_menu)
    bpy.types.VIEW3D_MT_add.remove(playblast_ui_add_menu)
