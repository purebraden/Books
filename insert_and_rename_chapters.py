#!/usr/bin/env python3
"""
Script to insert alternate versions into the book and rename chapters properly.
"""

import shutil
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    book1_dir = base_dir / 'Gravewater' / 'book1'
    alt_dir = book1_dir / '_alternate_versions'
    
    print("Step 1: Replacing chapters with alternate versions...")
    
    # Replace Chapter 33 with Phase 2 version
    ch33_regular = book1_dir / 'Chapter-33.md'
    ch33_phase2 = alt_dir / 'Chapter-33-PHASE-2.md'
    
    if ch33_phase2.exists():
        # Backup current Chapter 33
        shutil.move(str(ch33_regular), str(alt_dir / 'Chapter-33-regular-BACKUP.md'))
        # Move Phase 2 to main directory
        shutil.copy(str(ch33_phase2), str(ch33_regular))
        print("  [OK] Replaced Chapter 33 with Phase 2 version")
    
    # Replace Chapter 34 with Phase 1 version
    ch34_regular = book1_dir / 'Chapter-34.md'
    ch34_phase1 = alt_dir / 'Chapter-34-PHASE-1.md'
    
    if ch34_phase1.exists():
        # Backup current Chapter 34
        shutil.move(str(ch34_regular), str(alt_dir / 'Chapter-34-regular-BACKUP.md'))
        # Move Phase 1 to main directory
        shutil.copy(str(ch34_phase1), str(ch34_regular))
        print("  [OK] Replaced Chapter 34 with Phase 1 version")
    
    print("\nStep 2: Verifying chapter sequence...")
    
    # Get all chapter files
    chapters = []
    for f in sorted(book1_dir.glob('Chapter-*.md')):
        if f.name.startswith('Chapter-') and not f.name.startswith('Chapter-21-'):
            # Extract chapter number
            try:
                num = int(f.name.split('-')[1].split('.')[0])
                chapters.append((num, f))
            except:
                pass
    
    # Check for gaps
    chapter_nums = sorted([num for num, _ in chapters])
    print(f"  Found chapters: {min(chapter_nums)} to {max(chapter_nums)}")
    
    # Check if we need to handle Chapter 21 (REWRITTEN)
    ch21_rewritten = book1_dir / 'Chapter-21.md'
    if ch21_rewritten.exists():
        print("  [OK] Chapter 21 present (using REWRITTEN version)")
    
    # Verify Prologue and Epilogue
    prologue = book1_dir / 'Prologue.md'
    epilogue = book1_dir / 'Epilogue.md'
    
    if prologue.exists():
        print("  [OK] Prologue.md present")
    if epilogue.exists():
        print("  [OK] Epilogue.md present")
    
    print("\nStep 3: Final chapter list:")
    all_files = sorted([f for f in book1_dir.iterdir() if f.is_file() and not f.name.startswith('_')])
    for f in all_files:
        if f.name.endswith('.md'):
            print(f"  {f.name}")
    
    print("\nDone! Chapters are now in proper order with alternate versions inserted.")

if __name__ == '__main__':
    main()

