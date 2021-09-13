import bpy

##############################################
## MAIN MENU BUTTON
##############################################
def playblast_ui_main_menu(self, context):

    prefs = context.preferences.addons[__package__].preferences

    layout = self.layout 
    if prefs.pb_enable_3dview_menu: 
        if prefs.pb_icon_only:    
            layout.operator("pl.playblast", icon='FILE_MOVIE', text = '') 
            layout.operator("pl.turntable_camera", icon='CON_CAMERASOLVER', text = '') 
        else:
            layout.operator("pl.playblast", icon='FILE_MOVIE') 
            layout.operator("pl.turntable_camera", icon='CON_CAMERASOLVER', text = "Turntable") 

##############################################
## CONTEXT MENU BUTTON
##############################################
def playblast_ui_context_menu(self, context):

    prefs = context.preferences.addons[__package__].preferences

    layout = self.layout 
    if prefs.pb_enable_context_menu:
        layout.separator()     
        layout.operator("pl.playblast", icon='FILE_MOVIE') 
        layout.operator("pl.turntable_camera", icon='CON_CAMERASOLVER')


##############################################
## REGISTER/UNREGISTER
##############################################
def register():
    bpy.types.VIEW3D_MT_editor_menus.append(playblast_ui_main_menu) 
    bpy.types.VIEW3D_MT_object_context_menu.append(playblast_ui_context_menu) 
        
def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(playblast_ui_main_menu) 
    bpy.types.VIEW3D_MT_object_context_menu.remove(playblast_ui_context_menu) 