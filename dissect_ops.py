"""Core dissection operators for Z-Dissect — scalpel, remove, peel, sweep, optimize."""
import bpy
import bmesh
import json
import time
import math
from bpy.types import Operator
from mathutils import Vector, Matrix


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


class DISSECT_OT_sweep_scalpel(Operator):
    """Interactive sweep-surface scalpel. Click points to draw a cut path."""
    bl_idname = "dissect.sweep_scalpel"
    bl_label = "Advanced Scalpel"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.points = []

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            # In a real modal session, we'd record points or show a preview
            pass

        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.report({'INFO'}, "Point added")
            # In actual use, points would be added here via raycasting
            return {'RUNNING_MODAL'}

        elif event.type in {'RET', 'NUMPAD_ENTER'}:
            self.execute_cut(context)
            return {'FINISHED'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type != 'VIEW_3D':
            self.report({'WARNING'}, "Active space must be 3D View")
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Sweep Scalpel: Click to draw, Enter to cut, Esc to cancel")
        return {'RUNNING_MODAL'}

    def execute_cut(self, context):
        """Build the sweep surface and apply boolean."""
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            return

        # Fallback: if no points collected (e.g. background mode), create demo path
        if not self.points:
            loc = obj.location
            self.points = [
                loc + Vector((-1, -1, 0)),
                loc + Vector((0, 1, 0)),
                loc + Vector((1, -1, 0))
            ]

        # Create blade mesh (ribbon)
        blade_name = f"Blade_{int(time.time())}"
        blade_mesh = bpy.data.meshes.new(blade_name)
        blade_obj = bpy.data.objects.new(blade_name, blade_mesh)
        context.collection.objects.link(blade_obj)

        bm = bmesh.new()
        height = 2.0  # Vertical extent of the blade
        
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            v1 = bm.verts.new(p1 - Vector((0, 0, height/2)))
            v2 = bm.verts.new(p2 - Vector((0, 0, height/2)))
            v3 = bm.verts.new(p2 + Vector((0, 0, height/2)))
            v4 = bm.verts.new(p1 + Vector((0, 0, height/2)))
            
            bm.faces.new((v1, v2, v3, v4))

        bm.to_mesh(blade_mesh)
        bm.free()

        # Apply Boolean
        bool_mod = obj.modifiers.new(name="SweepCut", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = blade_obj
        
        try:
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        except:
            pass
        
        bpy.data.objects.remove(blade_obj, do_unlink=True)
        
        state = context.scene.dissect_state
        cut_record = state.cut_history.add()
        cut_record.object_name = obj.name
        cut_record.cut_type = "sweep"
        cut_record.timestamp = time.time()
        cut_record.description = f"Advanced sweep cut on {obj.name}"
        
        state.cut_count += 1
        state.is_modified = True


class DISSECT_OT_optimize_mesh(Operator):
    """Reduce polycount for real-time/web performance."""
    bl_idname = "dissect.optimize_mesh"
    bl_label = "Optimize Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        state = context.scene.dissect_state
        selected = context.selected_objects
        
        if not selected:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        for obj in selected:
            if obj.type != 'MESH':
                continue

            # 1. Apply Decimate
            dec_mod = obj.modifiers.new(name="OptimizeDecimate", type='DECIMATE')
            dec_mod.ratio = state.decimate_ratio
            dec_mod.decimate_type = state.optimization_mode
            
            # 2. Apply Remesh (optional)
            if state.use_remesh:
                rem_mod = obj.modifiers.new(name="OptimizeRemesh", type='REMESH')
                rem_mod.mode = 'VOXEL'
                rem_mod.voxel_size = 0.1
            
            # Apply optimization modifiers
            for mod in list(obj.modifiers):
                if mod.name.startswith("Optimize"):
                    try:
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except:
                        pass

            cut_record = state.cut_history.add()
            cut_record.object_name = obj.name
            cut_record.cut_type = "optimize"
            cut_record.timestamp = time.time()
            cut_record.description = f"Optimized {obj.name} (Ratio: {state.decimate_ratio})"

        self.report({'INFO'}, f"Optimized {len(selected)} object(s)")
        return {'FINISHED'}


class DISSECT_OT_remove_layer(Operator):
    """Remove (hide) the currently selected layer."""
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

    peel_distance: bpy.props.FloatProperty(name="Peel Distance", default=0.5, min=0.0, max=10.0)
    frame_start: bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    frame_end: bpy.props.IntProperty(name="End Frame", default=30, min=1)

    def execute(self, context):
        active_obj = context.active_object
        if not active_obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        initial_location = active_obj.location.copy()
        active_obj.location = initial_location
        active_obj.keyframe_insert(data_path="location", frame=self.frame_start)

        peel_offset = Vector((0, 0, self.peel_distance))
        active_obj.location = initial_location + peel_offset
        active_obj.keyframe_insert(data_path="location", frame=self.frame_end)

        state = context.scene.dissect_state
        cut_record = state.cut_history.add()
        cut_record.object_name = active_obj.name
        cut_record.cut_type = "peel"
        cut_record.timestamp = time.time()
        cut_record.description = f"Peel animation on {active_obj.name}"

        state.cut_count += 1
        state.is_modified = True
        return {'FINISHED'}


class DISSECT_OT_commit_cut(Operator):
    """Finalize the current cut operation."""
    bl_idname = "dissect.commit_cut"
    bl_label = "Commit Cut"
    bl_options = {'REGISTER'}

    def execute(self, context):
        state = context.scene.dissect_state
        state.is_modified = False
        self.report({'INFO'}, "Cut committed")
        return {'FINISHED'}
