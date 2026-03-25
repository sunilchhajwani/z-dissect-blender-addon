"""Blender Properties for dissection state tracking."""
import bpy
import json
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty
from bpy.types import PropertyGroup, Operator


class CutRecord(PropertyGroup):
    """Record of a single cut operation."""
    object_name: StringProperty(name="Object Name")
    cut_type: StringProperty(name="Cut Type")  # 'scalpel', 'remove', 'peel', 'sweep', 'optimize'
    timestamp: FloatProperty(name="Timestamp")
    backup_data: StringProperty(name="Backup Data")  # JSON of original mesh state
    description: StringProperty(name="Description")


class LayerRecord(PropertyGroup):
    """Record of a hidden/removed layer."""
    object_name: StringProperty(name="Object Name")
    layer_index: IntProperty(name="Layer Index")
    hidden: BoolProperty(name="Hidden")


class DissectionState(PropertyGroup):
    """Main dissection state property group."""
    current_system: StringProperty(
        name="Current System",
        default="Muscular System"
    )
    current_region: StringProperty(
        name="Current Region",
        default=""
    )
    current_layer: IntProperty(
        name="Current Layer",
        default=0,
        min=0,
        max=10,
        description="Dissection layer: 0=Skin, 1=Fat, 2=Fascia, 3=Muscle, 4=Bone"
    )
    is_modified: BoolProperty(
        name="Modified",
        default=False
    )
    active_tool: StringProperty(
        name="Active Tool",
        default="select",
        description="Current dissection tool"
    )
    cut_count: IntProperty(
        name="Cut Count",
        default=0
    )

    # Optimization Properties
    decimate_ratio: FloatProperty(
        name="Decimate Ratio",
        description="Ratio of faces to keep (1.0 = 100%, 0.1 = 10%)",
        default=0.5,
        min=0.0,
        max=1.0
    )
    optimization_mode: EnumProperty(
        name="Mode",
        description="Optimization algorithm",
        items=[
            ('COLLAPSE', "Collapse", "Reduce polycount while preserving shape"),
            ('UNSUBDIVIDE', "Un-Subdivide", "Reconstruct lower-level mesh"),
            ('DISSOLVE', "Dissolve", "Remove planar vertices")
        ],
        default='COLLAPSE'
    )
    use_remesh: BoolProperty(
        name="Use Remesh",
        description="Apply Remesh for cleaner topology",
        default=False
    )

    # Collections for tracking
    cut_history: CollectionProperty(type=CutRecord)
    hidden_layers: CollectionProperty(type=LayerRecord)


class DISSECT_OT_save_dissection(Operator):
    """Save current dissection state to a .zdissect file."""
    bl_idname = "dissect.save_dissection"
    bl_label = "Save Dissection State"
    bl_options = {'REGISTER'}

    filter_glob: StringProperty(
        default="*.zdissect",
        options={'HIDDEN'}
    )
    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        scene = context.scene
        state = scene.dissect_state

        save_data = {
            'version': (0, 1, 0),
            'current_system': state.current_system,
            'current_region': state.current_region,
            'current_layer': state.current_layer,
            'cut_count': state.cut_count,
            'cuts': [],
            'hidden': []
        }

        for cut in state.cut_history:
            save_data['cuts'].append({
                'object_name': cut.object_name,
                'cut_type': cut.cut_type,
                'timestamp': cut.timestamp,
                'description': cut.description
            })

        for hidden in state.hidden_layers:
            save_data['hidden'].append({
                'object_name': hidden.object_name,
                'hidden': hidden.hidden
            })

        with open(self.filepath, 'w') as f:
            json.dump(save_data, f, indent=2)

        state.is_modified = False
        self.report({'INFO'}, f"Dissection saved to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class DISSECT_OT_restore_dissection(Operator):
    """Restore dissection state from a .zdissect file."""
    bl_idname = "dissect.restore_dissection"
    bl_label = "Restore Dissection State"
    bl_options = {'REGISTER'}

    filter_glob: StringProperty(
        default="*.zdissect",
        options={'HIDDEN'}
    )
    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        scene = context.scene
        state = scene.dissect_state

        with open(self.filepath, 'r') as f:
            save_data = json.load(f)

        state.current_system = save_data.get('current_system', 'Muscular System')
        state.current_region = save_data.get('current_region', '')
        state.current_layer = save_data.get('current_layer', 0)
        state.cut_count = save_data.get('cut_count', 0)

        # Clear existing records
        state.cut_history.clear()
        state.hidden_layers.clear()

        for cut_data in save_data.get('cuts', []):
            cut = state.cut_history.add()
            cut.object_name = cut_data['object_name']
            cut.cut_type = cut_data['cut_type']
            cut.timestamp = cut_data['timestamp']
            cut.description = cut_data['description']

        for hidden_data in save_data.get('hidden', []):
            hidden = state.hidden_layers.add()
            hidden.object_name = hidden_data['object_name']
            hidden.hidden = hidden_data['hidden']

        state.is_modified = False
        self.report({'INFO'}, f"Dissection restored from {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class DISSECT_OT_reset_dissection(Operator):
    """Reset all dissection changes and restore original state."""
    bl_idname = "dissect.reset_dissection"
    bl_label = "Reset Dissection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        state = scene.dissect_state

        # Unhide all objects
        for obj in context.view_layer.objects:
            obj.hide_set(False)
            obj.hide_viewport = False

        # Clear collections
        state.cut_history.clear()
        state.hidden_layers.clear()
        state.current_layer = 0
        state.cut_count = 0
        state.is_modified = False

        self.report({'INFO'}, "Dissection reset complete")
        return {'FINISHED'}


class DISSECT_OT_undo_last_cut(Operator):
    """Undo the last cut operation."""
    bl_idname = "dissect.undo_last_cut"
    bl_label = "Undo Last Cut"
    bl_options={'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        state = scene.dissect_state

        if len(state.cut_history) == 0:
            self.report({'WARNING'}, "No cuts to undo")
            return {'CANCELLED'}

        # Remove last cut record
        state.cut_history.remove(len(state.cut_history) - 1)
        state.cut_count = max(0, state.cut_count - 1)

        self.report({'INFO'}, "Last cut undone")
        return {'FINISHED'}
