#!/usr/bin/env python3
"""
Z-Dissect Compatibility Test Script

Run this script in Blender to validate integration with Z-Anatomy models.
Usage: blender --background --python test_compatibility.py
       Or run from Blender's Script Editor.
"""

import bpy
import sys

def test_z_anatomy_collections():
    """Test if Z-Anatomy collections exist."""
    print("\n" + "=" * 60)
    print("TEST 1: Z-Anatomy Collections")
    print("=" * 60)

    expected_collections = [
        '.Skeletal system',
        '.Muscular system',
        '.Nervous system & Sense organs',
        '.Cardiovascular system',
        '.Visceral systems',
    ]

    found = []
    missing = []

    for col_name in expected_collections:
        if col_name in bpy.data.collections:
            col = bpy.data.collections[col_name]
            obj_count = len([o for o in col.all_objects if o.type == 'MESH'])
            found.append((col_name, obj_count))
            print(f"  ✓ {col_name}: {obj_count} mesh objects")
        else:
            missing.append(col_name)
            print(f"  ✗ {col_name}: NOT FOUND")

    return len(found), len(missing)


def test_object_naming():
    """Test object naming conventions."""
    print("\n" + "=" * 60)
    print("TEST 2: Object Naming Conventions")
    print("=" * 60)

    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']

    # Count objects with different suffixes
    labels = [o for o in mesh_objects if '.t' in o.name]
    connectors = [o for o in mesh_objects if '.j' in o.name]
    groups = [o for o in mesh_objects if '.g' in o.name]
    anatomical = [o for o in mesh_objects
                  if not any(s in o.name for s in ['.t', '.j', '.g', '.st'])]

    print(f"  Total mesh objects: {len(mesh_objects)}")
    print(f"  Text labels (.t): {len(labels)}")
    print(f"  Connectors (.j): {len(connectors)}")
    print(f"  Groups (.g): {len(groups)}")
    print(f"  Anatomical objects: {len(anatomical)}")

    # Sample object names
    print("\n  Sample anatomical object names:")
    for obj in anatomical[:10]:
        print(f"    - {obj.name}")

    return len(anatomical)


def test_parent_child_hierarchy():
    """Test parent-child hierarchy."""
    print("\n" + "=" * 60)
    print("TEST 3: Parent-Child Hierarchy")
    print("=" * 60)

    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']

    with_parent = [o for o in mesh_objects if o.parent]
    without_parent = [o for o in mesh_objects if not o.parent]

    print(f"  Objects with parent: {len(with_parent)}")
    print(f"  Objects without parent: {len(without_parent)}")

    # Sample hierarchy
    print("\n  Sample hierarchy (root objects with children):")
    roots = [o for o in mesh_objects if not o.parent and o.children]
    for root in roots[:5]:
        children_count = len(root.children)
        print(f"    - {root.name}: {children_count} children")

    return len(roots)


def test_muscular_system():
    """Test muscular system detection."""
    print("\n" + "=" * 60)
    print("TEST 4: Muscular System Detection")
    print("=" * 60)

    muscle_keywords = [
        'musculus', 'biceps', 'triceps', 'deltoid', 'pectoral',
        'gluteus', 'gastrocnemius', 'soleus', 'trapezius'
    ]

    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']
    potential_muscles = []

    for obj in mesh_objects:
        name_lower = obj.name.lower()
        if any(kw in name_lower for kw in muscle_keywords):
            if not any(s in obj.name for s in ['.t', '.j', '.g']):
                potential_muscles.append(obj.name)

    print(f"  Potential muscle objects: {len(potential_muscles)}")
    if potential_muscles:
        print("  Sample muscles found:")
        for name in sorted(potential_muscles)[:10]:
            print(f"    - {name}")

    return len(potential_muscles)


def test_skeletal_system():
    """Test skeletal system detection."""
    print("\n" + "=" * 60)
    print("TEST 5: Skeletal System Detection")
    print("=" * 60)

    bone_keywords = [
        'femur', 'tibia', 'humerus', 'radius', 'ulna',
        'skull', 'mandible', 'vertebr', 'rib', 'sternum'
    ]

    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']
    potential_bones = []

    for obj in mesh_objects:
        name_lower = obj.name.lower()
        if any(kw in name_lower for kw in bone_keywords):
            if not any(s in obj.name for s in ['.t', '.j', '.g']):
                potential_bones.append(obj.name)

    print(f"  Potential bone objects: {len(potential_bones)}")
    if potential_bones:
        print("  Sample bones found:")
        for name in sorted(potential_bones)[:10]:
            print(f"    - {name}")

    return len(potential_bones)


def test_boolean_readiness():
    """Test if objects are ready for Boolean operations."""
    print("\n" + "=" * 60)
    print("TEST 6: Boolean Operation Readiness")
    print("=" * 60)

    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']
    anatomical = [o for o in mesh_objects
                  if not any(s in o.name for s in ['.t', '.j', '.g', '.st'])]

    has_geometry = []
    no_geometry = []

    for obj in anatomical:
        if obj.data and len(obj.data.vertices) > 0:
            has_geometry.append(obj.name)
        else:
            no_geometry.append(obj.name)

    print(f"  Objects with geometry: {len(has_geometry)}")
    print(f"  Objects without geometry: {len(no_geometry)}")

    if no_geometry:
        print("  Warning: Some objects have no geometry:")
        for name in no_geometry[:5]:
            print(f"    - {name}")

    # Check polygon count
    total_polys = sum(len(obj.data.polygons) for obj in anatomical if obj.data)
    print(f"\n  Total polygons in anatomical objects: {total_polys:,}")

    return len(has_geometry)


def test_collection_visibility():
    """Test collection visibility settings."""
    print("\n" + "=" * 60)
    print("TEST 7: Collection Visibility")
    print("=" * 60)

    for col_name in ['.Muscular system', '.Skeletal system', '.Nervous system & Sense organs']:
        if col_name in bpy.data.collections:
            col = bpy.data.collections[col_name]
            # Check if collection is linked to scene
            is_linked = col in bpy.context.scene.collection.children
            print(f"  {col_name}: linked={is_linked}")

    return True


def run_all_tests():
    """Run all compatibility tests."""
    print("\n" + "=" * 60)
    print("Z-DISSECT COMPATIBILITY TEST")
    print("Testing integration with Z-Anatomy models")
    print("=" * 60)

    results = {
        'Collections': test_z_anatomy_collections(),
        'Naming': test_object_naming(),
        'Hierarchy': test_parent_child_hierarchy(),
        'Muscular': test_muscular_system(),
        'Skeletal': test_skeletal_system(),
        'Boolean': test_boolean_readiness(),
        'Visibility': test_collection_visibility(),
    }

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, result in results.items():
        if isinstance(result, tuple):
            found, missing = result
            status = "PASS" if missing == 0 else "PARTIAL"
            print(f"  {test_name}: {status} ({found} found, {missing} missing)")
            if missing > 0:
                all_passed = False
        elif isinstance(result, int):
            status = "PASS" if result > 0 else "FAIL"
            print(f"  {test_name}: {status} ({result} objects)")
            if result == 0:
                all_passed = False
        elif isinstance(result, bool):
            status = "PASS" if result else "FAIL"
            print(f"  {test_name}: {status}")
            if not result:
                all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Z-Dissect is compatible with Z-Anatomy")
    else:
        print("✗ SOME TESTS FAILED - Check Z-Anatomy model structure")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)