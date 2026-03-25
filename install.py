#!/usr/bin/env python3
"""
Z-Dissect Installation Script

This script downloads and installs Z-Anatomy models and companion addons.
Run this from Blender's Script Editor or via command line:

    blender --background --python install.py

Or run directly:
    python3 install.py
"""

import os
import sys
import shutil
import subprocess

# URLs for downloading resources
Z_ANATOMY_URL = "https://github.com/Z-Anatomy/Models-of-human-anatomy/raw/master/Z-Anatomy.zip"
ADDONS_URL = "https://github.com/Z-Anatomy/Blender-addons/archive/refs/heads/main.zip"

def get_blender_dirs():
    """Get Blender's config directories."""
    try:
        import bpy
        user_resources = bpy.utils.resource_path('USER')
        return {
            'addons': os.path.join(user_resources, 'scripts', 'addons'),
            'templates': os.path.join(user_resources, 'scripts', 'startup'),
            'config': os.path.join(user_resources, 'config'),
        }
    except ImportError:
        # Running outside Blender - use default paths
        home = os.path.expanduser('~')
        if sys.platform == 'darwin':  # macOS
            base = os.path.join(home, 'Library', 'Application Support', 'Blender')
        elif sys.platform == 'win32':  # Windows
            base = os.path.join(os.environ.get('APPDATA', home), 'Blender')
        else:  # Linux
            base = os.path.join(home, '.config', 'blender')

        # Find the highest version directory
        blender_versions = sorted([d for d in os.listdir(base) if d.startswith(('3.', '4.', '5.'))], reverse=True)
        version = blender_versions[0] if blender_versions else '4.5'

        return {
            'addons': os.path.join(base, version, 'scripts', 'addons'),
            'templates': os.path.join(base, version, 'scripts', 'startup'),
            'config': os.path.join(base, version, 'config'),
        }


def download_file(url, dest_path):
    """Download a file from URL to destination path."""
    print(f"Downloading: {url}")
    print(f"Destination: {dest_path}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Use curl on macOS/Linux, urllib as fallback
    try:
        subprocess.run(['curl', '-L', '-o', dest_path, url], check=True)
        print("Download complete.")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback to urllib
        import urllib.request
        try:
            urllib.request.urlretrieve(url, dest_path)
            print("Download complete.")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False


def install_template(source_zip, dest_dir):
    """Install Z-Anatomy as a Blender template."""
    os.makedirs(dest_dir, exist_ok=True)

    template_name = os.path.basename(source_zip)
    dest_path = os.path.join(dest_dir, template_name)

    if os.path.exists(dest_path):
        print(f"Template already installed: {dest_path}")
        return False

    shutil.copy2(source_zip, dest_path)
    print(f"Installed template: {dest_path}")
    return True


def install_addon(source_dir, dest_dir):
    """Install Z-Dissect addon."""
    addon_name = os.path.basename(source_dir)
    dest_path = os.path.join(dest_dir, addon_name)

    if os.path.exists(dest_path):
        print(f"Addon already installed: {dest_path}")
        # Update files
        shutil.rmtree(dest_path)

    shutil.copytree(source_dir, dest_path)
    print(f"Installed addon: {dest_path}")
    return True


def download_z_anatomy(dest_dir):
    """Download Z-Anatomy template."""
    dest_path = os.path.join(dest_dir, "Z-Anatomy.zip")
    if os.path.exists(dest_path):
        print(f"Z-Anatomy already downloaded: {dest_path}")
        return dest_path

    return dest_path if download_file(Z_ANATOMY_URL, dest_path) else None


def download_addons(dest_dir):
    """Download Z-Anatomy companion addons."""
    dest_path = os.path.join(dest_dir, "addons.zip")
    if os.path.exists(dest_path):
        print(f"Addons already downloaded: {dest_path}")
        return dest_path

    return dest_path if download_file(ADDONS_URL, dest_path) else None


def main():
    """Main installation process."""
    print("=" * 60)
    print("Z-Dissect Installation Script")
    print("=" * 60)

    dirs = get_blender_dirs()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Download Z-Anatomy
    print("\n[Step 1] Downloading Z-Anatomy template...")
    template_zip = download_z_anatomy(dirs['templates'])
    if template_zip:
        print("Z-Anatomy template ready.")
    else:
        print("ERROR: Failed to download Z-Anatomy template")
        print(f"Please download manually from: {Z_ANATOMY_URL}")

    # Step 2: Download Addons
    print("\n[Step 2] Downloading Z-Anatomy companion addons...")
    addons_zip = download_addons(dirs['config'])
    if addons_zip:
        print("Z-Anatomy addons ready.")
    else:
        print("ERROR: Failed to download addons")
        print(f"Please download manually from: {ADDONS_URL}")

    # Step 3: Install Z-Dissect addon
    print("\n[Step 3] Installing Z-Dissect addon...")
    install_addon(script_dir, dirs['addons'])

    print("\n" + "=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart Blender")
    print("2. Go to Edit → Preferences → Add-ons")
    print("3. Enable 'Z-Dissect' and 'Z-Anatomy' addons")
    print("4. File → New → Z-Anatomy to load the anatomical models")
    print("5. Press 'N' to open the sidebar → Z-Dissect tab")


if __name__ == "__main__":
    main()