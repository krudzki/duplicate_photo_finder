#!/usr/bin/env python3
"""
Example: Basic usage of Duplicate Photo Finder

This example demonstrates the most common use case:
scanning a folder for duplicates and backing them up.
"""

import sys
import os

# Add parent directory to path to import duplicate_finder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duplicate_finder import DuplicateFinder

def main():
    """
    Example: Scan a test folder for duplicates
    """
    
    # Configure paths (adjust these for your system)
    SCAN_PATH = r"C:\Users\YourName\TestPhotos"  # Change this
    PROTECTED_PATH = r"C:\Users\YourName\TestPhotos\Important"  # Change this
    BACKUP_PATH = r"C:\Users\YourName\DuplicatesBackup"  # Change this
    
    print("=" * 80)
    print("Duplicate Photo Finder - Example Usage")
    print("=" * 80)
    print(f"\nScan path: {SCAN_PATH}")
    print(f"Protected folder: {PROTECTED_PATH}")
    print(f"Backup folder: {BACKUP_PATH}\n")
    
    # Create finder instance
    finder = DuplicateFinder()
    
    # Override default configuration
    finder.SCAN_ROOT = SCAN_PATH
    finder.PROTECTED_FOLDER = PROTECTED_PATH
    finder.REVIEW_FOLDER = BACKUP_PATH
    
    # Step 1: Scan for files
    print("Step 1: Scanning for photos and videos...")
    finder.scan_files()
    
    # Step 2: Find duplicates
    print("\nStep 2: Analyzing duplicates...")
    files_to_move = finder.find_duplicates()
    
    if not files_to_move:
        print("\n✅ No duplicates found!")
        return
    
    # Step 3: Show what was found
    print(f"\n📊 Found {len(files_to_move)} duplicates:")
    for i, item in enumerate(files_to_move[:5], 1):  # Show first 5
        print(f"  {i}. {os.path.basename(item['duplicate'])}")
        print(f"     Reason: {item['reason']}")
        print(f"     Size: {item['size'] / 1024 / 1024:.2f} MB\n")
    
    if len(files_to_move) > 5:
        print(f"  ... and {len(files_to_move) - 5} more\n")
    
    # Step 4: Backup duplicates (in real usage, you'd prompt user)
    print("Step 3: Creating backup...")
    successfully_copied = finder.move_duplicates(files_to_move)
    
    # Step 5: Summary
    finder.print_summary()
    
    print("\n💡 Next steps:")
    print("  1. Review the backup folder")
    print("  2. Check the duplicate_report.txt")
    print("  3. If everything looks good, run the script with deletion enabled")

if __name__ == "__main__":
    main()
