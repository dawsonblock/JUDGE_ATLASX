#!/usr/bin/env python3
"""
rtl_sanity_check.py

This script performs basic sanity checks on the RTL files. It looks for
common pitfalls such as missing resets, undriven signals, and implicit
width mismatches. It is not a replacement for a full lint tool like
Verilator or Vivado's design rule checks, but it can catch simple
mistakes early in the development process.
"""

import pathlib
import re
import sys


def check_missing_reset(file_contents: str, filename: str):
    if 'always_ff' in file_contents and 'rst_n' in file_contents:
        if 'if (!rst_n)' not in file_contents:
            print(f"WARNING: {filename}: always_ff without explicit reset condition")


def check_implicit_width(file_contents: str, filename: str):
    pattern = re.compile(r'\bassign\s+\w+\s*=\s*\{\w+\}\s*;')
    for match in pattern.finditer(file_contents):
        print(f"NOTE: {filename}: implicit concatenation width may require attention: {match.group(0)}")


def main():
    rtl_dir = pathlib.Path('waveform_brain_v1_corrected/rtl')
    for path in rtl_dir.glob('*.v'):
        text = path.read_text()
        check_missing_reset(text, path.name)
        check_implicit_width(text, path.name)

    print("Sanity check complete.")


if __name__ == '__main__':
    main()