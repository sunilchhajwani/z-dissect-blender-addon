bl_info = {
    "name": "Z-Dissect",
    "description": "Anatomical dissection simulator for Z-Anatomy — scalpel cuts, layer removal, and peel tools with state save/restore",
    "author": "Z-Anatomy Contributors",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > N-Panel > Z-Dissect",
    "doc_url": "https://github.com/Z-Anatomy/Z-Dissect",
    "category": "3D View",
    "license": "CC-BY-SA-4.0",
}

import bpy
from . import properties
from . import anatomy_data
from . import select
from . import dissect_ops
from . import ui
from . import state
from . import utils

classes = (
    properties.DissectionState,
    properties.CutRecord,
    properties.LayerRecord,
    properties.DISSECT_OT_save_dissection,
    properties.DISSECT_OT_restore_dissection,
    properties.DISSECT_OT_reset_dissection,
    properties.DISSECT_OT_undo_last_cut,
    select.DISSECT_OT_select_system,
    select.DISSECT_OT_select_region,
    select.DISSECT_OT_select_hierarchy,
    select.DISSECT_OT_refresh_anatomy,
    dissect_ops.DISSECT_OT_scalpel,
    dissect_ops.DISSECT_OT_sweep_scalpel,
    dissect_ops.DISSECT_OT_optimize_mesh,
    dissect_ops.DISSECT_OT_remove_layer,
    dissect_ops.DISSECT_OT_peel,
    dissect_ops.DISSECT_OT_commit_cut,
    ui.DISSECT_PT_main,
    ui.DISSECT_UL_anatomy_tree,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.dissect_state = bpy.props.PointerProperty(type=properties.DissectionState)

    anatomy_data.load_anatomy_data()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.dissect_state


if __name__ == "__main__":
    register()
