# Reverse Engineering & Decompilation Guide for NFSMW (2005)

## 1. Disassembly Target & DRM Removal

The retail PC disc of *Need for Speed: Most Wanted (2005)* shipped with **Macrovision SafeDisc v4** copy protection.

### Why the Retail CD `.exe` Cannot Be Directly Analyzed:
1. **Encrypted PE Sections:** The code section (`.text`) is encrypted on disk and only decrypted at runtime by a ring-0 Windows kernel driver (`secdrv.sys`).
2. **Incompatible with Modern Systems:** `secdrv.sys` has been permanently disabled on modern Windows (Vista/7/8/10/11) and does not exist on macOS/Linux.
3. **Anti-Debugging & Nano-Code:** SafeDisc injects obfuscated exception handlers to detect disassemblers (IDA, Ghidra, x64dbg).

### The Solution:
- Use the **English v1.3 No-CD Executable** (standard patch version across the entire modding and reverse-engineering community).
- This binary has stripped SafeDisc wrappers, leaving standard unencrypted PE x86 code accessible in Ghidra and IDA Pro.

---

## 2. Tooling & Symbol Mapping

### Recommended Analysis Tools:
- **Ghidra** (NSA Open Source Reverse Engineering Suite): Excellent for automated struct definition and decompilation.
- **IDA Pro / IDA Free**: Gold standard for x86 disassembling.
- **NFSPluginSDK** ([berkayylmao/NFSPluginSDK](https://github.com/berkayylmao/NFSPluginSDK)):
  - Contains reverse-engineered C++ headers for Most Wanted 2005.
  - Maps internal classes: `Sim::Vehicle`, `Physics::RigidBody`, `TheGameFlowManager`, `FeManager`, `GRaceStatus`.

### Cross-Referencing Console Builds:
One of the most effective techniques in NFS reverse engineering is **cross-referencing with the Nintendo GameCube and Xbox 360 debug builds**:
- The GameCube version was compiled with Metrowerks CodeWarrior with dwarf debug information or partial string tables left intact.
- Function names, variable layouts, and internal debug assertions (e.g., `ASSERT(pVehicle != NULL)`) provide the exact source names used by the original EA Black Box team.

---

## 3. Static Recompilation (AOT Binary Translation)

Rather than manually rewriting 500,000+ lines of assembly into clean C++, modern recompilation projects use **Static Ahead-Of-Time (AOT) Binary Translation**.

```
  +-------------------------+
  |    speed.exe (x86 32)   |
  +------------+------------+
               |
               v
  +-------------------------+
  |    x86 Disassembler     |  (Capstone / LLVM / Custom Parser)
  +------------+------------+
               |
               v
  +-------------------------+
  |    Intermediate IR      |  (Translates x86 opcodes & flags to C code)
  +------------+------------+
               |
               v
  +-------------------------+
  |    Recompiled C/C++     |  (Outputs compilable source code)
  +------------+------------+
               |
               v
  +-------------------------+
  |   Clang (ARM64 Target)  |  (Compiles natively for Apple Silicon)
  +-------------------------+
```

### Key Technical Challenges in Static Recompilation:

#### 1. Calling Convention Thunks:
- MSVC x86 32-bit uses `__thiscall` (the `this` pointer is passed in register `ECX`, remaining parameters pushed on the stack right-to-left).
- Apple Silicon uses the **ARM64 AAPCS standard** (arguments in `X0-X7`, return values in `X0-X1`).
- The recompiler must generate ABI thunks to bridge function calls cleanly without corrupting the register state.

#### 2. x86 EFLAGS Emulation:
- Instructions in x86 frequently rely on arithmetic condition flags (Carry, Zero, Sign, Overflow, Parity).
- Native AOT recompiler code must emulate flag calculations either lazily or via bitwise logic in C.

#### 3. 32-bit Address Space Virtualization:
- The 2005 engine expects pointers to fit in 32 bits (`uint32_t`).
- On a 64-bit operating system (like macOS on Apple Silicon), pointers are 64 bits (`uint64_t`).
- **Solution:** Reserve a 4GB contiguous virtual memory region using `mmap()` (MAP_32BIT or base pointer offsetting) so all internal 32-bit game pointers can be dereferenced safely.
