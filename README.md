# Need for Speed: Most Wanted (2005) - Apple Silicon Native Port & Architecture Guide

An engineering roadmap, architectural reverse-engineering documentation, and porting blueprint for bringing **Need for Speed: Most Wanted (2005)** natively to **macOS on Apple Silicon (M1/M2/M3/M4 ARM64)**.

---

## 🎯 Executive Summary & Feasibility

Can *Need for Speed: Most Wanted (2005)* be ported natively to Apple Silicon? **Yes.**

The game originally ran on two primary architectures:
1. **32-bit x86 Little-Endian (PC Windows)** running DirectX 9.0c.
2. **64-bit PowerPC Big-Endian (Xbox 360 / GameCube / PS2)** running custom console graphics APIs.

On Apple Silicon (ARM64 macOS), there are two distinct paths forward:

| Route | Source Binary | Status & Technology | Visual Fidelity |
| :--- | :--- | :--- | :--- |
| **Path 1: Xbox 360 Static Recompilation (`SpeedBreaker`)** | Xbox 360 (`default.xex`) | **Functional & Native on macOS** via [SpeedBreaker](https://github.com/SpeedBreakerProject/speedbreaker). AOT translates PowerPC to native ARM64 with Metal/MoltenVK graphics. | Definitive console graphics (4K 60FPS, enhanced HDR lighting, detailed road shaders). |
| **Path 2: PC Static Recompilation (`nfsmwpc-recompiled`)** | PC Windows (`speed.exe` v1.3) | **In Active Development** via static x86-to-C recompilation (e.g. `codepdbh/nfsmwpc-recompiled`), bridging D3D9 via Vulkan (MoltenVK) and SDL2/3. | Classic PC visual style, full mod compatibility, and lighter footprint. |
| **Path 3: Clean-Room C++ Decompilation** | Multiplatform binaries | **Long-term Community Effort** via `dbalatoni13/nfsmw` (matching C++ decompilation). | True human-readable C++ source code. |

---

## 📂 Repository Contents

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) – Subsystem breakdown of EA's EAGL3 engine, memory layout, game loop, and physics.
- [`docs/REVERSE_ENGINEERING.md`](docs/REVERSE_ENGINEERING.md) – Disassembly guide for `speed.exe`, calling conventions, SafeDisc DRM bypass, and symbol mapping.
- [`docs/APPLE_SILICON_PORTING.md`](docs/APPLE_SILICON_PORTING.md) – Technical guide on ARM64 translation, Metal/MoltenVK rendering, audio replacement, and APFS case sensitivity.
- [`docs/ASSET_EXTRACTION.md`](docs/ASSET_EXTRACTION.md) – How to extract assets legally from the original PC CD/DVD or Xbox 360 disc on macOS.
- [`scripts/check_assets.py`](scripts/check_assets.py) – Asset validation tool to check game file integrity and case-sensitivity issues on macOS.

---

## 🚀 Quick Setup for Apple Silicon (M1 Pro MBP)

### Requirements
- **macOS:** macOS 14 Sonoma or macOS 15 Sequoia (recommended)
- **Hardware:** Apple Silicon (M1 Pro, M1 Max, M2, M3, etc.)
- **Xcode Command Line Tools:** `xcode-select --install`
- **Homebrew:** `brew install sdl2 sdl3 moltenvk ffmpeg cmake ninja`
- **Legally Owned Game Copy:** Original PC CD/DVD or Xbox 360 disc dump.

---

## 📜 Legal & Preservation Disclaimer
This documentation and accompanying tools are created strictly for **reverse engineering, educational research, software preservation, and interoperability** under fair use. No proprietary assets, copyrighted binaries, textures, or audio from Electronic Arts or EA Black Box are included in this repository. Users must supply their own legally purchased copy of *Need for Speed: Most Wanted (2005)*.
