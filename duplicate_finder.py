#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for finding and moving duplicate photos/videos.
Preserves the best quality, protects folder D:\Zdjęcia (W)
"""

import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from PIL import Image
import json
from datetime import datetime

# Configuration
PROTECTED_FOLDER = r"D:\Zdjęcia (W)"
REVIEW_FOLDER = r"D:\do sprawdzenia Claude"
SCAN_ROOT = r"D:\\"
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4'}

class DuplicateFinder:
    def __init__(self):
        self.file_hashes = defaultdict(list)
        self.file_names = defaultdict(list)  # NEW: duplicates by filename
        self.stats = {
            'total_scanned': 0,
            'duplicates_found': 0,
            'duplicates_by_name': 0,  # NEW
            'files_moved': 0,
            'space_saved': 0
        }
        
    def calculate_hash(self, filepath):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"⚠️ Read error: {filepath} - {e}")
            return None
    
    def get_image_quality(self, filepath):
        """Return image quality (resolution * file_size)"""
        try:
            file_size = os.path.getsize(filepath)
            
            # For MP4 videos - use only file size
            if filepath.lower().endswith('.mp4'):
                return file_size
            
            # For photos - combination of resolution and size
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    resolution = width * height
                    # Quality = resolution * (file_size / 1000) 
                    # Give more weight to resolution
                    quality_score = resolution * 10 + file_size
                    return quality_score
            except:
                # If can't open as image, use size only
                return file_size
                
        except Exception as e:
            print(f"⚠️ Cannot determine quality: {filepath} - {e}")
            return 0
    
    def is_in_protected_folder(self, filepath):
        """Check if file is in protected folder"""
        try:
            return Path(filepath).is_relative_to(PROTECTED_FOLDER)
        except:
            return False
    
    def scan_files(self):
        """Scan all files"""
        print(f"🔍 Scanning {SCAN_ROOT}...")
        print(f"🛡️ Protected folder: {PROTECTED_FOLDER}")
        print(f"📁 Looking for: {', '.join(SUPPORTED_EXTENSIONS)}\n")
        
        for root, dirs, files in os.walk(SCAN_ROOT):
            for file in files:
                filepath = os.path.join(root, file)
                ext = Path(file).suffix.lower()
                
                if ext in SUPPORTED_EXTENSIONS:
                    self.stats['total_scanned'] += 1
                    
                    # Show progress every 10 files
                    if self.stats['total_scanned'] % 10 == 0:
                        print(f"   📸 Scanned: {self.stats['total_scanned']} photos/videos... (Current: {file[:40]})", end='\r')
                    
                    file_hash = self.calculate_hash(filepath)
                    
                    if file_hash:
                        quality = self.get_image_quality(filepath)
                        is_protected = self.is_in_protected_folder(filepath)
                        
                        file_info = {
                            'path': filepath,
                            'quality': quality,
                            'size': os.path.getsize(filepath),
                            'protected': is_protected
                        }
                        
                        # Add to hashes (identical content)
                        self.file_hashes[file_hash].append(file_info)
                        
                        # NEW: Add to filenames (same name)
                        filename_lower = file.lower()
                        self.file_names[filename_lower].append(file_info)
        
        print(f"\n✅ Scanned: {self.stats['total_scanned']} files")
    
    def find_duplicates(self):
        """Find duplicates and determine which files to move"""
        files_to_move = []
        processed_paths = set()  # Avoid duplicating files
        
        print(f"\n🔎 Looking for duplicates by content (hash)...")
        
        # 1. DUPLICATES BY HASH (identical content)
        for file_hash, files in self.file_hashes.items():
            if len(files) > 1:
                self.stats['duplicates_found'] += len(files) - 1
                
                # Sort: protected first, then by quality
                files_sorted = sorted(files, 
                                    key=lambda x: (x['protected'], x['quality']), 
                                    reverse=True)
                
                best_file = files_sorted[0]
                duplicates = files_sorted[1:]
                
                # Check if any duplicate has better quality than protected
                for dup in duplicates:
                    if best_file['protected'] and dup['quality'] > best_file['quality']:
                        # Duplicate has better quality than protected - keep it
                        print(f"\n⭐ Found better version than protected:")
                        print(f"   Protected: {best_file['path']} (quality: {best_file['quality']})")
                        print(f"   Better: {dup['path']} (quality: {dup['quality']})")
                        continue
                    
                    # Otherwise - move duplicate
                    if dup['path'] not in processed_paths:
                        files_to_move.append({
                            'original': best_file['path'],
                            'duplicate': dup['path'],
                            'size': dup['size'],
                            'reason': 'identical content (hash)'
                        })
                        processed_paths.add(dup['path'])
        
        print(f"✅ Found {self.stats['duplicates_found']} duplicates by content")
        
        # 2. DUPLICATES BY NAME (same name, different content)
        print(f"\n🔎 Looking for duplicates by filename...")
        
        for filename, files in self.file_names.items():
            if len(files) > 1:
                # Check if these aren't already duplicates by hash (skip them)
                unique_hashes = set()
                for f in files:
                    # Calculate simple identifier based on path and size
                    unique_hashes.add((f['path'], f['size']))
                
                if len(unique_hashes) > 1:  # Different files with same name
                    self.stats['duplicates_by_name'] += len(files) - 1
                    
                    # Sort: protected first, then by quality
                    files_sorted = sorted(files, 
                                        key=lambda x: (x['protected'], x['quality']), 
                                        reverse=True)
                    
                    best_file = files_sorted[0]
                    duplicates = files_sorted[1:]
                    
                    for dup in duplicates:
                        # Check if already processed
                        if dup['path'] in processed_paths:
                            continue
                            
                        if best_file['protected'] and dup['quality'] > best_file['quality']:
                            # Duplicate has better quality than protected - keep it
                            print(f"\n⭐ Found better version (by name) than protected:")
                            print(f"   Protected: {best_file['path']} (quality: {best_file['quality']})")
                            print(f"   Better: {dup['path']} (quality: {dup['quality']})")
                            continue
                        
                        # Move duplicate
                        files_to_move.append({
                            'original': best_file['path'],
                            'duplicate': dup['path'],
                            'size': dup['size'],
                            'reason': f'same name: {filename}'
                        })
                        processed_paths.add(dup['path'])
        
        print(f"✅ Found {self.stats['duplicates_by_name']} additional duplicates by name")
        return files_to_move
    
    def move_duplicates(self, files_to_move):
        """Copy duplicates to review folder"""
        if not files_to_move:
            print("\n🎉 No duplicates to move!")
            return []
        
        # Create review folder
        os.makedirs(REVIEW_FOLDER, exist_ok=True)
        
        print(f"\n📦 Copying {len(files_to_move)} duplicates to review folder...")
        
        report_lines = []
        report_lines.append(f"REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("="*80 + "\n\n")
        
        successfully_copied = []  # List of successfully copied files
        
        for item in files_to_move:
            try:
                duplicate_path = item['duplicate']
                # Preserve folder structure
                relative_path = os.path.relpath(duplicate_path, SCAN_ROOT)
                dest_path = os.path.join(REVIEW_FOLDER, relative_path)
                
                # Create destination folders
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Copy file
                shutil.copy2(duplicate_path, dest_path)
                
                self.stats['files_moved'] += 1
                self.stats['space_saved'] += item['size']
                
                # Add to successful copies list
                successfully_copied.append({
                    'original_path': duplicate_path,
                    'backup_path': dest_path,
                    'size': item['size']
                })
                
                # Add to report
                report_lines.append(f"DUPLICATE #{self.stats['files_moved']}\n")
                report_lines.append(f"  Reason: {item['reason']}\n")
                report_lines.append(f"  Original (kept): {item['original']}\n")
                report_lines.append(f"  Duplicate (copied): {duplicate_path}\n")
                report_lines.append(f"  Backup location: {dest_path}\n")
                report_lines.append(f"  Size: {item['size'] / 1024 / 1024:.2f} MB\n\n")
                
                print(f"   ✓ {self.stats['files_moved']}/{len(files_to_move)}", end='\r')
                
            except Exception as e:
                print(f"\n⚠️ Copy error {duplicate_path}: {e}")
        
        # Save report
        report_path = os.path.join(REVIEW_FOLDER, "duplicate_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(report_lines)
        
        print(f"\n✅ Copied {self.stats['files_moved']} files to backup")
        print(f"📄 Report saved: {report_path}")
        
        return successfully_copied
    
    def delete_originals(self, successfully_copied):
        """Delete original duplicates after confirmation"""
        if not successfully_copied:
            return
        
        print(f"\n" + "="*80)
        print("⚠️  DELETING ORIGINAL DUPLICATES")
        print("="*80)
        print(f"All {len(successfully_copied)} duplicates have been safely backed up to:")
        print(f"📁 {REVIEW_FOLDER}")
        print(f"\n💡 You can now delete the original duplicates from disk.")
        print(f"   Backup will remain in the review folder in case of issues.")
        print("="*80 + "\n")
        
        response = input("❓ Delete original duplicates? (yes/no): ")
        
        if response.lower() not in ['yes', 'y', 'tak', 't']:
            print("✋ Deletion cancelled. Duplicates remain on disk.")
            print(f"💾 Backup is located at: {REVIEW_FOLDER}")
            return
        
        # Additional confirmation
        print(f"\n⚠️  This will delete {len(successfully_copied)} files from disk!")
        confirm = input("❓ Are you sure? Type 'DELETE' to confirm: ")
        
        if confirm != 'DELETE':
            print("✋ Cancelled. No files deleted.")
            return
        
        # Delete files
        print(f"\n🗑️  Deleting {len(successfully_copied)} duplicates...")
        deleted_count = 0
        deleted_size = 0
        
        for item in successfully_copied:
            try:
                original_path = item['original_path']
                if os.path.exists(original_path):
                    os.remove(original_path)
                    deleted_count += 1
                    deleted_size += item['size']
                    print(f"   ✓ Deleted {deleted_count}/{len(successfully_copied)}", end='\r')
            except Exception as e:
                print(f"\n⚠️ Deletion error {original_path}: {e}")
        
        print(f"\n✅ Deleted {deleted_count} files")
        print(f"💾 Freed: {deleted_size / 1024 / 1024 / 1024:.2f} GB")
        print(f"🛡️ Backup remains at: {REVIEW_FOLDER}")
    
    def print_summary(self):
        """Display summary"""
        print("\n" + "="*80)
        print("📊 SUMMARY")
        print("="*80)
        print(f"Scanned files: {self.stats['total_scanned']}")
        print(f"Duplicates by content (hash): {self.stats['duplicates_found']}")
        print(f"Duplicates by name: {self.stats['duplicates_by_name']}")
        print(f"Total duplicates: {self.stats['duplicates_found'] + self.stats['duplicates_by_name']}")
        print(f"Moved files: {self.stats['files_moved']}")
        print(f"Space saved: {self.stats['space_saved'] / 1024 / 1024 / 1024:.2f} GB")
        print(f"Review folder: {REVIEW_FOLDER}")
        print("="*80)
        print("\n💡 WHAT HAPPENED:")
        print(f"1. Scanned {self.stats['total_scanned']} files")
        print(f"2. Found {self.stats['duplicates_found'] + self.stats['duplicates_by_name']} duplicates")
        print(f"3. Copied {self.stats['files_moved']} duplicates to backup")
        print(f"4. Backup is located at: {REVIEW_FOLDER}")
        print("\n💡 IF YOU DIDN'T DELETE ORIGINAL DUPLICATES:")
        print(f"   - Check backup at: {REVIEW_FOLDER}")
        print(f"   - Run script again to delete duplicates")
        print(f"   - Or delete them manually using the report as a guide")

def main():
    print("="*80)
    print("🖼️  DUPLICATE PHOTO & VIDEO FINDER (By content + by name)")
    print("="*80)
    print(f"Scan path: {SCAN_ROOT}")
    print(f"Protected folder: {PROTECTED_FOLDER}")
    print(f"Review folder: {REVIEW_FOLDER}")
    print("\nSearch methods:")
    print("  ✓ Identical files (same content)")
    print("  ✓ Same names (different sizes/quality)")
    print("="*80 + "\n")
    
    input("⏸️  Press ENTER to start scanning... ")
    
    finder = DuplicateFinder()
    
    # Step 1: Scan files
    finder.scan_files()
    
    # Step 2: Find duplicates
    files_to_move = finder.find_duplicates()
    
    if files_to_move:
        print(f"\n⚠️  Found {len(files_to_move)} duplicates to move.")
        response = input("Copy them to review folder? (yes/no): ")
        
        if response.lower() in ['yes', 'y', 'tak', 't']:
            # Step 3: Copy duplicates
            successfully_copied = finder.move_duplicates(files_to_move)
            
            # Step 4: Ask to delete originals
            if successfully_copied:
                finder.delete_originals(successfully_copied)
        else:
            print("❌ Copying cancelled.")
    
    # Summary
    finder.print_summary()

if __name__ == "__main__":
    main()
