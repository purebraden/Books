#!/usr/bin/env python3
"""
Script to split the three part markdown files into individual chapter files.
"""

import re
import os
from pathlib import Path

def extract_chapter_number(title):
    """Extract chapter number from title like 'CHAPTER 1' or 'PROLOGUE'"""
    if title.upper() == 'PROLOGUE':
        return 0
    elif title.upper() == 'EPILOGUE':
        return 999
    match = re.search(r'CHAPTER\s+(\d+)', title, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def clean_title(title):
    """Clean chapter title, keeping phase markers for identification"""
    # Normalize spacing
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def get_phase_marker(title):
    """Extract phase marker from title like '(Phase 1)', '(Phase 2)', '(REWRITTEN)'"""
    match = re.search(r'\(([^)]+)\)', title)
    if match:
        return match.group(1)
    return None

def split_file(filepath, output_dir):
    """Split a markdown file into individual chapters"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by chapter markers (PROLOGUE, CHAPTER X, EPILOGUE)
    # Pattern matches: PROLOGUE, CHAPTER 1, CHAPTER 2, etc., EPILOGUE
    pattern = r'^(PROLOGUE|CHAPTER\s+\d+|EPILOGUE)(?:\s*\([^)]+\))?\s*$'
    
    chapters = []
    current_chapter = None
    current_content = []
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Check if this line is a chapter header
        if re.match(pattern, line.strip(), re.IGNORECASE):
            # Save previous chapter if exists
            if current_chapter is not None:
                chapters.append({
                    'title': current_chapter,
                    'content': '\n'.join(current_content).strip()
                })
            
            # Start new chapter
            current_chapter = clean_title(line.strip())
            current_content = []
        else:
            # Add line to current chapter
            if current_chapter is not None:
                current_content.append(line)
    
    # Don't forget the last chapter
    if current_chapter is not None:
        chapters.append({
            'title': current_chapter,
            'content': '\n'.join(current_content).strip()
        })
    
    # Write chapters to files
    for chapter in chapters:
        title = chapter['title']
        content = chapter['content']
        
        # Determine filename
        phase = get_phase_marker(title)
        base_title = re.sub(r'\s*\([^)]+\)', '', title).strip()
        
        if base_title.upper() == 'PROLOGUE':
            # Skip duplicate prologues (only keep first)
            filename = 'Prologue.md'
            if (output_dir / filename).exists():
                print(f"  Skipping duplicate: {filename}")
                continue
        elif base_title.upper() == 'EPILOGUE':
            filename = 'Epilogue.md'
        else:
            # Extract chapter number
            num = extract_chapter_number(base_title)
            if num is not None:
                if phase:
                    # Include phase in filename for duplicates
                    phase_clean = phase.replace(' ', '-').upper()
                    filename = f'Chapter-{num:02d}-{phase_clean}.md'
                else:
                    filename = f'Chapter-{num:02d}.md'
            else:
                # Fallback: use sanitized title
                filename = f"{base_title.replace(' ', '-')}.md"
        
        filepath = output_dir / filename
        
        # Format as markdown with title (use base title without phase marker in header)
        base_title = re.sub(r'\s*\([^)]+\)', '', title).strip()
        formatted_content = f"# {base_title}\n\n{content}\n"
        
        # Write file (overwrite if exists)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"  Created: {filename}")
    
    return len(chapters)

def main():
    # Set up paths
    base_dir = Path(__file__).parent
    book1_dir = base_dir / 'Gravewater' / 'book1'
    output_dir = base_dir / 'Gravewater' / 'book1'
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Process all three parts (look in book1 folder)
    part_files = [
        book1_dir / 'part1.md',
        book1_dir / 'part2.md',
        book1_dir / 'part3.md'
    ]
    
    total_chapters = 0
    for part_file in part_files:
        if part_file.exists():
            count = split_file(part_file, output_dir)
            total_chapters += count
        else:
            print(f"Warning: {part_file} not found")
    
    print(f"\nDone! Created {total_chapters} chapter files in {output_dir}")

if __name__ == '__main__':
    main()

