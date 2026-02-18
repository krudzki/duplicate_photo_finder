# Contributing to Duplicate Photo Finder

First off, thank you for considering contributing to Duplicate Photo Finder! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (file types, folder structures, etc.)
- **Describe the behavior you observed** and what you expected
- **Include system information**: OS, Python version, dependency versions
- **Add screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any alternatives** you've considered

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the code style** (PEP 8, use `black` for formatting)
3. **Write clear commit messages**
4. **Add tests** if you're adding functionality
5. **Update documentation** (README, docstrings, etc.)
6. **Ensure all tests pass**

#### Pull Request Process

1. Update the README.md with details of changes (if applicable)
2. Update the requirements.txt if you add dependencies
3. The PR will be merged once you have the sign-off of maintainers

## Development Setup

```bash
# Clone your fork
git clone https://github.com/krudzki/duplicate_photo_finder.git
cd duplicate-photo-finder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Style Guidelines

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use `black` for code formatting: `black .`
- Use type hints where appropriate
- Write descriptive docstrings for functions and classes

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add filename-based duplicate detection

- Implement secondary detection method by filename
- Add quality comparison for same-name files
- Update documentation with new feature details

Fixes #123
```

### Documentation

- Keep README.md up to date
- Document all public functions and classes
- Add inline comments for complex logic
- Update examples when adding features

## Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=duplicate_finder

# Run specific test
python -m pytest tests/test_duplicate_finder.py::test_hash_calculation
```

## Project Structure

```
duplicate-photo-finder/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── docs/                   # Additional documentation
├── examples/              # Example scripts and use cases
├── tests/                 # Unit and integration tests
├── duplicate_finder.py    # Main script
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
└── .gitignore
```

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

## Recognition

Contributors will be recognized in the README.md file.

Thank you for your contributions! 🙌
