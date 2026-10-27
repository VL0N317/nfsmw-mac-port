# Game Asset Extraction & Preparation Guide

To run or build any native port or recompilation of *Need for Speed: Most Wanted (2005)*, you must supply the original asset files from your legally purchased copy.

---

## 1. Physical PC CD/DVD Extraction on macOS

Since the **M1 Pro MacBook Pro** does not have an internal optical drive, you have two options:

### Option A: Using an External USB DVD/CD Drive
1. Connect the USB drive to your Mac (via a USB-C adapter/hub).
2. Insert **Disc 1** (of the 4-CD set or the 1-DVD Black Edition).
3. Open Terminal and create an ISO image of each disc using `hdiutil`:
   ```bash
   # List connected disk drives
   diskutil list

   # Unmount the disc before dumping (replace disk2 with your drive ID)
   diskutil unmountDisk /dev/disk2

   # Create a raw ISO backup
   sudo dd if=/dev/rdisk2 of=~/NFSMW_Disc1.iso bs=2048 status=progress
   ```
4. Repeat for Discs 2, 3, and 4 (if using the 4-CD edition).

### Option B: Using an Existing Windows PC or Pre-Installed Folder
If you have access to a Windows PC:
1. Install the game normally using your CD key.
2. Apply the **official EA v1.3 Patch**.
3. Copy the installed `Need for Speed Most Wanted` directory directly to your Mac using a USB flash drive, external SSD, or local network file sharing.

---

## 2. Directory Structure Verification

Ensure your game directory contains the following critical folders and files:

```text
Need for Speed Most Wanted/
├── CARS/             # 3D car models (GEOMETRY.BIN, TEXTURES.BIN, VINYLS.BIN)
├── FRONTEND/         # UI assets, menus, Blacklist portraits, cursors
├── GLOBAL/           # GLOBALB.BUN, GLOBALB.LZC (core fonts, shaders, particles)
├── LANGUAGES/        # Text localization files (English.bin, etc.)
├── MOVIES/           # Live-action FMV cutscenes (e.g. 01_intro.vp6, mia.vp6)
├── SOUND/            # Engine audio banks, speech, and EA Trax music files
│   ├── CARS/         # Engine RPM loops and exhaust notes
│   ├── SPEECH/       # Police radio chatter audio banks
│   └── TRACKS/       # Interactive music banks
├── TRACKS/           # City streaming chunks (STREAML1.BUN, STREAML2.BUN, etc.)
└── speed.exe         # Executable (Patch v1.3 unencrypted / No-CD)
```

---

## 3. Why the v1.3 Patch is Mandatory

1. **Bug Fixes:** Fixes several memory leaks and multiplayer packet crashes present in the v1.0 release.
2. **Standard Community Baseline:** All decompilation projects, memory offset SDKs (`NFSPluginSDK`), and static recompilation tools specifically target the **v1.3 English** executable offsets.
3. **SafeDisc Elimination:** The official v1.0 CD binary contains SafeDisc v4 encryption that cannot be disassembled or recompiled on Apple Silicon. The v1.3 unencrypted binary is required.
