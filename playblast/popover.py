import bpy
    
from .user_prefs import PB_Prefs

### Register preferences for use in dropdown items
bpy.utils.register_class(PB_Prefs)
class PL_PT_popover(bpy.types.Panel):
    """Playblast Popover for main menu"""
    bl_label = "Playblast Options"
    bl_idname = "playblast.popover"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences
        

        col = layout.column(align=True)
        col.scale_y = 1.3

        col.operator("playblast.playblast", icon='FILE_MOVIE')
        row = col.row(align=True)
        row.operator("playblast.player", icon='PLAY')
        row = col.row(align=True)
        row.operator("playblast.open_filebrowser", icon='FILEBROWSER', text="Open Folder")
        
        row.operator("playblast.open_preferences", icon='PREFERENCES')   
        
        layout.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER', text="Add Turnaround Camera")
        
        layout.separator()

        layout.prop(context.scene, "enable_overrides")

        if context.scene.enable_overrides:  
            # Resolution overrides    
            box = layout.box()  
            if prefs.pb_resize_method != 'NONE':
                box.prop(context.scene, "enable_resolution") 
                
                if context.scene.enable_resolution:           
                    row = box.row()
                    if prefs.pb_resize_method == 'PERCENTAGE':
                        row.label(text="Percentage")
                        row.scale_x = 2
                        row.prop(context.scene, "override_resolution_percentage", text="")
                    else:
                        row.label(text="Max Height")
                        row.scale_x = 2
                        row.prop(context.scene, "override_resolution_max_height", text="")
            else:
                box.label(text="Resize Method are disabled", icon='INFO')
            
            # Overlays overrides
            box = layout.box()
            row = box.row()
            row.prop(context.scene, "enable_overlays") 
            if context.scene.enable_overlays:
                row.scale_x = 1.5
                row.prop(context.scene, "hide_overlays", text="") 

        

def popover(self, context):
    prefs = context.preferences.addons[__package__].preferences
    if prefs.pb_enable_3dview_menu:
        if bpy.context.area.show_menus:
            self.layout.popover("playblast.popover", text="", icon='FILE_MOVIE')
        else:
            self.layout.popover("playblast.popover", icon='FILE_MOVIE')

bpy.utils.unregister_class(PB_Prefs)

####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(popover)

    bpy.types.Scene.enable_overrides = bpy.props.BoolProperty(
        name="Override Prefereces",
        description="Enable overrides for preferences",
        default=False,
    )
    bpy.types.Scene.enable_resolution = bpy.props.BoolProperty(
        name="Resize Scale",
        description="Enable resolution scale override",
        default=False,
    )
    bpy.types.Scene.override_resolution_percentage = bpy.props.IntProperty(
        name="Resolution Percentage",
        description="H.264 codec requires both the height and width to be divisible by 2",
        default=50,
        min=0, soft_min=10, soft_max=100, max=200,
        subtype='PERCENTAGE',
    )
    bpy.types.Scene.override_resolution_max_height = bpy.props.IntProperty(
        name="Resolution Y (Max height) in pixels",
        description="Max value for Resolution-Y in pixels. Resolution-X will be adjusted automatically ",
        min=128, max=2048,
        default=540,
    )
    bpy.types.Scene.enable_overlays = bpy.props.BoolProperty(
        name="Overlays",
        description="Enable resolution scale override",
        default=False,
    )
    bpy.types.Scene.hide_overlays = bpy.props.EnumProperty(
        name="Overlays",
        description="Hide overlays",
        items=[
            ('ALL', 'Hide all overlays', ''),
            ('BONES', 'Hide only bones', ''),
            ('ALL_EXCEPT_BACKGROUND_IMAGES', 'Hide all, except camera background images', ''),
            ('NONE', "Don't overwrite scene settings", '')],
        default="ALL",
    )

def unregister():
    bpy.utils.unregister_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover)

    del bpy.types.Scene.enable_overrides
    del bpy.types.Scene.enable_resolution
    del bpy.types.Scene.override_resolution_percentage
    del bpy.types.Scene.override_resolution_max_height
    del bpy.types.Scene.enable_overlays
    del bpy.types.Scene.hide_overlays