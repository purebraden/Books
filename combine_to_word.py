#!/usr/bin/env python3
"""
Script to combine all markdown files in book1 into a single Word document.
Order: Prologue, Chapters 1-35, Epilogue
"""

import subprocess
from pathlib import Path
import tempfile
import os

def main():
    base_dir = Path(__file__).parent
    book1_dir = base_dir / 'Gravewater' / 'book1'
    output_file = base_dir / 'Gravewater' / 'Gravewater_Book1.docx'
    
    # Get all markdown files, excluding alternate_versions
    files_to_combine = []
    
    # Prologue first
    prologue = book1_dir / 'Prologue.md'
    if prologue.exists():
        files_to_combine.append(prologue)
        print(f"Added: Prologue.md")
    
    # Chapters 1-35 in order
    for i in range(1, 36):
        chapter_file = book1_dir / f'Chapter-{i:02d}.md'
        if chapter_file.exists():
            files_to_combine.append(chapter_file)
            print(f"Added: Chapter-{i:02d}.md")
        else:
            print(f"Warning: Chapter-{i:02d}.md not found")
    
    # Epilogue last
    epilogue = book1_dir / 'Epilogue.md'
    if epilogue.exists():
        files_to_combine.append(epilogue)
        print(f"Added: Epilogue.md")
    
    if not files_to_combine:
        print("Error: No markdown files found!")
        return
    
    print(f"\nCombining {len(files_to_combine)} files into Word document...")
    print(f"Files in order: {[f.name for f in files_to_combine]}")
    
    # Create a temporary combined markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as combined_md:
        temp_md_path = combined_md.name
        
        # Write all files with page breaks between them
        for i, file_path in enumerate(files_to_combine):
            print(f"  Writing: {file_path.name}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Add page break before each new chapter (except the first)
                # Use Word-compatible page break
                if i > 0:
                    combined_md.write('\n\n<div style="page-break-before: always;"></div>\n\n')
                
                combined_md.write(content)
                combined_md.write('\n\n')
        
        # Verify Epilogue was written
        combined_md.flush()
        with open(temp_md_path, 'r', encoding='utf-8') as verify:
            content_check = verify.read()
            if 'Epilogue' in content_check:
                print(f"  [OK] Epilogue content verified in temp file")
            else:
                print(f"  [WARNING] Epilogue not found in temp file!")
        
        print(f"  Total content written to temp file")
    
    # Convert to Word using pandoc
    try:
        print(f"Converting to Word document...")
        # Build pandoc command with TOC and page breaks
        # Use --wrap=none to preserve HTML divs for page breaks
        cmd = [
            'pandoc',
            temp_md_path,
            '-o', str(output_file),
            '--toc',  # Add table of contents
            '--toc-depth=2',  # Show level 1 and 2 headings (to include Epilogue)
            '--standalone',  # Create standalone document
            '--wrap=none',  # Preserve HTML formatting
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\nSuccess! Created: {output_file}")
            print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")
            print("Features added:")
            print("  - Table of Contents")
            print("  - Page breaks between chapters")
        else:
            print(f"Error converting: {result.stderr}")
            # Try simpler version
            print("Trying simpler conversion...")
            cmd = [
                'pandoc',
                temp_md_path,
                '-o', str(output_file),
                '--toc',
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"\nSuccess! Created: {output_file}")
            else:
                print(f"Error: {result.stderr}")
    
    except FileNotFoundError:
        print("Error: pandoc not found. Please install pandoc first.")
        print("See INSTALL_INSTRUCTIONS.md for details.")
    finally:
        # Clean up temp file
        if os.path.exists(temp_md_path):
            os.unlink(temp_md_path)

if __name__ == '__main__':
    main()

