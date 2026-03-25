"""Shared utilities for Z-Dissect."""
import bpy


def get_anatomy_root():
    """Return the root object of the anatomy hierarchy (usually 'Anatomy')."""
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and 'Anatomy' in obj.name:
            return obj
    for obj in bpy.data.objects:
        if obj.name.startswith('Anatomy') or 'anatomy' in obj.name.lower():
            return obj
    return None


def get_muscle_objects():
    """Return all objects tagged as muscular tissue."""
    muscles = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            name_lower = obj.name.lower()
            if any(tag in name_lower for tag in ('musculus', 'muscle', 'mUSC', 'biceps', 'triceps', 'deltoid', 'pectoral', 'abdominis', 'quadriceps', 'gastrocnemius')):
                muscles.append(obj)
    return muscles


def get_skeletal_objects():
    """Return all objects tagged as bone/skeletal."""
    bones = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            name_lower = obj.name.lower()
            if any(tag in name_lower for tag in ('os', 'bone', 'skeletal', 'femur', 'tibia', 'humerus', 'radius', 'ulna', 'pelvis', 'spine', 'skull', 'cranium')):
                bones.append(obj)
    return bones


def get_nervous_objects():
    """Return all objects tagged as nervous tissue."""
    nerves = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            name_lower = obj.name.lower()
            if any(tag in name_lower for tag in ('nerv', 'nerve', 'brain', 'spinal', 'ganglion')):
                nerves.append(obj)
    return nerves


def set_object_selection(obj, select):
    """Set object selection state."""
    obj.select_set(select)


def clear_selection():
    """Deselect all objects."""
    bpy.ops.object.select_all(action='DESELECT')


def select_objects(objects):
    """Select a list of objects."""
    clear_selection()
    for obj in objects:
        obj.select_set(True)
