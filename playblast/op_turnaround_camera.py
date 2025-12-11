
import bpy
from bpy_extras import anim_utils


class PL_OT_turnaround_camera(bpy.types.Operator):
    """Create Turnaround Camera (overwrites pre-existing ones)"""
    bl_idname = "playblast.turnaround_camera"
    bl_label = "Add Turnaround Camera"
    bl_options = {'REGISTER', 'UNDO'}

    # Creation Settings
    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Start Frame for Turnaround Camera Animation",
        default=1,
        soft_min=0,
    )
    end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="End Frame for Turnaround Camera Animation",
        default=200,
        soft_min=0,
    )
    camera_distance: bpy.props.IntProperty(
        name="Camera Distance",
        description="Camera Distance to the center of interest (in meters)",
        default=10,
        soft_min=0,
    )
    active_camera: bpy.props.BoolProperty(
        name="Set Active Camera",
        description="Active camera, used for rendering the scene",
        default=True,
    )
    invert_direction: bpy.props.BoolProperty(
        name="Invert Direction",
        description="Invert the direction of turnaround rotation",
        default=False,
    )
    interpolation_type: bpy.props.EnumProperty(
        name="Interpolation Type",
        description="Interpolation Type between keyframes",
        items=[('LINEAR', 'Linear', ''),
               ('BEZIER', 'Bezier', ''),
               ('BACK', 'Back', ''), ],
        default='LINEAR'
    )

    # Prevents operator appearing in unsupported editors
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):
        # Manipulation of variables
        turnaround_rotation = 6.28319  # In radians

        # Invert direction
        if self.invert_direction:
            turnaround_rotation *= -1

        # Set start and end frame of scene
        scene = bpy.context.scene
        scene.frame_start = self.start_frame
        scene.frame_end = self.end_frame

        # Create Turnaround Collection and link to main collection
        if not "Turnaround" in bpy.data.collections:
            collection = bpy.data.collections.new("Turnaround")
            bpy.context.scene.collection.children.link(collection)
        else:
            collection = bpy.data.collections["Turnaround"]

        # Create Camera
        if not "Turnaround_Cam" in bpy.data.cameras:
            cam = bpy.data.cameras.new("Turnaround_Cam")
        else:
            cam = bpy.data.cameras["Turnaround_Cam"]

        if not "Turnaround_Camera" in bpy.data.objects:
            camera = bpy.data.objects.new("Turnaround_Camera", cam)
            camera.rotation_euler = (1.5708, 0.0, 0.0)
            collection.objects.link(camera)
        else:
            camera = bpy.data.objects["Turnaround_Camera"]

        camera.location = (0, self.camera_distance * -1, 0)

        # Create Empty
        if not "Turnaround_Rotation" in bpy.data.objects:
            empty = bpy.data.objects.new("Turnaround_Rotation", None)
            empty.empty_display_size = 2
            empty.empty_display_type = 'PLAIN_AXES'
            collection.objects.link(empty)
        else:
            empty = bpy.data.objects["Turnaround_Rotation"]

        # Parent camera to empty
        camera.parent = empty

        # Set empty as active
        empty.select_set(True)
        bpy.context.view_layer.objects.active = empty

        # Set scene active camera
        if self.active_camera:
            bpy.context.scene.camera = camera

        if not "Turnaround_Action" in bpy.data.actions:
            action = bpy.data.actions.new("Turnaround_Action")
        else:
            action = bpy.data.actions["Turnaround_Action"]

        # Set active action
        if empty.animation_data is None:
            empty.animation_data_create()
        empty.animation_data.action = action

        # Remove existing fcurves
        if bpy.app.version >= (5, 0, 0):
            # Blender 5.0+ compatibility - use channelbag API
            action = empty.animation_data.action
            if action and hasattr(empty.animation_data, 'action_slots'):
                # Find the action slot that contains this action
                action_slot = None
                if empty.animation_data.action_slots:
                    # Try to find the slot with this action
                    for slot in empty.animation_data.action_slots:
                        if slot.action == action:
                            action_slot = slot
                            break
                    # If not found, use active slot or first slot
                    if not action_slot:
                        action_slot = empty.animation_data.action_slots.active
                        if not action_slot and len(empty.animation_data.action_slots) > 0:
                            action_slot = empty.animation_data.action_slots[0]
                
                if action_slot:
                    # Get or ensure channelbag exists
                    channelbag = anim_utils.action_ensure_channelbag_for_slot(action, action_slot)
                    # Remove all existing fcurves
                    for fcurve in list(channelbag.fcurves):
                        channelbag.fcurves.remove(fcurve)
        else:
            # Pre-Blender 5.0
            if action.fcurves:
                fc = action.fcurves
                fc.remove(fc[0])

        # Insert start keyframe (0,0,0)
        empty.rotation_euler[2] = 0
        empty.keyframe_insert(data_path="rotation_euler",
                              index=2, frame=self.start_frame)

        # Insert end keyframe (360 degrees in Z axis)
        empty.rotation_euler[2] = turnaround_rotation
        empty.keyframe_insert(data_path="rotation_euler",
                              index=2, frame=self.end_frame)

        # Select action and set interpolation type
        if bpy.app.version >= (5, 0, 0):
            # Blender 5.0+ compatibility - use channelbag API
            action = empty.animation_data.action
            if action and hasattr(empty.animation_data, 'action_slots'):
                # Find the action slot that contains this action
                action_slot = None
                if empty.animation_data.action_slots:
                    # Try to find the slot with this action
                    for slot in empty.animation_data.action_slots:
                        if slot.action == action:
                            action_slot = slot
                            break
                    # If not found, use active slot or first slot
                    if not action_slot:
                        action_slot = empty.animation_data.action_slots.active
                        if not action_slot and len(empty.animation_data.action_slots) > 0:
                            action_slot = empty.animation_data.action_slots[0]
                
                if action_slot:
                    # Get channelbag for the slot
                    channelbag = anim_utils.action_get_channelbag_for_slot(action, action_slot)
                    if channelbag and len(channelbag.fcurves) > 0:
                        channelbag.fcurves[0].keyframe_points[0].interpolation = self.interpolation_type
        else:
            # Pre-Blender 5.0
            action = empty.animation_data.action
            action.fcurves[0].keyframe_points[0].interpolation = self.interpolation_type

        return{'FINISHED'}

    # Popup
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # Custom Draw
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        box.separator()
        col = box.column(align=True)
        col.prop(self, "start_frame")
        col.prop(self, "end_frame")

        box.prop(self, "camera_distance")
        box.prop(self, "active_camera")
        box.prop(self, "invert_direction")
        box.prop(self, "interpolation_type")
        box.separator()


##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(PL_OT_turnaround_camera)


def unregister():
    bpy.utils.unregister_class(PL_OT_turnaround_camera)
