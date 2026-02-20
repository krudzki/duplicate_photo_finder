#!/usr/bin/env python3
"""
Unit tests for Duplicate Photo Finder
"""

import unittest
import tempfile
import shutil
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duplicate_finder import DuplicateFinder


class TestDuplicateFinder(unittest.TestCase):
    """Test cases for DuplicateFinder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.finder = DuplicateFinder()
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename, content):
        """Helper to create test files"""
        filepath = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath
    
    def test_calculate_hash(self):
        """Test MD5 hash calculation"""
        # Create test file
        test_content = b"test content for hashing"
        filepath = self.create_test_file("test.jpg", test_content)
        
        # Calculate hash
        hash1 = self.finder.calculate_hash(filepath)
        hash2 = self.finder.calculate_hash(filepath)
        
        # Same file should produce same hash
        self.assertEqual(hash1, hash2)
        self.assertIsNotNone(hash1)
        self.assertEqual(len(hash1), 32)  # MD5 hash is 32 chars
    
    def test_calculate_hash_different_content(self):
        """Test that different content produces different hashes"""
        file1 = self.create_test_file("test1.jpg", b"content A")
        file2 = self.create_test_file("test2.jpg", b"content B")
        
        hash1 = self.finder.calculate_hash(file1)
        hash2 = self.finder.calculate_hash(file2)
        
        self.assertNotEqual(hash1, hash2)
    
    def test_get_image_quality_nonexistent_file(self):
        """Test quality calculation for non-existent file"""
        quality = self.finder.get_image_quality("/fake/path/file.jpg")
        self.assertEqual(quality, 0)
    
    def test_is_in_protected_folder(self):
        """Test protected folder detection"""
        # Set up protected folder
        self.finder.PROTECTED_FOLDER = os.path.join(self.test_dir, "protected")
        os.makedirs(self.finder.PROTECTED_FOLDER)
        
        # Create files
        protected_file = self.create_test_file("protected/image.jpg", b"data")
        normal_file = self.create_test_file("normal/image.jpg", b"data")
        
        # Test detection
        self.assertTrue(self.finder.is_in_protected_folder(protected_file))
        self.assertFalse(self.finder.is_in_protected_folder(normal_file))
    
    def test_duplicate_detection_by_hash(self):
        """Test finding duplicates with identical content"""
        # Create identical files in different locations
        content = b"identical content"
        file1 = self.create_test_file("folder1/image.jpg", content)
        file2 = self.create_test_file("folder2/copy.jpg", content)
        
        # Mock the scan by directly adding to file_hashes
        hash_val = self.finder.calculate_hash(file1)
        
        self.finder.file_hashes[hash_val].append({
            'path': file1,
            'quality': 1000,
            'size': len(content),
            'protected': False
        })
        self.finder.file_hashes[hash_val].append({
            'path': file2,
            'quality': 1000,
            'size': len(content),
            'protected': False
        })
        
        # Find duplicates
        duplicates = self.finder.find_duplicates()
        
        # Should find 1 duplicate (keeps best, marks other as duplicate)
        self.assertEqual(len(duplicates), 1)
        self.assertIn('identical content', duplicates[0]['reason'])
    
    def test_stats_initialization(self):
        """Test that stats are properly initialized"""
        self.assertEqual(self.finder.stats['total_scanned'], 0)
        self.assertEqual(self.finder.stats['duplicates_found'], 0)
        self.assertEqual(self.finder.stats['duplicates_by_name'], 0)
        self.assertEqual(self.finder.stats['files_moved'], 0)
        self.assertEqual(self.finder.stats['space_saved'], 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.finder = DuplicateFinder()
    
    def test_empty_directory_scan(self):
        """Test scanning an empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.finder.SCAN_ROOT = tmpdir
            self.finder.scan_files()
            self.assertEqual(self.finder.stats['total_scanned'], 0)
    
    def test_calculate_hash_with_permission_error(self):
        """Test hash calculation with permission denied"""
        # This test might behave differently on different OS
        fake_path = "/root/restricted/file.jpg"
        hash_result = self.finder.calculate_hash(fake_path)
        self.assertIsNone(hash_result)


if __name__ == '__main__':
    unittest.main()
