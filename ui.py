"""UI Panel for Z-Dissect in the N-panel."""
import bpy
from bpy.types import Operator, Panel
from .anatomy_data import ANATOMY_HIERARCHY


class DISSECT_OT_expand_region(Operator):
    """Placeholder for region expansion (used for UI state)."""
    bl_idname = "dissect.expand_region"
    bl_label = "Expand Region"
    bl_options = {'REGISTER'}

    system_name: bpy.props.StringProperty()
    region_name: bpy.props.StringProperty()

    def execute(self, context):
        return {'FINISHED'}


class DISSECT_PT_main(Panel):
    """Main dissection panel in the N-panel."""
    bl_label = "Z-Dissect"
    bl_idname = "DISSECT_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z-Dissect"

    def draw(self, context):
        layout = self.layout
        state = context.scene.dissect_state

        # Header
        row = layout.row()
        row.label(text="Z-Dissect", icon='MOD_BOOLEAN')
        if state.is_modified:
            row.label(text="●", icon='ERROR')

        layout.separator()

        # Tool Shelf
        box = layout.box()
        box.label(text="Tools", icon='TOOL_SETTINGS')
        row = box.row(align=True)
        row.operator("dissect.scalpel", text="Scalpel", icon='MOD_BOOLEAN')
        row = box.row(align=True)
        row.operator("dissect.remove_layer", text="Remove", icon='HIDE_ON')
        row = box.row(align=True)
        row.operator("dissect.peel", text="Peel", icon='ANIM')

        layout.separator()

        # Layer Controls
        box = layout.box()
        box.label(text="Layers", icon='GROUP')
        row = box.row()
        row.prop(state, "current_layer", slider=True)
        layout.label(text="0=Skin, 1=Fat, 2=Fascia, 3=Muscle, 4=Bone")

        layout.separator()

        # System Browser
        box = layout.box()
        box.label(text="System Browser", icon='GROUP')

        for system_name, regions in ANATOMY_HIERARCHY.items():
            row = box.row()
            row.prop(state, "current_system",
                     text="",
                     value=system_name,
                     icon='RADIOBUT_OFF' if state.current_system != system_name else 'RADIOBUT_ON',
                     expand=False)
            op = row.operator("dissect.select_system", text="", icon='RESTRICT_SELECT_OFF')
            op.system_name = system_name

            if state.current_system == system_name:
                for region_name, parts in regions.items():
                    row = box.row(align=True)
                    row.separator(level=1)
                    row.prop(state, "current_region",
                             text="",
                             value=region_name,
                             icon='RADIOBUT_OFF' if state.current_region != region_name else 'RADIOBUT_ON',
                             expand=False)
                    op = row.operator("dissect.select_region", text="", icon='RESTRICT_SELECT_OFF')
                    op.system_name = system_name
                    op.region_name = region_name

        layout.separator()

        # Progress
        box = layout.box()
        box.label(text="Progress", icon='TRACKING')
        row = box.row()
        row.label(text=f"Cuts: {state.cut_count}")
        row.label(text=f"System: {state.current_system}")

        layout.separator()

        # State Management
        box = layout.box()
        box.label(text="State", icon='FILE')
        row = box.row(align=True)
        row.operator("dissect.save_dissection", text="Save", icon='EXPORT')
        row.operator("dissect.restore_dissection", text="Load", icon='IMPORT')
        layout.separator()
        row = layout.row()
        row.operator("dissect.reset_dissection", text="Reset All", icon='LOOP_BACK')
        row.operator("dissect.undo_last_cut", text="Undo Cut", icon='UNDO')

        layout.separator()

        # Utilities
        layout.operator("dissect.refresh_anatomy", text="Refresh Anatomy", icon='FILE_REFRESH')


class DISSECT_UL_anatomy_tree(Panel):
    """UI list for anatomy tree view."""
    bl_label = "Anatomy Tree"
    bl_idname = "DISSECT_UL_anatomy_tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z-Dissect"

    def draw(self, context):
        layout = self.layout
        state = context.scene.dissect_state

        for system_name, regions in ANATOMY_HIERARCHY.items():
            box = layout.box()
            row = box.row()
            row.label(text=system_name, icon='OBJECT_DATA')
            op = row.operator("dissect.select_system", text="Select All", icon='SELECT_EXTEND')
            op.system_name = system_name

            for region_name, parts in regions.items():
                row = box.row(align=True)
                row.separator(level=1)
                row.label(text=region_name, icon='GROUP')
                op = row.operator("dissect.select_region", text="", icon='SELECT_EXTEND')
                op.system_name = system_name
                op.region_name = region_name

                for part_name in parts[:5]:
                    row = box.row(align=True)
                    row.separator(level=2)
                    row.label(text=part_name, icon='MESH_CUBE')
