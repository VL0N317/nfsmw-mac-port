# Engineering Roadmap: NFSMW 2005 on Apple Silicon

This document outlines the milestones for achieving a native, hardware-accelerated port of *Need for Speed: Most Wanted (2005)* on Apple Silicon (M1/M2/M3/M4 macOS).

---

## Phase 1: Preparation & Asset Verification
- [x] Document the engine architecture (EAGL3 / QuickSilver).
- [x] Identify calling conventions and memory layout of `speed.exe` v1.3.
- [x] Create an automated asset verification tool (`scripts/check_assets.py`).
- [ ] Dump and extract clean game assets from legally owned media.
- [ ] Confirm asset directory structure and verify case-sensitivity on APFS.

---

## Phase 2: Platform Abstraction Layer (PAL)
Build or adapt the platform layer that will replace Win32 / DirectX:
- [ ] **Windowing & Events:** Implement macOS window lifecycle via SDL3 / Cocoa.
- [ ] **Filesystem VFS:** Implement a case-insensitive virtual file system mapping POSIX paths to the game data directory.
- [ ] **Audio Backend:** Integrate `miniaudio` or `OpenAL Soft` to replace `mss32.dll` calls.
- [ ] **Input Handling:** Map macOS `GameController.framework` (DualSense, Xbox, Switch Pro) and keyboard/mouse to DirectInput 8 callbacks.
- [ ] **Movie Player:** Wrap FFmpeg (`libavcodec`) to decode EA VP6 cutscenes to Metal textures.

---

## Phase 3: Graphics & Rendering Engine
- [ ] Set up **MoltenVK** or native **Metal** device initialization.
- [ ] Port or translate D3D9 vertex and pixel shaders into Metal Shading Language (MSL).
- [ ] Implement the **Visual Treatment** post-processing pipeline:
  - Overbright bloom filter.
  - Sepia/amber color tint.
  - Motion blur velocity buffer.
  - Road specular reflection distortions.
- [ ] Implement Retina display scaling and 16:10 widescreen camera FOV adjustments.

---

## Phase 4: Recompilation & Execution
- [ ] **Option A (Static Recompilation):** Integrate `speed.exe` disassembled functions into AOT-compiled C modules with AAPCS64 calling thunks.
- [ ] **Option B (SpeedBreaker Recompilation):** Compile the Xbox 360 PPC recompiled source tree for macOS ARM64 using Xcode/Clang.
- [ ] Run initial headless simulation test (verifying `TheGameFlowManager` state transitions from `BOOT` to `FRONTEND`).
- [ ] Render main menu and vehicle garage.
- [ ] Stream in world geometry (`TRACKS/STREAML1.BUN`) and execute initial driving physics loop.

---

## Phase 5: Polish & Optimizations
- [ ] Fix any CPU memory alignment stalls on Apple Silicon.
- [ ] Enable 120Hz ProMotion support with frame-time smoothing.
- [ ] Add native macOS menu bar options for resolution, MSAA, and controller remapping.
