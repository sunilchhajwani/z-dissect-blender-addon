# Z-Dissect - Developer Documentation

Technical documentation for developers and advanced users.

---

## Architecture Overview

```
z_dissect/
├── __init__.py          # Addon registration and bl_info
├── anatomy_data.py      # Z-Anatomy structure mappings, object detection
├── properties.py        # DissectionState, CutRecord, LayerRecord properties
├── select.py            # Selection operators by system/region
├── dissect_ops.py       # Scalpel, Remove, Peel operators
├── state.py             # State export/import (.zdissect files)
├── ui.py                # N-panel UI components
├── utils.py             # Helper functions (selection, object utilities)
├── test_compatibility.py # Validation script for Z-Anatomy integration
└── install.py           # Installation helper script
```

---

## Module Details

### `__init__.py`

Entry point for the addon. Registers all Blender classes and initializes anatomy data.

```python
bl_info = {
    "name": "Z-Dissect",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "category": "3D View",
}
```

### `anatomy_data.py`

Handles Z-Anatomy integration:

- `ZANATOMY_COLLECTIONS` - List of Z-Anatomy collection names
- `COLLECTION_TO_SYSTEM` - Maps collections to systems
- `MUSCLE_NAME_MAP`, `BONE_NAME_MAP`, `NERVE_NAME_MAP` - Latin/English translations
- `_detect_system_from_name()` - Heuristic object detection
- `load_anatomy_data()` - Builds object maps from scene
- `get_objects_in_system()` - Returns objects for a system

### `properties.py`

Blender property groups for state management:

- `DissectionState` - Main property group attached to Scene
- `CutRecord` - Stores Boolean cut history
- `LayerRecord` - Stores hidden layer info
- Save/Load operators for `.zdissect` files

### `dissect_ops.py`

Core dissection operators:

- `DISSECT_OT_scalpel` - Draw and execute Boolean cuts
- `DISSECT_OT_remove_layer` - Hide selected layer
- `DISSECT_OT_peel` - Animate layer peeling with keyframes
- `DISSECT_OT_commit_cut` - Apply Boolean operation

### `select.py`

Anatomy selection operators:

- `DISSECT_OT_select_system` - Select all in a system
- `DISSECT_OT_select_region` - Select by body region
- `DISSECT_OT_select_hierarchy` - Select by hierarchy path
- `DISSECT_OT_refresh_anatomy` - Rebuild anatomy cache

### `ui.py`

N-panel UI components:

- `DISSECT_PT_main` - Main panel in 3D View sidebar
- `DISSECT_UL_anatomy_tree` - Anatomy hierarchy browser

---

## Z-Anatomy Integration

### Collection Structure

Z-Anatomy uses collections with dot prefix:

```
.Muscular system
.Skeletal system
.Nervous system & Sense organs
.Cardiovascular system
.Visceral systems
```

### Object Naming Conventions

| Suffix | Meaning |
|--------|---------|
| `.t` | Text label |
| `.j` | Connector line |
| `.g` | Group object |
| `.st` | Secondary text label |

### Latin/English Mappings

Z-Anatomy uses Latin names. The addon maps to English:

```python
MUSCLE_NAME_MAP = {
    'Musculus biceps brachii': 'Biceps brachii',
    'Musculus triceps brachii': 'Triceps brachii',
    # ... 50+ mappings
}
```

---

## API Reference

### Getting Objects by System

```python
import bpy
from z_dissect.anatomy_data import get_objects_in_system

# Get all muscle objects
muscles = get_objects_in_system('Muscular System')

# Get all skeletal objects
bones = get_objects_in_system('Skeletal System')
```

### Detecting Object System

```python
from z_dissect.anatomy_data import get_object_system

obj = bpy.context.active_object
system = get_object_system(obj.name)
# Returns: 'Muscular System', 'Skeletal System', etc.
```

### Getting System Regions

```python
from z_dissect.anatomy_data import get_system_regions

regions = get_system_regions('Muscular System')
# Returns: ['Head & Neck', 'Thorax', 'Upper Limb', ...]
```

---

## Testing

### Run Compatibility Test

```bash
# From command line
blender --background --python test_compatibility.py

# Or in Blender Script Editor
# Open test_compatibility.py and click Run
```

### Test Coverage

The test script validates:

1. Z-Anatomy collection existence
2. Object naming conventions
3. Parent-child hierarchy
4. Muscular/Skeletal system detection
5. Boolean operation readiness
6. Collection visibility

---

## Command Line Installation

For automated setups:

```bash
# Download Z-Anatomy models
curl -L -o Z-Anatomy.zip \
  "https://github.com/Z-Anatomy/Models-of-human-anatomy/raw/master/Z-Anatomy.zip"

# Download companion addons
curl -L -o addons.zip \
  "https://github.com/Z-Anatomy/Blender-addons/archive/refs/heads/main.zip"
unzip addons.zip

# Run install script (requires Blender)
blender --background --python install.py
```

---

## Blender Version Compatibility

| Blender Version | Status |
|----------------|--------|
| 4.5+ | ✅ Fully supported |
| 4.0 - 4.4 | ⚠️ Should work, untested |
| 3.x | ❌ Not supported |
| 2.x | ❌ Not supported |

---

## Contributing

### Code Style

- Follow PEP 8 for Python
- Use type hints where possible
- Document all public functions

### Adding New Anatomy

To add new anatomical structures:

1. Edit `anatomy_data.py`
2. Add entries to `ANATOMY_HIERARCHY`
3. Add Latin/English mappings if needed
4. Run `test_compatibility.py`

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit PR with description

---

## Known Limitations

1. **Large Files**: Z-Anatomy models are 300MB, not included in repo
2. **Naming Variations**: Some objects may not be detected automatically
3. **Boolean Performance**: Complex cuts may be slow on older hardware
4. **Undo Stack**: Limited to 32 cuts in history

---

## Performance Tips

- Use Simplified view mode (press Z → Wireframe) for faster navigation
- Hide collections not in use
- Work with subsections, not full body
- Use Object mode for selection, Edit mode for cuts

---

## License

CC-BY-SA 4.0 - See LICENSE file for details.

---

## Related Projects

- [Z-Anatomy Models](https://github.com/Z-Anatomy/Models-of-human-anatomy)
- [Z-Anatomy Addons](https://github.com/Z-Anatomy/Blender-addons)
- [BodyParts3D](https://lifesciencedb.jp/bp3d/)
- [Blender API Docs](https://docs.blender.org/api/current/)