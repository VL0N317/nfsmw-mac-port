# Apple Silicon (M1 Pro) Porting & Platform Abstraction

Bringing a 2005 Windows game natively to Apple Silicon requires replacing all Win32 / DirectX APIs with modern POSIX, Metal, and macOS frameworks.

---

## 1. Why Apple Silicon M1 Pro is an Ideal Target

1. **Little-Endian Architecture:**
   - Both x86 (PC) and ARM64 (Apple Silicon) are **little-endian**.
   - Unlike porting from PowerPC (Xbox 360/GameCube), bytes do **not** need to be flipped when reading binary game assets (`.BUN`, `.BIN`, textures, geometry).
2. **Massive GPU Headroom:**
   - The original game targeted 2005 GPUs (e.g. NVIDIA GeForce 6800 GT, ATI Radeon X800) with ~30-60 GFLOPS.
   - The M1 Pro GPU delivers **~5,200 GFLOPS (5.2 TFLOPS)**, providing more than enough power to render at **native Retina resolutions (up to 4K) at a locked 60 or 120 FPS (ProMotion)**.

---

## 2. API Translation Matrix

| Windows / 2005 PC Component | Original Library | Modern macOS / Apple Silicon Replacement |
| :--- | :--- | :--- |
| **Window & Events** | Win32 API (`CreateWindowEx`, `HWND`) | **SDL3 / SDL2** or native Cocoa / AppKit |
| **Graphics API** | Direct3D 9.0c | **Metal** (direct) or **Vulkan via MoltenVK** (`dxvk-native`) |
| **Shader Language** | HLSL / D3D9 Shader Model 2.0/3.0 | **Metal Shading Language (MSL)** via **SPIRV-Cross** |
| **Audio Pipeline** | Miles Sound System (`mss32.dll`) | **miniaudio** / **FAudio** / **OpenAL Soft** |
| **Input Handling** | DirectInput 8 (`dinput8.dll`) | **SDL3 GameController** / Apple **GameController.framework** |
| **Video Playback** | Electronic Arts VP6 (`.vp6`) | **FFmpeg (`libavcodec`)** |
| **File Paths & VFS** | Win32 paths with backslashes (`\`) | **Case-Insensitive VFS Shim** with POSIX forward slashes |

---

## 3. Graphics & Shaders on macOS

### Option A: `dxvk-native` + MoltenVK (Fastest Route)
- `dxvk-native` is a source-level port of DXVK that translates Direct3D 9 calls into Vulkan calls without Wine.
- On macOS, Vulkan calls are translated to native Metal commands via **MoltenVK**.
- Supports original D3D9 blend modes, render states, and depth buffers natively.

### Option B: Native Metal Shaders
- Original HLSL shaders extracted from `GLOBAL/GLOBALB.BUN` can be converted:
  `HLSL -> DXC / glslang -> SPIR-V -> SPIRV-Cross -> Metal Shading Language (.metal)`
- Custom passes for the NFSMW **Visual Treatment**:
  - Full-screen quad pass applying luminance threshold, Gaussian blur, and color grading matrix.

---

## 4. Input & Modern Controller Support

The original 2005 PC release only supported DirectInput 8 (which lacked modern trigger rumble, deadzone calibration, and proper analog trigger travel).

### Sony DualShock 4 (PS4) Mapping on Apple Silicon
The DualShock 4 is natively supported out of the box by macOS (`GameController.framework`) with full vibration/rumble support over both Bluetooth and USB:

```
                [ L2: Progressive Brake ]           [ R2: Progressive Throttle ]
                [ L1: Clutch / Action   ]           [ R1: Reset Car            ]
                      \                                   /
            [ D-Pad ]  \                                 /  [ Triangle: Change Camera ]
     Up: Engage Pursuit \                               /   [ Square: Look Back      ]
   Down: Speedbreaker    +-----------------------------+    [ Circle: Nitrous (NOS)  ]
                          |  [SHARE]   [Touch]  [OPT]  |    [ Cross: E-Brake / Enter ]
                          |                            |
                          |    (L3)            (R3)    |
                          |  Steering      Speedbreaker|
                          +----------------------------+
```

#### How to Pair DualShock 4 to macOS:
1. Turn off the controller.
2. Hold down the **PS Button + SHARE Button** simultaneously for ~3 seconds until the light bar blinks rapidly in white (pairing mode).
3. Open **System Settings → Bluetooth** on your Mac and click **Connect** next to *"DUALSHOCK 4 Wireless Controller"*.
4. Launch SpeedBreaker — it will detect the controller immediately with analog triggers and haptic rumble enabled.

---

## 5. File System & APFS Compatibility

### Case Sensitivity:
- In Windows, `global\globalb.bun` and `GLOBAL\GLOBALB.BUN` are identical.
- While APFS is formatted as case-insensitive by default on most macOS user drives, game scripts often mismatch casing.
- **VFS Implementation:** A lightweight wrapper intercepts file open calls (`fopen`, `CreateFileA`) and scans the target directory to resolve casing dynamically.

### Path Separators:
- Replace all Windows backslashes (`\`) with POSIX forward slashes (`/`).
