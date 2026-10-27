#!/usr/bin/env python3
"""
Asset Verification & Integrity Checker for NFSMW (2005)
Checks whether an asset directory contains all required core files for a native port.
"""

import os
import sys
from pathlib import Path

REQUIRED_DIRECTORIES = [
    "CARS",
    "FRONTEND",
    "GLOBAL",
    "MOVIES",
    "SOUND",
    "TRACKS"
]

ESSENTIAL_FILES = [
    "GLOBAL/GLOBALB.BUN",
    "FRONTEND/FRONTEND.BIN",
    "SOUND/PFIFO.BIG",
    "TRACKS/STREAML1.BUN",
    "CARS/BMWGTR/GEOMETRY.BIN"
]

def verify_assets(game_dir: Path):
    print(f"[*] Checking NFSMW assets in: {game_dir}")
    
    if not game_dir.exists() or not game_dir.is_dir():
        print(f"[!] Error: Directory '{game_dir}' does not exist.")
        return False

    missing_dirs = []
    for d in REQUIRED_DIRECTORIES:
        p = game_dir / d
        if not p.exists() or not p.is_dir():
            missing_dirs.append(d)

    if missing_dirs:
        print(f"[-] Missing required directories: {', '.join(missing_dirs)}")
    else:
        print("[+] All core directories present.")

    missing_files = []
    for f in ESSENTIAL_FILES:
        p = game_dir / f
        if not p.exists():
            # Check case-insensitive fallback
            parts = f.split('/')
            cur = game_dir
            found = True
            for part in parts:
                matched = [entry for entry in os.listdir(cur) if entry.lower() == part.lower()]
                if matched:
                    cur = cur / matched[0]
                else:
                    found = False
                    break
            if not found:
                missing_files.append(f)
            else:
                print(f"  [i] Notice: File casing mismatch detected for '{f}' -> '{cur.relative_to(game_dir)}'")

    if missing_files:
        print(f"[-] Missing essential files: {missing_files}")
    else:
        print("[+] All critical test files verified!")

    # Check executable
    exe_candidates = ["speed.exe", "SPEED.EXE"]
    exe_found = any((game_dir / exe).exists() for exe in exe_candidates)
    if exe_found:
        print("[+] Found speed.exe executable.")
    else:
        print("[!] Warning: speed.exe not found in root game folder.")

    return len(missing_dirs) == 0 and len(missing_files) == 0

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    success = verify_assets(target)
    sys.exit(0 if success else 1)
