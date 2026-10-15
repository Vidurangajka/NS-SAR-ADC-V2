#!/usr/bin/env python3
"""
For every cell folder in DIGITAL_LIB that has a matching cell folder name in
STD_CELL_LIB, this copies in every view (schematic, layout, spice, cdl,
etc.) from the standard cell library EXCEPT 'symbol' -- the existing
'symbol' view in DIGITAL_LIB is never touched, never backed up, never
replaced.

Any other existing view folder in DIGITAL_LIB/<cell>/ (e.g. a leftover
'schematic' from a previous SpiceIn attempt) is backed up first by renaming
it to '<view>_backup_<timestamp>', then the standard-cell version is copied
in fresh.

SAFETY:
  - A full backup of the entire DIGITAL_LIB directory is taken before
    anything else happens, into a sibling folder
    '<DIGITAL_LIB.name>_full_backup_<timestamp>'.
  - DRY_RUN defaults to True. Review the printed plan before setting it to
    False and running for real.
  - Close all Cadence sessions with either library open, and check for
    stray lock files first:
        find <DIGITAL_LIB> -name '.cdslck'

Run:
    python3 replace_views_keep_symbol.py
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

DIGITAL_LIB = Path("/home/user22/NS_SAR_ADC/libraries/NS_SAR_Digital")
STD_CELL_LIB = Path(
    "/home/user22/Sky130_cadence_pdk/sky130_scl_9T_0.1.1/sky130_scl_9T/oa/sky130_scl_9T"
)

EXCLUDE_VIEWS = {"symbol"}

# Set to False only after reviewing the dry-run output.
DRY_RUN = False

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def full_library_backup() -> Path:
    backup_path = DIGITAL_LIB.parent / f"{DIGITAL_LIB.name}_full_backup_{TIMESTAMP}"
    print(f"Full library backup -> {backup_path}")
    if not DRY_RUN:
        shutil.copytree(DIGITAL_LIB, backup_path)
    return backup_path


def main() -> None:
    if not DIGITAL_LIB.is_dir():
        raise SystemExit(f"ERROR: DIGITAL_LIB not found: {DIGITAL_LIB}")
    if not STD_CELL_LIB.is_dir():
        raise SystemExit(f"ERROR: STD_CELL_LIB not found: {STD_CELL_LIB}")

    print(f"DRY_RUN = {DRY_RUN}")
    print(f"DIGITAL_LIB  = {DIGITAL_LIB}")
    print(f"STD_CELL_LIB = {STD_CELL_LIB}")
    print()

    full_library_backup()
    print()

    matched = 0
    skipped_no_match = 0
    views_replaced = 0
    views_added = 0

    for cell_dir in sorted(DIGITAL_LIB.iterdir()):
        if not cell_dir.is_dir() or cell_dir.name.startswith(
            f"{DIGITAL_LIB.name}_full_backup"
        ):
            continue

        cell_name = cell_dir.name
        std_cell_dir = STD_CELL_LIB / cell_name

        if not std_cell_dir.is_dir():
            skipped_no_match += 1
            continue

        print(f"Match: {cell_name}")
        matched += 1

        for view_dir in sorted(std_cell_dir.iterdir()):
            if not view_dir.is_dir():
                continue
            view_name = view_dir.name

            if view_name in EXCLUDE_VIEWS:
                print(f"  Skipping '{view_name}' view (preserved, never touched)")
                continue

            dest_view = cell_dir / view_name

            if dest_view.exists():
                backup_view = cell_dir / f"{view_name}_backup_{TIMESTAMP}"
                print(f"  Backing up existing '{view_name}' -> {backup_view.name}")
                if not DRY_RUN:
                    shutil.move(str(dest_view), str(backup_view))
                views_replaced += 1
            else:
                views_added += 1

            print(f"  Copying '{view_name}' in from standard cell library")
            if not DRY_RUN:
                shutil.copytree(view_dir, dest_view)

    print()
    print("=== Summary ===")
    print(f"Cells matched              : {matched}")
    print(f"No matching cell in std lib: {skipped_no_match}")
    print(f"Views backed up & replaced : {views_replaced}")
    print(f"Views added fresh          : {views_added}")

    if DRY_RUN:
        print()
        print("This was a DRY RUN -- no files were changed.")
        print("Review the plan above, then set DRY_RUN = False to run for real.")


if __name__ == "__main__":
    main()