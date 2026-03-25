# Z-Dissect - Anatomical Dissection Simulator for Blender

A Blender addon for interactive anatomical dissection simulation, integrated with Z-Anatomy models.

## Features

- **Scalpel Tool**: Boolean-based dissection cuts on anatomical models
- **Layer Removal**: Non-destructive hiding of anatomical layers
- **Peel Animation**: Animated peeling with keyframe support
- **System Browser**: Navigate by anatomical system (Muscular, Skeletal, Nervous)
- **State Save/Load**: Export and restore dissection progress (`.zdissect` files)
- **Undo History**: Revert cuts from history

## Requirements

- **Blender 3.0+** (tested with Blender 4.x)
- **Z-Anatomy Template** (download separately - see below)

## Installation

### Step 1: Download Z-Anatomy Models

The Z-Anatomy models are large files hosted separately. Download them from:

```bash
# Download Z-Anatomy template (contains Startup.blend with anatomical models)
curl -L -o Z-Anatomy.zip "https://github.com/Z-Anatomy/Models-of-human-anatomy/raw/master/Z-Anatomy.zip"
```

Or download manually from: https://github.com/Z-Anatomy/Models-of-human-anatomy

### Step 2: Install Z-Anatomy Template

1. Copy `Z-Anatomy.zip` to your Blender templates directory:
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/startup/`
   - **Windows**: `C:\Users\<you>\AppData\Roaming\Blender\4.5\scripts\startup\`
   - **Linux**: `~/.config/blender/4.5/scripts/startup/`

2. Restart Blender
3. Create new file from template: **File → New → Z-Anatomy**

### Step 3: Install Z-Dissect Addon

1. Clone or download this repository
2. Copy the `z_dissect/` folder to your Blender addons directory:
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`
   - **Windows**: `C:\Users\<you>\AppData\Roaming\Blender\4.5\scripts\addons/`
   - **Linux**: `~/.config/blender/4.5/scripts/addons/`

3. Open Blender → **Edit → Preferences → Add-ons**
4. Search for "Z-Dissect" and enable it

### Step 4: Install Optional Z-Anatomy Addons (Recommended)

Download companion addons for enhanced functionality:

```bash
# Download all Z-Anatomy companion addons
curl -L -o addons.zip "https://github.com/Z-Anatomy/Blender-addons/archive/refs/heads/main.zip"
unzip addons.zip
```

Install each addon:
- **Z-Cross**: Cross-section planes for slicing views
- **Z-Label**: Create anatomical labels and annotations
- **Z-Mirror**: Toggle mirror modifiers for symmetrical anatomy
- **Z-Sync**: Synchronize visibility across views
- **Z-Translate**: Translate anatomical names

## Usage

### Quick Start

1. Open Blender with Z-Anatomy template
2. Press `N` to open the N-panel (3D View sidebar)
3. Click the **Z-Dissect** tab
4. Use the tools:

| Tool | Description |
|------|-------------|
| **Scalpel** | Draw a cut line on selected mesh |
| **Remove** | Hide the selected anatomical layer |
| **Peel** | Animate peeling of layers |
| **Undo Cut** | Revert the last dissection cut |
| **Reset All** | Restore all hidden objects |
| **Save State** | Export current dissection state |
| **Load State** | Import a saved state file |

### Selecting Anatomy

Use the **System Browser** panel to select anatomical structures:

1. **System**: Choose Muscular, Skeletal, or Nervous
2. **Region**: Select body region (Head, Torso, Upper Limb, etc.)
3. **Part**: Pick specific anatomical part

Click **Select** to highlight the structure in the viewport.

### Dissection Workflow

1. Select the anatomical structure you want to dissect
2. Enter **Scalpel Mode** by clicking the Scalpel button
3. Draw a cut path on the mesh surface
4. Press **Enter** to execute the Boolean cut
5. Use **Remove** to hide layers progressively
6. **Save State** to preserve your dissection progress

## Anatomical Data

The addon includes the TA2 (Terminologia Anatomica 2) hierarchy for:

- **Muscular System**: ~200+ muscles organized by region
- **Skeletal System**: Bones by body region
- **Nervous System**: Major nerves and neural structures

## File Structure

```
z_dissect/
├── __init__.py          # Addon registration and bl_info
├── anatomy_data.py      # TA2 anatomical hierarchy
├── properties.py        # Dissection state properties
├── select.py            # Selection operators by system/region
├── dissect_ops.py       # Scalpel, Remove, Peel operators
├── state.py             # State export/import helpers
├── ui.py                # N-panel UI
├── utils.py             # Utility functions
├── install.py           # Installation helper script
└── README.md            # This file
```

## Download Links

| Resource | URL |
|----------|-----|
| Z-Anatomy Models | https://github.com/Z-Anatomy/Models-of-human-anatomy |
| Z-Anatomy Addons | https://github.com/Z-Anatomy/Blender-addons |
| Z-Dissect Addon | https://github.com/sunilchhajwani/z-dissect-blender-addon |

## Credits

- **Z-Anatomy Models**: [Z-Anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy) by Gauthier Kervyn, Marcin Zielinski, Lluis Vinent
- **BodyParts3D**: Database Center for Life Science
- **License**: CC-BY-SA 4.0

## Support

- **Issues**: [GitHub Issues](https://github.com/sunilchhajwani/z-dissect-blender-addon/issues)
- **Z-Anatomy Project**: [z-anatomy.com](https://www.z-anatomy.com/)