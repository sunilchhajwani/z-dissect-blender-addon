"""Core dissection operators for Z-Dissect — scalpel, remove, peel."""
import bpy
import bmesh
import json
import time
from bpy.types import Operator
from mathutils import Vector


class DISSECT_OT_scalpel(Operator):
    """Draw a cut line on the selected mesh to split it (Boolean Difference)."""
    bl_idname = "dissect.scalpel"
    bl_label = "Scalpel Cut"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects or len(selected_objects) == 0:
            self.report({'WARNING'}, "No object selected for cutting")
            return {'CANCELLED'}

        obj = selected_objects[0]
        if obj.type != 'MESH':
            self.report({'WARNING'}, "Selected object is not a mesh")
            return {'CANCELLED'}

        # Get BMesh from object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        # Record cut for undo
        state = context.scene.dissect_state
        cut_record = state.cut_history.add()
        cut_record.object_name = obj.name
        cut_record.cut_type = "scalpel"
        cut_record.timestamp = time.time()
        cut_record.description = f"Scalpel cut on {obj.name}"

        # Create a cut plane mesh (simple quad)
        cut_plane_name = f"CutPlane_{int(time.time())}"
        cut_mesh = bpy.data.meshes.new(cut_plane_name)
        cut_obj = bpy.data.objects.new(cut_plane_name, cut_mesh)
        context.collection.objects.link(cut_obj)

        # Build cut plane geometry (perpendicular to view)
        bm_cutter = bmesh.new()
        verts = [
            bm_cutter.verts.new((-1, 0, 0)),
            bm_cutter.verts.new((1, 0, 0)),
            bm_cutter.verts.new((1, 0.1, 0)),
            bm_cutter.verts.new((-1, 0.1, 0))
        ]
        bm_cutter.faces.new(verts)
        bm_cutter.to_mesh(cut_mesh)
        bm_cutter.free()

        # Position cut plane at object location
        cut_obj.location = obj.location
        cut_obj.rotation_euler = obj.rotation_euler

        # Apply Boolean Difference modifier
        bool_mod = obj.modifiers.new(name="DissectCut", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cut_obj

        # Apply modifier
        try:
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        except:
            pass

        # Remove cutter object
        bpy.data.objects.remove(cut_obj, do_unlink=True)

        state.cut_count += 1
        state.is_modified = True

        self.report({'INFO'}, f"Cut applied to {obj.name}")
        return {'FINISHED'}


class DISSECT_OT_remove_layer(Operator):
    """Remove (hide) the currently selected layer to reveal underlying tissue."""
    bl_idname = "dissect.remove_layer"
    bl_label = "Remove Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        state = context.scene.dissect_state

        for obj in selected_objects:
            obj.hide_set(True)

            # Record in state
            layer_record = state.hidden_layers.add()
            layer_record.object_name = obj.name
            layer_record.hidden = True

        state.is_modified = True
        self.report({'INFO'}, f"Hidden {len(selected_objects)} object(s)")
        return {'FINISHED'}


class DISSECT_OT_peel(Operator):
    """Peel away the selected structure with animated transformation."""
    bl_idname = "dissect.peel"
    bl_label = "Peel Layer"
    bl_options = {'REGISTER', 'UNDO'}

    peel_distance: bpy.props.FloatProperty(
        name="Peel Distance",
        default=0.5,
        min=0.0,
        max=10.0
    )
    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        min=1
    )
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        default=30,
        min=1
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        state = context.scene.dissect_state
        active_obj = context.active_object

        initial_location = active_obj.location.copy()

        # Set keyframe at start
        active_obj.location = initial_location
        active_obj.keyframe_insert(data_path="location", frame=self.frame_start)

        # Set keyframe at end (peeled position)
        peel_offset = Vector((0, 0, self.peel_distance))
        active_obj.location = initial_location + peel_offset
        active_obj.keyframe_insert(data_path="location", frame=self.frame_end)

        # Record in cut history
        cut_record = state.cut_history.add()
        cut_record.object_name = active_obj.name
        cut_record.cut_type = "peel"
        cut_record.timestamp = time.time()
        cut_record.description = f"Peel animation on {active_obj.name}"

        state.cut_count += 1
        state.is_modified = True

        self.report({'INFO'}, f"Peel animation added to {active_obj.name}")
        return {'FINISHED'}


class DISSECT_OT_commit_cut(Operator):
    """Finalize the current cut operation and clean up."""
    bl_idname = "dissect.commit_cut"
    bl_label = "Commit Cut"
    bl_options = {'REGISTER'}

    def execute(self, context):
        state = context.scene.dissect_state
        state.is_modified = False
        self.report({'INFO'}, "Cut committed")
        return {'FINISHED'}
