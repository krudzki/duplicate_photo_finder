# Quick Start Guide - Publishing to GitHub

This guide will help you publish your Duplicate Photo Finder project to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account created
- Project files ready (you have them!)

## Step 1: Initialize Git Repository

Open terminal in your project directory and run:

```bash
cd /path/to/duplicate-photo-finder
git init
```

## Step 2: Configure Git (First Time Only)

If you haven't configured Git before:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Stage All Files

```bash
git add .
```

## Step 4: Create First Commit

```bash
git commit -m "Initial commit: Duplicate Photo Finder v1.0.0"
```

## Step 5: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon (top right) → "New repository"
3. Repository name: `duplicate-photo-finder`
4. Description: "A powerful tool to find and manage duplicate photos and videos"
5. Choose: **Public** (for open source) or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (you already have these!)
7. Click "Create repository"

## Step 6: Connect Local to GitHub

GitHub will show commands. Copy and run them:

```bash
git remote add origin https://github.com/YOUR-USERNAME/duplicate-photo-finder.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 7: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files!

## Step 8: Customize Your Repository

### Update README.md

Edit these placeholders in `README.md`:
- Replace `yourusername` with your GitHub username
- Update author name in LICENSE file
- Add your email in setup.py

### Add Repository Topics

On GitHub repository page:
1. Click ⚙️ (settings icon) next to "About"
2. Add topics: `python`, `photos`, `duplicates`, `cleanup`, `photo-management`

### Enable GitHub Actions

GitHub Actions (CI/CD) should automatically run on your first push.

Check it: Repository → "Actions" tab

## Step 9: Create First Release

1. Go to your repository
2. Click "Releases" (right sidebar) → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Version 1.0.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

## Optional Enhancements

### Add Badges

Your README already has badges! Update the URLs:

```markdown
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### Enable Issues

Repository → Settings → General → Features → ✓ Issues

### Add Code of Conduct

Repository → Insights → Community → Add → Code of Conduct → Choose "Contributor Covenant"

### Add Security Policy

Create `.github/SECURITY.md`:

```markdown
# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities to: your.email@example.com

We take security seriously and will respond within 48 hours.
```

## Maintaining Your Project

### Making Changes

```bash
# Make your changes to files
git add .
git commit -m "Description of changes"
git push
```

### Creating New Versions

1. Update CHANGELOG.md
2. Update version in setup.py
3. Commit changes
4. Create new release on GitHub

### Accepting Pull Requests

1. Review the PR on GitHub
2. Test the changes locally if needed
3. Click "Merge pull request"

## Promoting Your Project

### Share On

- Reddit: r/Python, r/photography, r/DataHoarder
- Twitter/X: #Python #OpenSource #Photography
- Hacker News: news.ycombinator.com
- Dev.to: Write an article about it

### Optimize for Discovery

Add to these lists:
- Awesome Python: https://github.com/vinta/awesome-python
- PyPI: Publish your package (see setup.py)

## Troubleshooting

### "Remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/duplicate-photo-finder.git
```

### "Permission denied (publickey)"

Use HTTPS instead of SSH, or set up SSH keys:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "Failed to push some refs"

```bash
git pull origin main --rebase
git push origin main
```

## Next Steps

1. ✅ Star your own repository (why not? 😄)
2. ✅ Share with friends
3. ✅ Write a blog post about building it
4. ✅ Add more features
5. ✅ Help others who open issues

## Helpful Resources

- [GitHub Docs](https://docs.github.com)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Markdown Guide](https://www.markdownguide.org/)
- [Semantic Versioning](https://semver.org/)

---

**Congratulations! Your project is now on GitHub!** 🎉

Don't forget to update the README with your actual GitHub username and star your own project! ⭐
