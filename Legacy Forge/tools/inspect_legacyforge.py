#!/usr/bin/env python3
"""Read-only static inventory for a LegacyForge Android APK.

Usage:
    python3 inspect_legacyforge.py LegacyForge-49.4.apk

This script does not install, patch, sign, contact services, or extract credentials.
It prints ZIP inventory, hashes, ELF metadata, and selected printable-string matches.
"""
from __future__ import annotations
import hashlib
import re
import struct
import sys
import zipfile
from pathlib import Path

KEYWORDS = re.compile(
    rb"(?i)legacyforge|gameapiurl|jointicket|accountdeviceid|"
    rb"accountneedsactivation|discord|serverlist|arkdedicated|"
    rb"downloadstatsby|statdownloadresponse|&port=|"
    rb"main obb|animation pack|download gateway"
)
URL = re.compile(rb"(?i)(?:https?|wss?)://[^\x00-\x20\"'<>]{5,250}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def strings(data: bytes, minimum: int = 5):
    for match in re.finditer(rb"[\x20-\x7e]{" + str(minimum).encode() + rb",}", data):
        yield match.start(), match.group().decode("utf-8", "replace")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 inspect_legacyforge.py APK")
        return 2
    apk = Path(sys.argv[1])
    if not apk.is_file():
        print(f"File not found: {apk}")
        return 2

    print(f"File: {apk.name}")
    print(f"Size: {apk.stat().st_size}")
    print(f"SHA-256: {sha256(apk)}")

    with zipfile.ZipFile(apk) as z:
        entries = z.infolist()
        print(f"ZIP entries: {len(entries)}")
        print("\nDEX / native / game-data entries:")
        for item in entries:
            name = item.filename
            if name.endswith((".dex", ".so", ".obb", ".pak", ".ini", ".json")):
                print(f"{item.file_size:>12}  {name}")

        print("\nRelevant printable strings:")
        for item in entries:
            if not (item.filename.endswith(".dex") or item.filename.endswith(".so")):
                continue
            data = z.read(item)
            hits = [(off, value) for off, value in strings(data) if KEYWORDS.search(value.encode()) or URL.search(value.encode())]
            if hits:
                print(f"\n[{item.filename}]")
                for off, value in hits[:500]:
                    print(f"0x{off:08x}  {value[:500]}")

        print("\nELF shared-library headers:")
        for item in entries:
            if not item.filename.endswith(".so"):
                continue
            data = z.read(item)
            if data[:4] != b"\x7fELF" or len(data) < 20:
                continue
            elf_class = {1: "ELF32", 2: "ELF64"}.get(data[4], "unknown")
            endian = "<" if data[5] == 1 else ">"
            machine = struct.unpack_from(endian + "H", data, 18)[0]
            machine_name = {183: "AArch64", 40: "ARM", 62: "x86_64", 3: "x86"}.get(machine, str(machine))
            print(f"{item.filename}: {elf_class}, {machine_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
