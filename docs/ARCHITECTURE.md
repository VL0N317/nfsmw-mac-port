# Architecture & Engine Internals: Need for Speed: Most Wanted (2005)

## 1. Engine Overview: EAGL3 / QuickSilver

*Need for Speed: Most Wanted (2005)* was developed by **EA Black Box** using the proprietary **EAGL3** (EA Graphics Library version 3) engine, colloquially referred to inside debug strings as **QuickSilver**.

The engine architecture follows a modular, object-oriented design written in C++ (compiled originally with MSVC 7.1 / Visual Studio .NET 2003 on Windows, CodeWarrior on GameCube/PS2, and the Xbox 360 SDK compiler).

```
                      +-----------------------------+
                      |       TheGameFlowManager    |
                      |   (Main Loop & State FSM)   |
                      +--------------+--------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
+--------v--------+         +--------v--------+         +--------v--------+
|   Simulation    |         |    Rendering    |         |   Audio & VFS   |
|     (GSim)      |         |     (eagl3)     |         |    (EA Sound)   |
+--------+--------+         +--------+--------+         +--------+--------+
         |                           |                           |
  - Sim::Vehicle              - D3D9 Device               - Miles Sound Sys
  - Collision Engine          - Shader Manager            - EA Trax Dynamic
  - AI Pursuit Manager        - Visual Treatment (Bloom)  - BigFile Loader
  - SpeedBreaker Time Scale   - World Streaming           - VP6 Movie Playback
```

---

## 2. Windows Executable (`speed.exe`) Structure

- **Base Address:** `0x00400000`
- **Original Subsystem:** Windows GUI (32-bit x86 PE)
- **Compilation Toolchain:** Microsoft Visual C++ 7.1 (2003)
- **Calling Conventions:**
  - Member functions: `__thiscall` (ECX holds `this` pointer)
  - Engine callbacks / utilities: `__cdecl`
  - Windows API / COM interop: `__stdcall`
- **Target Version for Recompilation:** **Patch v1.3 English (`speed.exe`, size ~5.8 MB or 6.8 MB uncompressed)**.
  > **Note:** The v1.3 executable has the standard memory layout targeted by the modding SDKs (e.g., `NFSPluginSDK` and ThirteenAG's `WidescreenFix`).

---

## 3. Core Engine Subsystems

### A. The Game Flow Manager (`TheGameFlowManager`)
Controls top-level game states using a finite state machine:
- `STATE_BOOT` (`0x0`): Hardware detection, memory pool allocations.
- `STATE_FRONTEND` (`0x3`): Main menu, Blacklist 15 menu, car customization, rap sheet.
- `STATE_LOADING` (`0x4`): Parsing `.BUN` track files, instantiating car models, loading textures into VRAM.
- `STATE_GAMEPLAY` (`0x6`): Active racing or free-roam police pursuit.

### B. Simulation & Vehicle Physics (`GSim`)
- **Vehicle Dynamics:** Calculated at a fixed step (typically 60 Hz or 100 Hz simulation ticks).
- **Speedbreaker Time Dilation:** Modifies the global simulation delta time (`Sim::Clock`), scaling down vehicle velocities and player reaction physics while boosting steering authority and car mass (preventing rollover during high-speed turns).
- **Damage Model:** Purely cosmetic in free-roam/races, but structural damage models apply to police cruisers and destructible pursuit breakers (water towers, gas station canopies).

### C. Police AI & Pursuit Mechanics
- **Heat Levels (1 to 5, +6 in Challenge Series):** Dictates spawn frequencies, squad tactics, and pursuit vehicle classes (Civilian Cruisers → City Undercover → State Monaro/GTO → Federal Corvettes → Rhino SUVs).
- **Tactical Roles:**
  - Box-in / Pit maneuvers.
  - Rolling roadblocks and static spike strips.
  - Police Helicopter (`AIHelicopter`): Disorients the player with downdraft physics and reports player positions through cooldown periods.

### D. Rendering Pipeline & Shaders
- **Render Engine:** Direct3D 9 with Fixed Function + early programmable vertex/pixel shaders.
- **The "Visual Treatment":** The defining aesthetic of NFSMW 2005. It consists of:
  - High dynamic bloom / over-exposure pass.
  - Sepia / amber color tint matrix multiplication.
  - Motion blur (velocity buffer based on camera matrix).
  - Wet asphalt specular reflection maps with real-time road distortion.

### E. Audio Subsystem (EA Sound & Miles Sound System)
- **Engine Sounds:** Granular synthesis using recorded RPM audio loops.
- **Interactive Soundtrack (EA Trax):** Dynamically crossfades between ambient rock/electronic stems and high-intensity pursuit themes when police are actively chasing.
- **Police Radio Scanner:** Procedural speech concatenation linking unit IDs, street names, and action verbs (`"Suspect spotted eastbound on Rosewood..."`).

### F. File System & BigFile Archives (`.BUN`, `.BIN`, `.VIV`)
- Files are bundled into monolithic streaming chunks to minimize seek times on 2005 optical drives:
  - `GLOBAL/GLOBALB.BUN`: Shared geometry, core UI fonts, particle effects.
  - `TRACKS/STREAM*.BUN`: City chunks and road geometry streamed dynamically based on player position.
  - `CARS/<CAR_NAME>/GEOMETRY.BIN` & `TEXTURES.BIN`: 3D car models, level of detail (LOD0 to LOD4), and vinyl skins.
