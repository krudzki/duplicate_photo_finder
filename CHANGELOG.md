# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-02-18

### Added
- Initial release
- Dual detection methods: by content (hash) and by filename
- Smart quality analysis combining resolution and file size
- Protected folder support
- Safe backup-first approach with double confirmation
- Support for JPG, PNG, HEIC, MP4 files
- Recursive directory scanning
- Real-time progress indicators
- Detailed reporting system
- Comprehensive documentation and examples

### Features
- MD5 hash-based duplicate detection
- Filename-based duplicate detection for same-name files
- Quality scoring algorithm for photos (resolution × 10 + file_size)
- Video quality comparison by file size
- Automatic preservation of highest quality versions
- Backup folder with preserved directory structure
- Two-step deletion confirmation process
- Cross-platform support (Windows, macOS, Linux)

### Documentation
- Complete README with badges and examples
- Contributing guidelines
- MIT License
- Example scripts
- Unit tests
- GitHub Actions CI/CD pipeline

## [Unreleased]

### Planned Features
- GUI interface
- Support for RAW and TIFF formats
- Perceptual hash for similar images
- Parallel processing
- Cloud storage integration
- Command-line arguments support
- Configuration file support
