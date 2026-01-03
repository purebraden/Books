# Installation Instructions: Python & Pandoc for Windows

## Installing Python

### Option 1: Microsoft Store (Easiest)
1. Open the **Microsoft Store**
2. Search for **"Python 3.12"** (or latest version)
3. Click **"Get"** or **"Install"**
4. After installation, verify:
   - Open PowerShell
   - Run: `python --version`

### Option 2: Official Installer
1. Go to https://www.python.org/downloads/
2. Download the latest **Python 3.x** installer
3. Run the installer
4. **IMPORTANT:** Check **"Add Python to PATH"** during installation
5. Click **"Install Now"**
6. Verify: `python --version` in PowerShell

---

## Installing Pandoc

### Option 1: Installer (Recommended)
1. Go to https://github.com/jgm/pandoc/releases/latest
2. Download **`pandoc-X.X.X-windows-x86_64.msi`** (latest version)
3. Run the installer
4. Follow the prompts (defaults are fine)
5. Verify: `pandoc --version` in PowerShell

### Option 2: Using Chocolatey (if you have it)
```powershell
choco install pandoc
```

---

## After Installation

1. **Open a new PowerShell window** (to refresh PATH)
2. Verify both are installed:
   ```powershell
   python --version
   pandoc --version
   ```

---

## Converting Your .docx Files

Once both are installed, you can convert the files:

### Convert a single file:
```powershell
pandoc "parts\Gravewater pt1.docx" -o "parts\Gravewater pt1.md"
```

### Convert all three at once:
```powershell
pandoc "parts\Gravewater pt1.docx" -o "parts\Gravewater pt1.md"
pandoc "parts\Gravewater pt2.docx" -o "parts\Gravewater pt2.md"
pandoc "parts\Gravewater pt3.docx" -o "parts\Gravewater pt3.md"
```

---

## Troubleshooting

### Python not found
- Make sure you checked "Add Python to PATH" during installation
- Restart PowerShell/terminal after installation
- Try `py --version` instead of `python --version`

### Pandoc not found
- Restart PowerShell/terminal after installation
- Check that Pandoc is in your PATH: `$env:PATH -split ';' | Select-String pandoc`

### Permission errors
- Run PowerShell as Administrator if needed
- Check file paths are correct

---

*Created: January 2, 2026*


