"""Anatomical selection operators for Z-Dissect."""
import bpy
from bpy.types import Operator
from .anatomy_data import ANATOMY_HIERARCHY, get_object_system, get_system_regions, get_all_systems
from .utils import clear_selection, select_objects


class DISSECT_OT_select_system(Operator):
    """Select all objects belonging to a body system."""
    bl_idname = "dissect.select_system"
    bl_label = "Select Anatomy System"
    bl_options = {'REGISTER', 'UNDO'}

    system_name: bpy.props.StringProperty(name="System Name")

    def execute(self, context):
        system_name = self.system_name
        selected_objects = []

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj_system = get_object_system(obj.name)
                if obj_system == system_name:
                    selected_objects.append(obj)

        if not selected_objects:
            self.report({'WARNING'}, f"No objects found for {system_name}")
            return {'CANCELLED'}

        select_objects(selected_objects)
        context.scene.dissect_state.current_system = system_name
        self.report({'INFO'}, f"Selected {len(selected_objects)} objects in {system_name}")
        return {'FINISHED'}


class DISSECT_OT_select_region(Operator):
    """Select all objects in an anatomical region."""
    bl_idname = "dissect.select_region"
    bl_label = "Select Anatomy Region"
    bl_options = {'REGISTER', 'UNDO'}

    system_name: bpy.props.StringProperty(name="System Name")
    region_name: bpy.props.StringProperty(name="Region Name")

    def execute(self, context):
        region_parts = ANATOMY_HIERARCHY.get(self.system_name, {}).get(self.region_name, [])
        selected_objects = []

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj_name_lower = obj.name.lower()
                for part in region_parts:
                    if part.lower().replace(' ', '') in obj_name_lower.replace(' ', ''):
                        selected_objects.append(obj)
                        break

        if not selected_objects:
            self.report({'WARNING'}, f"No objects found for {self.region_name}")
            return {'CANCELLED'}

        select_objects(selected_objects)
        context.scene.dissect_state.current_region = self.region_name
        self.report({'INFO'}, f"Selected {len(selected_objects)} objects in {self.region_name}")
        return {'FINISHED'}


class DISSECT_OT_select_hierarchy(Operator):
    """Select an object and all its children in the hierarchy."""
    bl_idname = "dissect.select_hierarchy"
    bl_label = "Select Anatomy Hierarchy"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        root_obj = selected[0]
        selected_objects = [root_obj]

        def get_children(obj):
            children = []
            for child in bpy.data.objects:
                if child.parent == obj:
                    children.append(child)
            return children

        queue = [root_obj]
        while queue:
            current = queue.pop(0)
            children = get_children(current)
            for child in children:
                selected_objects.append(child)
                queue.append(child)

        select_objects(selected_objects)
        self.report({'INFO'}, f"Selected {len(selected_objects)} objects in hierarchy")
        return {'FINISHED'}


class DISSECT_OT_refresh_anatomy(Operator):
    """Refresh anatomy data and rebuild system maps."""
    bl_idname = "dissect.refresh_anatomy"
    bl_label = "Refresh Anatomy Data"
    bl_options = {'REGISTER'}

    def execute(self, context):
        from . import anatomy_data
        anatomy_data.load_anatomy_data()
        self.report({'INFO'}, "Anatomy data refreshed")
        return {'FINISHED'}
