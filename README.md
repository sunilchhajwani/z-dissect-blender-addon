# Z-Dissect - Anatomical Dissection Simulator for Blender

A Blender addon for interactive anatomical dissection simulation, integrated with Z-Anatomy 3D models.

**Perfect for medical students, anatomy educators, and anyone interested in human anatomy.**

---

## What You Can Do

- ✅ Explore 3D human anatomy (muscles, bones, nerves)
- ✅ Make virtual dissection cuts on anatomical models
- ✅ Remove layers to see what's underneath
- ✅ Animate peeling of anatomical structures
- ✅ Save and restore your dissection progress

---

## Complete Setup Guide

### What You'll Need

- A computer (Windows, Mac, or Linux)
- Internet connection
- At least 10 GB of free disk space
- A mouse (recommended)

---

## Step 1: Install Blender

Blender is the free 3D software that runs Z-Dissect.

### For Windows

1. Open your web browser
2. Go to: **https://www.blender.org/download/**
3. Click the **"Download Blender"** button
4. Wait for the file to download (about 300 MB)
5. Open your **Downloads** folder
6. Double-click the downloaded file
7. Click **"Next"** through all screens
8. Click **"Install"** and wait
9. Click **"Finish"**
10. Open Blender from your Start menu to verify it works

### For Mac

1. Open your web browser
2. Go to: **https://www.blender.org/download/**
3. Click the **"Download Blender"** button
4. Open your **Downloads** folder
5. Drag **Blender.app** to your **Applications** folder
6. Open Blender from Applications to verify it works

### For Linux

1. Open your web browser
2. Go to: **https://www.blender.org/download/**
3. Download the version for your distribution
4. Install using your package manager or extract the archive

---

## Step 2: Download Z-Dissect Addon

### Easy Method (Recommended)

1. Open your web browser
2. Go to: **https://github.com/sunilchhajwani/z-dissect-blender-addon**
3. Click the green **"Code"** button (top right)
4. Click **"Download ZIP"**
5. Save the file to your computer
6. Right-click the ZIP file and select **"Extract All"** (Windows) or double-click to extract (Mac)
7. Remember where you extracted the folder

### For Developers

If you know how to use Git:

```bash
git clone https://github.com/sunilchhajwani/z-dissect-blender-addon.git
```

---

## Step 3: Download Z-Anatomy 3D Models

The Z-Anatomy models contain the actual 3D human anatomy. This is a large file (about 300 MB).

### Download Steps

1. Open your web browser
2. Go to: **https://github.com/Z-Anatomy/Models-of-human-anatomy**
3. Scroll down and click on **"Z-Anatomy.zip"**
4. Wait for the download to complete (5-10 minutes depending on your internet)
5. The file will be in your **Downloads** folder
6. **Do NOT unzip this file** - keep it as a ZIP

---

## Step 4: Find Your Blender Addons Folder

### For Windows

1. Press **Windows Key + R** on your keyboard
2. Type: `%APPDATA%\Blender` and press Enter
3. Open the version folder (e.g., `4.5`)
4. Open the `scripts` folder
5. Open the `addons` folder
6. **This is your addons folder**

**If the folders don't exist, create them.**

### For Mac

1. Open **Finder**
2. Press **Cmd + Shift + G** (Go to folder)
3. Type: `~/Library/Application Support/Blender/`
4. Open the version folder (e.g., `4.5`)
5. Open the `scripts` folder
6. Open the `addons` folder
7. **This is your addons folder**

**If the folders don't exist, create them.**

### For Linux

1. Open your file manager
2. Press **Ctrl + H** to show hidden files
3. Navigate to: `~/.config/blender/[version]/scripts/addons/`
4. **This is your addons folder**

---

## Step 5: Install Z-Dissect

### Method 1: Copy to Addons Folder

1. Find the `z_dissect` folder from Step 2
2. Copy the entire `z_dissect` folder
3. Paste it into your **addons folder** (from Step 4)
4. The addons folder should now contain: `z_dissect/__init__.py` and other files

### Method 2: Install via Blender (Alternative)

1. Open Blender
2. Go to **Edit → Preferences** (Windows/Linux) or **Blender → Preferences** (Mac)
3. Click **"Add-ons"** on the left sidebar
4. Click **"Install..."** at the top
5. Navigate to the `z_dissect` folder
6. Select `__init__.py`
7. Click **"Install Add-on"**
8. Check the box next to **"Z-Dissect"** to enable it

---

## Step 6: Install Z-Anatomy Models

1. Find the `Z-Anatomy.zip` file you downloaded in Step 3
2. **Keep it as a ZIP file** (do not unzip)
3. Copy `Z-Anatomy.zip` to your **startup folder**:
   - **Windows:** `%APPDATA%\Blender\[version]\scripts\startup\`
   - **Mac:** `~/Library/Application Support/Blender/[version]/scripts/startup/`
   - **Linux:** `~/.config/blender/[version]/scripts/startup/`

**If the `startup` folder doesn't exist, create it.**

---

## Step 7: Open Z-Anatomy in Blender

1. **Open Blender**
2. Click **File → New** in the top menu
3. You should see **"Z-Anatomy"** in the list
4. Click **"Z-Anatomy"**
5. Wait for it to load (30-60 seconds)
6. You should see a 3D human body on the screen

### If "Z-Anatomy" Doesn't Appear

1. Make sure `Z-Anatomy.zip` is in the correct `startup` folder
2. Close and restart Blender
3. Try again

---

## Step 8: Use Z-Dissect

### Opening the Z-Dissect Panel

1. Look at the 3D viewport (main window)
2. Press **"N"** on your keyboard
3. A sidebar opens on the right
4. Click the **"Z-Dissect"** tab at the top

### Available Tools

| Button | What It Does |
|--------|-------------|
| **Scalpel** | Draw a cut line on anatomy to make dissection cuts |
| **Remove** | Hide the selected body part |
| **Peel** | Animate peeling away layers |
| **Undo Cut** | Undo the last dissection |
| **Reset All** | Show all hidden parts |
| **Save State** | Save your progress |
| **Load State** | Load a saved dissection |

### Selecting Body Parts

1. In the Z-Dissect panel, find **"System Browser"**
2. Choose a **System** (Muscular, Skeletal, Nervous)
3. Choose a **Region** (Head, Thorax, etc.)
4. Choose a **Part** (specific muscle/bone)
5. Click **"Select"** to highlight it

### Making a Dissection Cut

1. Click on the **3D model** to select a body part
2. Click **"Scalpel"** in the Z-Dissect panel
3. Draw on the model by clicking points
4. Press **"Enter"** to make the cut

### Removing Layers

1. Click on a body part to select it
2. Click **"Remove"**
3. The part is hidden, showing what's underneath

### Saving Your Progress

1. Click **"Save State"**
2. Choose where to save
3. Give it a name
4. Click **"Save"**

### Restoring Progress

1. Click **"Load State"**
2. Find your saved file
3. Click **"Open"**

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **N** | Open/close sidebar |
| **Z** | Change view mode |
| **H** | Hide selected |
| **Alt + H** | Show hidden |
| **G** | Move object |
| **R** | Rotate object |
| **S** | Scale object |
| **X** | Delete |
| **Ctrl + Z** | Undo |

---

## Troubleshooting

### "I don't see Z-Dissect in the sidebar"

- Press **"N"** to open the sidebar
- Make sure the addon is enabled (Edit → Preferences → Add-ons)
- Restart Blender

### "The 3D model doesn't load"

- Make sure `Z-Anatomy.zip` is in the `startup` folder
- Check you have enough RAM (8 GB minimum)
- Wait longer for large models to load

### "Scalpel doesn't work"

- Select a body part first by clicking on it
- Make sure you're drawing on the model surface
- The object shouldn't be hidden

### "My computer is slow"

- Close other applications
- Press **Z** and choose **Wireframe** for faster view
- Hide parts you're not working on

### "Where's my Blender folder?"

| System | Path |
|--------|------|
| **Windows** | Press Win+R, type `%APPDATA%\Blender` |
| **Mac** | Cmd+Shift+G, type `~/Library/Application Support/Blender/` |
| **Linux** | Go to `~/.config/blender/` |

---

## Quick Start Checklist

Print this to track your progress:

- [ ] Download and install Blender
- [ ] Download Z-Dissect addon
- [ ] Download Z-Anatomy.zip (300 MB)
- [ ] Install Z-Dissect addon
- [ ] Place Z-Anatomy.zip in startup folder
- [ ] Restart Blender
- [ ] Open Z-Anatomy template
- [ ] Press N for sidebar
- [ ] Click Z-Dissect tab
- [ ] Start dissecting!

---

## Download Links

| What | Where |
|------|-------|
| Z-Dissect Addon | https://github.com/sunilchhajwani/z-dissect-blender-addon |
| Z-Anatomy Models | https://github.com/Z-Anatomy/Models-of-human-anatomy |
| Blender (Free) | https://www.blender.org/download/ |

---

## Need Help?

- **Report Issues:** [GitHub Issues](https://github.com/sunilchhajwani/z-dissect-blender-addon/issues)
- **Z-Anatomy Website:** [z-anatomy.com](https://www.z-anatomy.com/)
- **Blender Help:** [docs.blender.org](https://docs.blender.org/)

---

## Credits

- **Z-Anatomy Models:** Gauthier Kervyn, Marcin Zielinski, Lluis Vinent
- **BodyParts3D:** Database Center for Life Science
- **License:** CC-BY-SA 4.0 (Free to use with attribution)

---

**For technical documentation, see [DEVELOPERS.md](DEVELOPERS.md)**