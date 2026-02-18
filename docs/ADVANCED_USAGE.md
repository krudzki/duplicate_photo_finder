# Advanced Usage Guide

This guide covers advanced use cases and customization options for Duplicate Photo Finder.

## Table of Contents

1. [Custom Configuration](#custom-configuration)
2. [Programmatic Usage](#programmatic-usage)
3. [Quality Algorithm Customization](#quality-algorithm-customization)
4. [Batch Processing](#batch-processing)
5. [Integration with Other Tools](#integration-with-other-tools)

## Custom Configuration

### Modifying Detection Settings

You can customize which file extensions to scan:

```python
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mov', '.avi'}
```

### Multiple Protected Folders

To protect multiple folders, modify the `is_in_protected_folder` method:

```python
PROTECTED_FOLDERS = [
    r"D:\Important Photos",
    r"D:\Archives\Professional",
    r"D:\Family Photos"
]

def is_in_protected_folder(self, filepath):
    """Check if file is in any protected folder"""
    try:
        path = Path(filepath)
        return any(path.is_relative_to(folder) for folder in PROTECTED_FOLDERS)
    except:
        return False
```

## Programmatic Usage

### Using as a Library

```python
from duplicate_finder import DuplicateFinder

# Initialize finder
finder = DuplicateFinder()

# Configure paths
finder.SCAN_ROOT = r"C:\Photos"
finder.PROTECTED_FOLDER = r"C:\Photos\Important"
finder.REVIEW_FOLDER = r"C:\Backups\Duplicates"

# Run scan
finder.scan_files()

# Get duplicates without moving
duplicates = finder.find_duplicates()

# Custom processing
for dup in duplicates:
    print(f"Found: {dup['duplicate']}")
    print(f"Reason: {dup['reason']}")
    print(f"Size: {dup['size'] / 1024:.2f} KB")
```

### Custom Filtering

Filter duplicates before processing:

```python
# Get all duplicates
all_duplicates = finder.find_duplicates()

# Filter only large files (> 5MB)
large_duplicates = [
    dup for dup in all_duplicates 
    if dup['size'] > 5 * 1024 * 1024
]

# Filter by file type
video_duplicates = [
    dup for dup in all_duplicates
    if dup['duplicate'].lower().endswith('.mp4')
]

# Process filtered list
finder.move_duplicates(large_duplicates)
```

## Quality Algorithm Customization

### Custom Quality Scoring

Modify the quality calculation for specific needs:

```python
def get_image_quality(self, filepath):
    """Custom quality calculation prioritizing resolution"""
    try:
        file_size = os.path.getsize(filepath)
        
        if filepath.lower().endswith('.mp4'):
            # For videos, prefer higher bitrate (size)
            return file_size * 10
        
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                resolution = width * height
                
                # Custom formula: heavily favor resolution
                quality_score = resolution * 100 + file_size
                return quality_score
        except:
            return file_size
            
    except Exception as e:
        return 0
```

### Consider EXIF Data

Add EXIF metadata to quality scoring:

```python
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_quality_with_exif(self, filepath):
    """Enhanced quality with EXIF consideration"""
    base_quality = self.get_image_quality(filepath)
    
    try:
        with Image.open(filepath) as img:
            exif = img._getexif()
            if exif:
                # Bonus for photos with GPS data
                if 34853 in exif:  # GPS IFD
                    base_quality *= 1.1
                
                # Bonus for RAW format conversions
                if exif.get(272, '').upper() in ['NIKON', 'CANON', 'SONY']:
                    base_quality *= 1.05
    except:
        pass
    
    return base_quality
```

## Batch Processing

### Processing Multiple Directories

```python
import os

directories_to_scan = [
    r"D:\Photos\2023",
    r"D:\Photos\2024",
    r"E:\Backup\Photos"
]

for directory in directories_to_scan:
    print(f"\n{'='*80}")
    print(f"Processing: {directory}")
    print('='*80)
    
    finder = DuplicateFinder()
    finder.SCAN_ROOT = directory
    finder.REVIEW_FOLDER = os.path.join(directory, "_duplicates_backup")
    
    finder.scan_files()
    duplicates = finder.find_duplicates()
    
    if duplicates:
        finder.move_duplicates(duplicates)
    
    finder.print_summary()
```

### Scheduled Execution

Create a scheduled task (Windows) or cron job (Linux/Mac):

**Windows Task Scheduler:**
```batch
@echo off
python "C:\path\to\duplicate_finder.py"
```

**Linux/Mac Cron:**
```bash
# Run every Sunday at 2 AM
0 2 * * 0 /usr/bin/python3 /path/to/duplicate_finder.py
```

## Integration with Other Tools

### Export to CSV

```python
import csv

duplicates = finder.find_duplicates()

with open('duplicates_report.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Original', 'Duplicate', 'Reason', 'Size (MB)'])
    
    for dup in duplicates:
        writer.writerow([
            dup['original'],
            dup['duplicate'],
            dup['reason'],
            f"{dup['size'] / 1024 / 1024:.2f}"
        ])
```

### JSON Export

```python
import json

duplicates = finder.find_duplicates()

report = {
    'scan_date': datetime.now().isoformat(),
    'total_scanned': finder.stats['total_scanned'],
    'duplicates_found': len(duplicates),
    'duplicates': duplicates
}

with open('duplicates_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
```

### Integration with Cloud Storage

```python
# Example: Google Drive integration
from googleapiclient.discovery import build

def upload_to_drive(filepath, folder_id):
    """Upload backup to Google Drive"""
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': os.path.basename(filepath),
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return file.get('id')

# After backing up duplicates
for dup in successfully_copied:
    upload_to_drive(dup['backup_path'], DRIVE_FOLDER_ID)
```

## Performance Optimization

### Parallel Processing

For very large libraries, consider parallel processing:

```python
from concurrent.futures import ThreadPoolExecutor
import hashlib

def calculate_hash_parallel(self, filepaths):
    """Calculate hashes in parallel"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(self.calculate_hash, filepaths)
    return dict(zip(filepaths, results))
```

### Memory Optimization

For systems with limited RAM:

```python
def scan_files_chunked(self, chunk_size=1000):
    """Process files in chunks to reduce memory usage"""
    file_buffer = []
    
    for root, dirs, files in os.walk(self.SCAN_ROOT):
        for file in files:
            if Path(file).suffix.lower() in SUPPORTED_EXTENSIONS:
                file_buffer.append(os.path.join(root, file))
                
                if len(file_buffer) >= chunk_size:
                    self._process_chunk(file_buffer)
                    file_buffer = []
    
    # Process remaining files
    if file_buffer:
        self._process_chunk(file_buffer)
```

## Troubleshooting

### Common Issues

**Issue: Out of memory with large photo libraries**
- Use chunked processing (see above)
- Reduce `chunk_size` parameter
- Close other applications

**Issue: Slow scanning on network drives**
- Copy files locally first
- Use `--fast-scan` mode (skip quality analysis)
- Increase network buffer size

**Issue: Permission errors**
- Run as administrator (Windows) or with sudo (Linux/Mac)
- Check file permissions
- Skip problematic files with try-except

## Best Practices

1. **Always backup before running**: Even with safety features, maintain separate backups
2. **Test on small directory first**: Verify behavior before scanning large libraries
3. **Review the report**: Check `duplicate_report.txt` before deleting
4. **Use protected folders**: Mark important directories as protected
5. **Regular maintenance**: Run periodically to keep libraries clean

## Support

For more help:
- Check the [main README](../README.md)
- Review [examples](../examples/)
- Open an [issue on GitHub](https://github.com/krudzki/duplicate_photo_finder/issues)
