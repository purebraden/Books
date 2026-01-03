#!/usr/bin/env python3
"""
Script to organize chapters by continuity and rename them properly.
"""

import os
import shutil
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    book1_dir = base_dir / 'Gravewater' / 'book1'
    backup_dir = base_dir / 'Gravewater' / 'book1' / '_alternate_versions'
    
    # Create backup directory for alternate versions
    backup_dir.mkdir(exist_ok=True)
    
    # Chapter 21: Both versions are identical, keep REWRITTEN, move regular to backup
    ch21_regular = book1_dir / 'Chapter-21.md'
    ch21_rewritten = book1_dir / 'Chapter-21-REWRITTEN.md'
    
    if ch21_regular.exists() and ch21_rewritten.exists():
        # Compare file sizes - if identical, keep REWRITTEN
        if ch21_regular.stat().st_size == ch21_rewritten.stat().st_size:
            print("Chapter 21: Both versions identical, keeping REWRITTEN version")
            shutil.move(str(ch21_regular), str(backup_dir / 'Chapter-21-original.md'))
            shutil.move(str(ch21_rewritten), str(book1_dir / 'Chapter-21.md'))
        else:
            print("Chapter 21: Versions differ, keeping both for review")
            shutil.move(str(ch21_rewritten), str(backup_dir / 'Chapter-21-REWRITTEN.md'))
    
    # Chapter 33: Keep regular version (flows from 32), move Phase 2 to backup
    ch33_phase2 = book1_dir / 'Chapter-33-PHASE-2.md'
    if ch33_phase2.exists():
        print("Chapter 33: Moving Phase 2 to backup (keeping regular version)")
        shutil.move(str(ch33_phase2), str(backup_dir / 'Chapter-33-PHASE-2.md'))
    
    # Chapter 34: Keep regular version (flows from 33), move Phase versions to backup
    ch34_phase1 = book1_dir / 'Chapter-34-PHASE-1.md'
    ch34_phase2 = book1_dir / 'Chapter-34-PHASE-2.md'
    
    if ch34_phase1.exists():
        print("Chapter 34: Moving Phase 1 to backup")
        shutil.move(str(ch34_phase1), str(backup_dir / 'Chapter-34-PHASE-1.md'))
    
    if ch34_phase2.exists():
        # Check if it's a duplicate of regular
        ch34_regular = book1_dir / 'Chapter-34.md'
        if ch34_regular.exists():
            if ch34_regular.stat().st_size == ch34_phase2.stat().st_size:
                print("Chapter 34: Phase 2 is duplicate, moving to backup")
            else:
                print("Chapter 34: Phase 2 differs, moving to backup for review")
        shutil.move(str(ch34_phase2), str(backup_dir / 'Chapter-34-PHASE-2.md'))
    
    # Chapter 35: Keep regular version, move Phase 1 to backup (if it's a duplicate)
    ch35_phase1 = book1_dir / 'Chapter-35-PHASE-1.md'
    if ch35_phase1.exists():
        ch35_regular = book1_dir / 'Chapter-35.md'
        if ch35_regular.exists():
            if ch35_regular.stat().st_size == ch35_phase1.stat().st_size:
                print("Chapter 35: Phase 1 is duplicate, moving to backup")
            else:
                print("Chapter 35: Phase 1 differs, moving to backup for review")
        shutil.move(str(ch35_phase1), str(backup_dir / 'Chapter-35-PHASE-1.md'))
    
    # Verify final structure
    print("\nFinal chapter structure:")
    chapters = sorted([f for f in book1_dir.iterdir() if f.is_file() and f.name.startswith('Chapter-')])
    for ch in chapters:
        print(f"  {ch.name}")
    
    print(f"\nAlternate versions moved to: {backup_dir}")
    print("Done!")

if __name__ == '__main__':
    main()

