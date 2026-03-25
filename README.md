# Z-Dissect - Anatomical Dissection Simulator for Blender

A Blender addon for interactive anatomical dissection simulation, integrated with Z-Anatomy 3D models.

## What You'll Learn to Do

- Explore 3D human anatomy (muscles, bones, nerves)
- Make virtual dissection cuts on anatomical models
- Remove layers to see what's underneath
- Animate peeling of anatomical structures
- Save and restore your dissection progress

---

## Complete Setup Guide (For Everyone)

### Prerequisites Checklist

Before starting, make sure you have:

- [ ] A computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] At least 10 GB of free disk space
- [ ] Basic mouse with left and right click (recommended)

---

## Step 1: Install Blender

Blender is the free 3D software that runs Z-Dissect.

### For Windows

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **https://www.blender.org/download/**
3. Click the **"Download Blender"** button
4. The file will download automatically (it's about 300 MB)
5. Once downloaded, find the file in your **Downloads** folder
6. Double-click the file to run it
7. Click **"Next"** through all the installation screens
8. Click **"Install"** and wait for it to finish
9. Click **"Finish"**

### For Mac

1. Open your web browser
2. Go to: **https://www.blender.org/download/**
3. Click the **"Download Blender"** button
4. Open your **Downloads** folder
5. Drag the **Blender.app** file to your **Applications** folder
6. Done!

### For Linux

1. Open your web browser
2. Go to: **https://www.blender.org/download/**
3. Download the appropriate version for your distribution
4. Extract and install according to your distribution's method

### Verify Blender Installation

1. Open Blender from your Start menu (Windows) or Applications folder (Mac)
2. You should see a 3D cube in the center of the screen
3. If you see this, Blender is installed correctly!
4. Close Blender for now (we'll open it again later)

---

## Step 2: Download Z-Dissect Addon

### Option A: Download as ZIP (Easiest)

1. Open your web browser
2. Go to: **https://github.com/sunilchhajwani/z-dissect-blender-addon**
3. Click the green **"Code"** button near the top right
4. Click **"Download ZIP"**
5. Save the file to your computer
6. Once downloaded, right-click the ZIP file and select **"Extract All"** (Windows) or double-click to extract (Mac)
7. Remember where you extracted the folder - you'll need it in Step 4

### Option B: Clone with Git (For developers)

```bash
git clone https://github.com/sunilchhajwani/z-dissect-blender-addon.git
```

---

## Step 3: Download Z-Anatomy 3D Models

The Z-Anatomy models contain the actual 3D human anatomy (muscles, bones, etc.). These are large files (~300 MB).

### For Windows

1. Open your web browser
2. Go to: **https://github.com/Z-Anatomy/Models-of-human-anatomy**
3. Scroll down and find **"Z-Anatomy.zip"** in the files list
4. Click on **"Z-Anatomy.zip"** to download it
5. Wait for the download to complete (this may take 5-10 minutes)
6. Once downloaded, find the file in your **Downloads** folder

### For Mac

1. Open your web browser
2. Go to: **https://github.com/Z-Anatomy/Models-of-human-anatomy**
3. Click on **"Z-Anatomy.zip"** in the files list
4. The file will download to your **Downloads** folder
5. Wait for it to complete

### Alternative: Download via Command Line

If you know how to use the command line/terminal:

**Windows (PowerShell):**
```powershell
# Download to your Downloads folder
cd $env:USERPROFILE\Downloads
Invoke-WebRequest -Uri "https://github.com/Z-Anatomy/Models-of-human-anatomy/raw/master/Z-Anatomy.zip" -OutFile "Z-Anatomy.zip"
```

**Mac/Linux:**
```bash
# Download to your Downloads folder
cd ~/Downloads
curl -L -o Z-Anatomy.zip "https://github.com/Z-Anatomy/Models-of-human-anatomy/raw/master/Z-Anatomy.zip"
```

---

## Step 4: Find Your Blender Addons Folder

Blender stores addons in a specific folder. Here's how to find it:

### For Windows

1. Open Blender
2. In the top menu, click **Edit** → **Preferences**
3. In the window that opens, click **"File Paths"** on the left sidebar
4. Look for **"Data"** folder path - this is your addons location
5. Usually it's: `C:\Users\[YourName]\AppData\Roaming\Blender\[Version]\scripts\addons\`

**Easier method for Windows:**

1. Press **Windows Key + R** on your keyboard
2. Type: `%APPDATA%\Blender` and press Enter
3. Open the version folder (e.g., `4.5`)
4. Open `scripts` folder
5. Open `addons` folder
6. This is where you'll put the Z-Dissect folder

### For Mac

1. Open Blender
2. In the top menu, click **Blender** → **Preferences**
3. Click **"File Paths"** on the left
4. Look for **"Data"** folder path

**Easier method for Mac:**

1. Open **Finder**
2. Press **Cmd + Shift + G** (Go to folder)
3. Type: `~/Library/Application Support/Blender/`
4. Open the version folder (e.g., `4.5`)
5. Open `scripts` folder
6. Open `addons` folder

### For Linux

1. Open your file manager
2. Press **Ctrl + H** to show hidden files
3. Navigate to: `~/.config/blender/[version]/scripts/addons/`

---

## Step 5: Install Z-Dissect Addon

1. **Copy the Z-Dissect folder** from where you extracted it in Step 2
2. **Paste it** into the `addons` folder you found in Step 4
3. Your addons folder should now contain a folder called `z_dissect` with files like:
   - `__init__.py`
   - `anatomy_data.py`
   - `dissect_ops.py`
   - etc.

### Alternative: Install via Blender (Easier)

1. Open Blender
2. Go to **Edit** → **Preferences** (Windows/Linux) or **Blender** → **Preferences** (Mac)
3. Click **"Add-ons"** on the left sidebar
4. Click **"Install..."** button at the top
5. Navigate to where you extracted the `z_dissect` folder
6. Select the `__init__.py` file inside the `z_dissect` folder
7. Click **"Install Add-on"**
8. Check the box next to **"Z-Dissect"** to enable it

---

## Step 6: Install Z-Anatomy Template (For the 3D Models)

1. Find the `Z-Anatomy.zip` file you downloaded in Step 3
2. Do NOT unzip it - keep it as a ZIP file
3. Copy `Z-Anatomy.zip` to your Blender startup folder:
   - **Windows:** `C:\Users\[YourName]\AppData\Roaming\Blender\[Version]\scripts\startup\`
   - **Mac:** `~/Library/Application Support/Blender/[Version]/scripts/startup/`
   - **Linux:** `~/.config/blender/[Version]/scripts/startup/`

4. If the `startup` folder doesn't exist, create it

### Alternative: Install via Blender Preferences

1. Open Blender
2. Go to **Edit** → **Preferences** (or **Blender** → **Preferences** on Mac)
3. Click **"File Paths"** on the left
4. Find the **"Startup"** path and click the folder icon
5. This opens the startup folder - paste `Z-Anatomy.zip` here

---

## Step 7: Open Z-Anatomy in Blender

1. **Open Blender**
2. In the top menu, click **File** → **New**
3. You should see **"Z-Anatomy"** in the list
4. Click **"Z-Anatomy"**
5. Wait for it to load (this may take 30-60 seconds as it loads all the anatomical models)
6. You should now see a 3D human body model on the screen

### If "Z-Anatomy" doesn't appear in the New menu:

1. Make sure `Z-Anatomy.zip` is in the correct `startup` folder
2. Restart Blender
3. Try again

---

## Step 8: Use Z-Dissect

Now you're ready to use Z-Dissect!

### Opening the Z-Dissect Panel

1. Look at the 3D viewport (the main window showing the 3D model)
2. Press **"N"** on your keyboard
3. A sidebar will appear on the right side
4. Click the **"Z-Dissect"** tab at the top of the sidebar
5. You should see buttons for various dissection tools

### Available Tools

| Tool | What It Does |
|------|-------------|
| **Scalpel** | Draw a cut line on selected anatomy to make dissection cuts |
| **Remove** | Hide the selected anatomical layer |
| **Peel** | Animate peeling away layers |
| **Undo Cut** | Undo the last dissection cut |
| **Reset All** | Show all hidden anatomy |
| **Save State** | Save your current dissection progress |
| **Load State** | Load a previously saved dissection |

### Selecting Anatomy

1. In the Z-Dissect panel, find **"System Browser"**
2. Click the dropdown menu under **"System"**
3. Choose: **Muscular System**, **Skeletal System**, or **Nervous System**
4. Click the dropdown under **"Region"** to pick a body part (Head, Thorax, etc.)
5. Click the dropdown under **"Part"** to pick specific anatomy
6. Click **"Select"** to highlight that structure in the 3D view

### Making a Dissection Cut (Scalpel)

1. Click on the **3D model** to select a body part (e.g., a muscle)
2. In the Z-Dissect panel, click **"Scalpel"**
3. Your cursor will change - now you can draw on the model
4. Click points on the model surface to draw a cut line
5. Press **"Enter"** to execute the cut
6. The model will be split along your line!

### Removing Layers

1. Select a body part by clicking on it
2. In the Z-Dissect panel, click **"Remove"**
3. The selected part will be hidden
4. You can now see what's underneath!

### Saving Your Progress

1. In the Z-Dissect panel, click **"Save State"**
2. Choose where to save the file
3. Give it a name (e.g., "My_Dissection_1")
4. Click **"Save"**
5. Your progress is saved as a `.zdissect` file

### Loading Your Progress

1. In the Z-Dissect panel, click **"Load State"**
2. Find your `.zdissect` file
3. Click **"Open"**
4. Your dissection is restored!

---

## Troubleshooting

### "I don't see Z-Dissect in the sidebar"

1. Make sure you pressed **"N"** to open the sidebar
2. Make sure the Z-Dissect addon is enabled (check Edit → Preferences → Add-ons)
3. Restart Blender

### "The 3D model doesn't load"

1. Make sure `Z-Anatomy.zip` is in the correct `startup` folder
2. Check that your computer has enough RAM (8 GB minimum recommended)
3. Wait longer - large models take time to load

### "I get an error when using Scalpel"

1. Make sure you have a mesh object selected first
2. Click directly on the model surface when drawing the cut line
3. Make sure the object isn't already hidden

### "My computer is slow"

1. Close other applications when using Z-Dissect
2. Use a simpler view mode (toggle with **Z** key)
3. Hide parts of anatomy you're not working on

### "Where do I find my Blender folder?"

**Windows:**
- Press `Win + R`, type `%APPDATA%\Blender`, press Enter

**Mac:**
- In Finder, press `Cmd + Shift + G`, type `~/Library/Application Support/Blender/`

**Linux:**
- Navigate to `~/.config/blender/`

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **N** | Open/close right sidebar |
| **Z** | Change view mode (wireframe, solid, etc.) |
| **Tab** | Switch between Object/Edit mode |
| **A** | Select all / deselect all |
| **H** | Hide selected objects |
| **Alt + H** | Show hidden objects |
| **G** | Grab/move selected object |
| **R** | Rotate selected object |
| **S** | Scale selected object |
| **X** | Delete selected object |
| **Ctrl + Z** | Undo |
| **Ctrl + Shift + Z** | Redo |

---

## Technical Details

### File Structure

```
z_dissect/
├── __init__.py          # Addon registration
├── anatomy_data.py      # Z-Anatomy structure mappings
├── properties.py        # Dissection state properties
├── select.py            # Selection operators
├── dissect_ops.py       # Scalpel, Remove, Peel operators
├── state.py             # Save/Load state
├── ui.py                # Sidebar UI
├── utils.py             # Helper functions
├── test_compatibility.py # Validation script
├── install.py           # Installation helper
└── README.md            # This file
```

### Supported Anatomy Systems

- **Muscular System**: 200+ muscles
- **Skeletal System**: All major bones
- **Nervous System**: Brain, spinal cord, major nerves
- **Cardiovascular System**: Heart, major vessels
- **Visceral Systems**: Internal organs

---

## Download Links

| Resource | URL |
|----------|-----|
| Z-Dissect Addon | https://github.com/sunilchhajwani/z-dissect-blender-addon |
| Z-Anatomy Models | https://github.com/Z-Anatomy/Models-of-human-anatomy |
| Z-Anatomy Addons | https://github.com/Z-Anatomy/Blender-addons |
| Blender (Free) | https://www.blender.org/download/ |

---

## Credits & License

- **Z-Anatomy Models**: [Z-Anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy) by Gauthier Kervyn, Marcin Zielinski, Lluis Vinent
- **BodyParts3D**: Database Center for Life Science
- **License**: CC-BY-SA 4.0 (Free to use, modify, and share with attribution)

---

## Need Help?

- **Issues & Bugs**: [GitHub Issues](https://github.com/sunilchhajwani/z-dissect-blender-addon/issues)
- **Z-Anatomy Project**: [z-anatomy.com](https://www.z-anatomy.com/)
- **Blender Documentation**: [docs.blender.org](https://docs.blender.org/)

---

## Quick Start Checklist

Print this checklist to track your progress:

- [ ] Download and install Blender from blender.org
- [ ] Download Z-Dissect addon from GitHub
- [ ] Download Z-Anatomy.zip (300 MB)
- [ ] Install Z-Dissect addon in Blender
- [ ] Place Z-Anatomy.zip in Blender's startup folder
- [ ] Restart Blender
- [ ] Open Z-Anatomy template (File → New → Z-Anatomy)
- [ ] Press N to open sidebar
- [ ] Click Z-Dissect tab
- [ ] Start exploring anatomy!

---

*Happy dissecting!* 🔬