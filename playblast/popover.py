import bpy

###################
## POPOVER CLASS ##
###################
class PL_PT_popover(bpy.types.Panel):
    """Playblast Popover Panel"""
    bl_label = "Playblast Options"
    bl_idname = "playblast.popover"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences # Import preferences        

        col = layout.column(align=True)
        col.scale_y = 1.3

        col.operator("playblast.playblast", icon='FILE_MOVIE')

        row = col.row(align=True)
        row.operator("playblast.player", icon='PLAY')
        row.operator("playblast.open_filebrowser", icon='FILEBROWSER', text="Open Folder")

        row = layout.row(align=True)
        row.operator("playblast.open_preferences", icon='PREFERENCES')   
        row.prop(context.scene, "enable_overrides", icon='DECORATE_OVERRIDE')

        if context.scene.enable_overrides: 
            # Resolution overrides    
            box = layout.box()  
            if prefs.pb_resize_method != 'NONE':
                row = box.row(align=True)
                row.prop(context.scene, "enable_resolution", text="") 
                
                if context.scene.enable_resolution:           
                    if prefs.pb_resize_method == 'PERCENTAGE':
                        row.prop(context.scene, "override_resolution_percentage")
                    else:
                        row.prop(context.scene, "override_resolution_max_height", text="Max px Height")
                else:
                    row.label(text="Resize Scale")
            else:
                box.label(text="Resize disabled on preferences", icon='INFO')
            
            # Overlays overrides
            row = box.row(align=True)
            row.prop(context.scene, "enable_overlays", text="") 
            if context.scene.enable_overlays:
                row.prop(context.scene, "hide_overlays", text="") 
            else:
                row.label(text="Overlays")

            # Folder overrides
            row = box.row(align=True)
            row.prop(context.scene, "enable_folder", text="") 
            if context.scene.enable_folder:
                row.prop(context.scene, "custom_folder", text="") 
            else:
                row.label(text="Folder Output")
            layout.separator()

        layout.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER', text="Add Turnaround Camera")

        

def popover(self, context):
    prefs = context.preferences.addons[__package__].preferences
    if prefs.pb_enable_3dview_menu:
        if bpy.context.area.show_menus:
            self.layout.popover("playblast.popover", text="", icon='FILE_MOVIE')
        else:
            self.layout.popover("playblast.popover", icon='FILE_MOVIE')


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(popover)

    bpy.types.Scene.enable_overrides = bpy.props.BoolProperty(
        name="Override Prefs",
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
    bpy.types.Scene.enable_folder = bpy.props.BoolProperty(
        name="Folder Output",
        description="Enable custom folder output override",
        default=False,
    )
    bpy.types.Scene.custom_folder = bpy.props.StringProperty(
        name="Custom folder",
        description="Folder output path for playblast files",
        default="//",
        subtype='FILE_PATH',
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
    del bpy.types.Scene.enable_folder
    del bpy.types.Scene.custom_folder