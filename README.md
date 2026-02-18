# 🖼️ Duplicate Photo Finder

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful Python tool to find and manage duplicate photos and videos on your system. Detects duplicates by both **file content** (hash) and **filename**, preserving the highest quality version while safely backing up duplicates.

## ✨ Features

- 🔍 **Dual Detection Methods**
  - Content-based detection (MD5 hash) for identical files
  - Filename-based detection for same-name files with different quality
- 📊 **Smart Quality Analysis**
  - Combines resolution and file size for photos
  - Intelligent comparison for videos
- 🛡️ **Protected Folder Support**
  - Designate folders that should never have files removed
  - Automatically preserves higher quality versions even from unprotected folders
- 💾 **Safe Backup-First Approach**
  - Always creates backup before any deletion
  - Two-step confirmation process for deletion
  - Detailed report of all actions
- 🎯 **Efficient Scanning**
  - Supports: JPG, PNG, HEIC, MP4
  - Recursive directory traversal
  - Real-time progress indicators

## 📋 Requirements

- Python 3.8+
- Pillow (PIL)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/duplicate-photo-finder.git
cd duplicate-photo-finder

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
python duplicate_finder.py
```

### Configuration

Edit the configuration variables at the top of `duplicate_finder.py`:

```python
PROTECTED_FOLDER = r"D:\Zdjęcia (W)"  # Folder to protect from deletion
REVIEW_FOLDER = r"D:\do sprawdzenia Claude"  # Backup folder
SCAN_ROOT = r"D:\\"  # Root folder to scan
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4'}
```

## 📖 How It Works

1. **Scanning Phase**
   - Recursively scans specified directory
   - Calculates MD5 hash for each file
   - Tracks files by both content and filename

2. **Analysis Phase**
   - Identifies duplicates by hash (identical content)
   - Identifies duplicates by filename (same name, different quality)
   - Calculates quality score for each file:
     - Photos: `(width × height × 10) + file_size`
     - Videos: `file_size`

3. **Backup Phase**
   - Copies all duplicates to review folder
   - Preserves original folder structure
   - Generates detailed report

4. **Cleanup Phase** (Optional)
   - Requires double confirmation
   - Deletes original duplicates from disk
   - Keeps backup in review folder

## 🎯 Use Cases

- **Photography Workflow**: Clean up multiple exports of the same photo
- **Backup Consolidation**: Merge multiple backup folders
- **Storage Optimization**: Free up disk space by removing duplicate media
- **Library Management**: Organize photo libraries with duplicate versions

## 📊 Example Output

```
🖼️  DUPLICATE PHOTO & VIDEO FINDER (By content + by name)
================================================================================
Scan path: D:\
Protected folder: D:\Zdjęcia (W)
Review folder: D:\do sprawdzenia Claude

Search methods:
  ✓ Identical files (same content)
  ✓ Same names (different sizes/quality)
================================================================================

🔍 Scanning D:\...
   📸 Scanned: 32150 photos/videos...

✅ Scanned: 32150 files

🔎 Looking for duplicates by content (hash)...
✅ Found 45 duplicates by content

🔎 Looking for duplicates by filename...
✅ Found 23 additional duplicates by name

📊 SUMMARY
================================================================================
Scanned files: 32150
Duplicates by content (hash): 45
Duplicates by name: 23
Total duplicates: 68
Moved files: 68
Space saved: 2.34 GB
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code of Conduct
- Development setup
- Pull request process
- Coding standards

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Safety Features

- ✅ Never modifies protected folders
- ✅ Creates backup before any deletion
- ✅ Requires explicit confirmation for deletion
- ✅ Generates detailed reports of all actions
- ✅ Preserves folder structure in backups

## ⚠️ Disclaimer

Always backup your important data before running any file management tools. While this tool includes multiple safety features, the authors are not responsible for any data loss.

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information (OS, Python version)

## 💡 Future Enhancements

- [ ] GUI interface
- [ ] Support for more file formats (RAW, TIFF, etc.)
- [ ] Perceptual hash for similar-but-not-identical images
- [ ] Parallel processing for faster scanning
- [ ] Cloud storage integration
- [ ] Automatic quality detection improvements

## 👨‍💻 Author

Created with ❤️ for photographers and digital hoarders everywhere.

---

**Star ⭐ this repo if you find it useful!**
