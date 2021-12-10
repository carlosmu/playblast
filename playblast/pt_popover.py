import bpy

###################
## POPOVER CLASS ##
###################


class PL_PT_popover(bpy.types.Panel):
    """Playblast Popover Panel"""
    bl_label = "Playblast Options"
    bl_idname = "PLAYBLAST_PT_popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        col.scale_y = 1.3

        col.operator("playblast.playblast", icon='FILE_MOVIE')

        row = col.row(align=True)
        row.operator("playblast.player", icon='PLAY')
        row.operator("playblast.open_filebrowser",
                     icon='FILEBROWSER', text="Open Folder")

        row = layout.row(align=True)
        row.prop(context.scene, "enable_overrides", icon='FILE_CACHE')
        row.operator("playblast.open_preferences", icon='PREFERENCES')

        if context.scene.enable_overrides:
            col = layout.column()

            # Version Number
            row = col.row(align=True)
            row.prop(context.scene, "enable_version", text="")
            if context.scene.enable_version:
                row.label(text="Version:")

                # Version numbering
                version_number = str(context.scene.version_number)
                version = f'v{version_number:0>3}'
                row.label(text=version)

                # Version buttons
                row.operator("playblast.recover_version",
                             icon='RECOVER_LAST', text="")
                row.operator("playblast.decrease_version",
                             icon='REMOVE', text="")
                row.operator("playblast.increase_version", icon='ADD', text="")
            else:
                row.label(text="Version number")

            # Resolution Overrides
            row = col.row(align=True)
            row.prop(context.scene, "enable_resolution", text="")
            if context.scene.enable_resolution:
                row.prop(context.scene, "override_resize_method", text="")

                if context.scene.override_resize_method == 'PERCENTAGE':
                    row.prop(context.scene,
                             "override_resolution_percentage", text="")
                elif context.scene.override_resize_method == 'MAX_HEIGHT':
                    row.prop(context.scene,
                             "override_resolution_max_height", text="px")
                else:
                    pass
            else:
                row.label(text="Resolution Scale")

            # Overlays overrides
            row = col.row(align=True)
            row.prop(context.scene, "enable_overlays", text="")
            if context.scene.enable_overlays:
                row.prop(context.scene, "hide_overlays", text="")
            else:
                row.label(text="Overlays")

            # Folder overrides
            row = col.row(align=True)
            row.prop(context.scene, "enable_folder", text="")
            if context.scene.enable_folder:
                row.prop(context.scene, "custom_folder", text="")
            else:
                row.label(text="Folder Output")
            layout.separator()

        layout.operator("playblast.turnaround_camera", icon='CON_CAMERASOLVER')


# Main Menu popover
def popover_mainmenu(self, context):
    prefs = context.preferences.addons[__package__].preferences
    if prefs.pb_enable_3dview_menu:
        if bpy.context.area.show_menus:
            self.layout.popover("PLAYBLAST_PT_popover",
                                text="", icon='FILE_MOVIE')
        else:
            self.layout.popover("PLAYBLAST_PT_popover", icon='FILE_MOVIE')



# Context menu popover
def popover_contextmenu(self, context):
    prefs = context.preferences.addons[__package__].preferences
    if prefs.pb_enable_context_menu:
        layout = self.layout
        layout.popover("PLAYBLAST_PT_popover", icon='FILE_MOVIE')
        layout.separator()


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.append(popover_mainmenu)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(popover_contextmenu)

    bpy.types.Scene.enable_overrides = bpy.props.BoolProperty(
        name="Quick Settings",
        description="Enable overrides for preferences",
        default=False,
    )
    bpy.types.Scene.enable_resolution = bpy.props.BoolProperty(
        name="Resolution Scale",
        description="Enable resolution scale override",
        default=False,
    )
    bpy.types.Scene.override_resize_method = bpy.props.EnumProperty(
        name="Resize Method",
        description="Method for resize the current file resolution",
        items=[
            ('PERCENTAGE', 'Percentage',
             'Scale resolution based on Percentage multiplier'),
            ('MAX_HEIGHT', 'Max height',
             'Scale resolution based on Max Height (Y Resolution)'),
            ('NONE', 'Keep project resolution', "Don't scale resolution, mantain project settings")],
        default='PERCENTAGE',
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
        description="Enable overlays override",
        default=False,
    )
    bpy.types.Scene.hide_overlays = bpy.props.EnumProperty(
        name="Overlays",
        description="Hide overlays",
        items=[
            ('ALL', 'Hide all overlays', ''),
            ('BONES', 'Hide only bones', ''),
            ('ALL_EXCEPT_BACKGROUND_IMAGES',
             'Hide all, except camera background images', ''),
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
    bpy.types.Scene.enable_version = bpy.props.BoolProperty(
        name="Enable Version",
        description="Enable custom version",
        default=False,
    )
    bpy.types.Scene.version_number = bpy.props.IntProperty(
        name="Custom Version",
        description="Version for playblast files",
        default=1,
        min=0
    )


def unregister():
    bpy.utils.unregister_class(PL_PT_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover_mainmenu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(popover_contextmenu)

    del bpy.types.Scene.enable_overrides
    del bpy.types.Scene.enable_resolution
    del bpy.types.Scene.override_resize_method
    del bpy.types.Scene.override_resolution_percentage
    del bpy.types.Scene.override_resolution_max_height
    del bpy.types.Scene.enable_overlays
    del bpy.types.Scene.hide_overlays
    del bpy.types.Scene.enable_folder
    del bpy.types.Scene.custom_folder
    del bpy.types.Scene.enable_version
    del bpy.types.Scene.version_number