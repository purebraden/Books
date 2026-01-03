#!/usr/bin/env python3
"""
Extract missing chapters from the part files.
"""

from pathlib import Path
import re

def extract_chapter(filepath, chapter_title, output_dir):
    """Extract a specific chapter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the chapter
    pattern = rf'^{re.escape(chapter_title)}\s*$'
    lines = content.split('\n')
    
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if re.match(pattern, line.strip(), re.IGNORECASE):
            start_idx = i
            break
    
    if start_idx is None:
        print(f"  Chapter '{chapter_title}' not found in {filepath.name}")
        return False
    
    # Find the next chapter or end of file
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^CHAPTER\s+\d+|^PROLOGUE|^EPILOGUE', lines[i].strip(), re.IGNORECASE):
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = len(lines)
    
    # Extract content
    chapter_lines = lines[start_idx:end_idx]
    chapter_content = '\n'.join(chapter_lines).strip()
    
    # Determine filename
    if chapter_title.upper() == 'PROLOGUE':
        filename = 'Prologue.md'
    elif chapter_title.upper() == 'EPILOGUE':
        filename = 'Epilogue.md'
    else:
        # Extract number
        match = re.search(r'CHAPTER\s+(\d+)', chapter_title, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            filename = f'Chapter-{num:02d}.md'
        else:
            # Handle phase markers
            base_title = re.sub(r'\s*\([^)]+\)', '', chapter_title).strip()
            match = re.search(r'CHAPTER\s+(\d+)', base_title, re.IGNORECASE)
            if match:
                num = int(match.group(1))
                phase = re.search(r'\(([^)]+)\)', chapter_title)
                if phase:
                    phase_clean = phase.group(1).replace(' ', '-').upper()
                    filename = f'Chapter-{num:02d}-{phase_clean}.md'
                else:
                    filename = f'Chapter-{num:02d}.md'
            else:
                filename = f"{chapter_title.replace(' ', '-')}.md"
    
    # Format as markdown
    base_title = re.sub(r'\s*\([^)]+\)', '', chapter_title).strip()
    formatted = f"# {base_title}\n\n{chapter_content}\n"
    
    # Write file
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted)
    
    print(f"  Created: {filename}")
    return True

def main():
    base_dir = Path(__file__).parent
    book1_dir = base_dir / 'Gravewater' / 'book1'
    
    # Extract Chapter 35
    print("Extracting Chapter 35...")
    extract_chapter(
        book1_dir / 'part3.md',
        'CHAPTER 35 (Phase 1)',
        book1_dir
    )
    
    # Check if Epilogue exists in part files
    print("\nChecking for Epilogue in part files...")
    for part_file in [book1_dir / 'part1.md', book1_dir / 'part2.md', book1_dir / 'part3.md']:
        if part_file.exists():
            with open(part_file, 'r', encoding='utf-8') as f:
                if 'EPILOGUE' in f.read().upper():
                    print(f"  Found EPILOGUE in {part_file.name}")
                    extract_chapter(part_file, 'EPILOGUE', book1_dir)
                    break
    
    print("\nDone!")

if __name__ == '__main__':
    main()

