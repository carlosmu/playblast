import bpy

##############################################
## MAIN MENU BUTTON
##############################################
def playblast_ui_main_menu(self, context):

    pb_enable_3dview_menu = context.preferences.addons[__package__].preferences.pb_enable_3dview_menu
    pb_icon_only = context.preferences.addons[__package__].preferences.pb_icon_only

    layout = self.layout 
    if pb_enable_3dview_menu: 
        if pb_icon_only:    
            layout.operator("pl.playblast", icon='FILE_MOVIE', text = '') 
        else:
            layout.operator("pl.playblast", icon='FILE_MOVIE') 


##############################################
## CONTEXT MENU BUTTON
##############################################
def playblast_ui_context_menu(self, context):

    pb_enable_context_menu = context.preferences.addons[__package__].preferences.pb_enable_context_menu

    layout = self.layout 
    if pb_enable_context_menu:     
        layout.operator("pl.playblast", icon='FILE_MOVIE') 


##############################################
## REGISTER/UNREGISTER
##############################################
def register():
    bpy.types.VIEW3D_MT_editor_menus.append(playblast_ui_main_menu) 
    bpy.types.VIEW3D_MT_object_context_menu.append(playblast_ui_context_menu) 
        
def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(playblast_ui_main_menu) 
    bpy.types.VIEW3D_MT_object_context_menu.remove(playblast_ui_context_menu) 