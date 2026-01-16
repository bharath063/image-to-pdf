# CI/CD Guide

This project uses an **automated CI/CD pipeline** that handles versioning, building, and releasing automatically.

## 🚀 How It Works

### On Every Push to `main`:

1. **Analyzes your commits** to determine version bump
2. **Automatically bumps version** in `pyproject.toml`
3. **Commits the change** back to the repository
4. **Creates a git tag** (e.g., `v1.2.3`)
5. **Builds installers** for macOS, Linux, and Windows
6. **Creates a GitHub Release** with all installers attached

## 📝 Commit Message Format (Conventional Commits)

The system uses your commit messages to determine how to bump the version:

### Patch Release (0.0.X)
```bash
git commit -m "fix: resolve crash on startup"
git commit -m "fix(ui): correct button alignment"
git commit -m "patch: update dependencies"
```

### Minor Release (0.X.0)
```bash
git commit -m "feat: add drag and drop support"
git commit -m "feature: implement dark mode"
```

### Major Release (X.0.0)
```bash
git commit -m "feat!: redesign UI with breaking changes"
git commit -m "feature!: new API with breaking changes"

# Or in commit body:
git commit -m "feat: redesign authentication

BREAKING CHANGE: old auth tokens no longer supported"
```

## 🎯 Complete Workflow Example

### Scenario 1: Bug Fix

```bash
# 1. Fix the bug
git add .
git commit -m "fix: resolve PDF generation error"

# 2. Push to main
git push origin main

# 3. Automatic process:
#    - Current version: 1.2.3
#    - Detects "fix:" → patch bump
#    - New version: 1.2.4
#    - Updates pyproject.toml
#    - Creates tag v1.2.4
#    - Builds installers
#    - Creates GitHub Release v1.2.4
```

### Scenario 2: New Feature

```bash
# 1. Implement feature
git add .
git commit -m "feat: add PDF preview before export"

# 2. Push to main
git push origin main

# 3. Automatic process:
#    - Current version: 1.2.4
#    - Detects "feat:" → minor bump
#    - New version: 1.3.0
#    - Creates release v1.3.0
```

### Scenario 3: Breaking Change

```bash
# 1. Make breaking changes
git add .
git commit -m "feat!: redesign export API

BREAKING CHANGE: ExportPDF() now requires options parameter"

# 2. Push to main
git push origin main

# 3. Automatic process:
#    - Current version: 1.3.0
#    - Detects "!" or "BREAKING CHANGE:" → major bump
#    - New version: 2.0.0
#    - Creates release v2.0.0
```

## 🔒 Safety Features

### 1. **Prevents Infinite Loops**
- Bot commits include `[skip ci]` to prevent re-triggering
- Workflow checks for this marker

### 2. **Tag Conflict Prevention**
- Checks if tag already exists before creating
- Fails early if version conflict detected

### 3. **Build Validation**
- Release only created if ALL builds succeed
- macOS, Linux, and Windows must all pass

### 4. **No Release on PR Merges with No Real Changes**
- If version doesn't change, no release is created
- Artifacts are still built for testing

## 📦 What Gets Created

For version `1.2.3`, the following are created:

### 1. **Git Tag**
```
v1.2.3
```

### 2. **GitHub Release**
- Title: `Release v1.2.3`
- Changelog: Auto-generated from commits
- Assets:
  - `ImageToPDF-1.2.3-macos.zip`
  - `ImageToPDF-1.2.3-linux.tar.gz`
  - `ImageToPDF-1.2.3-windows.zip`

### 3. **Updated pyproject.toml**
```toml
[project]
version = "1.2.3"
```

## 🛠️ Manual Release (Alternative)

If you prefer manual control, you can still create releases the old way:

```bash
# 1. Manually update pyproject.toml
# version = "2.0.0"

# 2. Commit
git commit -am "chore: bump version to 2.0.0 [skip ci]"
git push

# 3. Create tag manually
git tag v2.0.0
git push origin v2.0.0

# 4. Workflow will detect existing tag and build for it
```

## 🔍 Monitoring Releases

### Check Release Status

1. **Actions Tab**: Monitor workflow progress
   - `https://github.com/YOUR_USERNAME/image-to-pdf/actions`

2. **Releases Page**: See published releases
   - `https://github.com/YOUR_USERNAME/image-to-pdf/releases`

### Workflow Steps

The workflow consists of 3 jobs:

1. **version-and-release** (1-2 min)
   - Analyzes commits
   - Bumps version
   - Creates tag

2. **build** (5-10 min)
   - Builds for macOS, Linux, Windows in parallel
   - Creates installers

3. **release** (1-2 min)
   - Downloads all artifacts
   - Creates GitHub Release
   - Attaches installers

## 🐛 Troubleshooting

### No Release Created

**Symptom**: Push successful but no release appears

**Possible Causes**:
1. Commit message doesn't match conventional format
2. Version didn't change
3. Commit has `[skip ci]` marker

**Solution**:
```bash
# Check Actions tab for logs
# Make a commit with proper format:
git commit --allow-empty -m "feat: trigger release"
git push
```

### Tag Already Exists

**Symptom**: Workflow fails with "tag already exists"

**Solution**:
```bash
# Delete the tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Fix the issue and push again
git push
```

### Build Failed on One Platform

**Symptom**: macOS/Linux/Windows build fails

**Solution**:
- Check Actions logs for specific error
- Fix the issue
- Tag gets created but release doesn't (by design)
- Push fix, version will bump again

## 🎛️ Configuration

### Change Version Bump Strategy

Edit `.github/workflows/release.yml`:

```yaml
# Current logic (lines ~50-60)
if echo "$COMMITS" | grep -qiE "^(feat|feature)(\(.*\))?!:|^BREAKING CHANGE:"; then
  BUMP_TYPE="major"
elif echo "$COMMITS" | grep -qiE "^(feat|feature)(\(.*\))?:"; then
  BUMP_TYPE="minor"
else
  BUMP_TYPE="patch"
fi
```

### Disable Auto-Release

To temporarily disable auto-releases:

**Option 1**: Add `[skip ci]` to commits
```bash
git commit -m "fix: something [skip ci]"
```

**Option 2**: Disable workflow in GitHub
- Go to Actions → Release → Disable workflow

### Custom Release Notes

Release notes are auto-generated from commits. To customize:

Edit the "Create Release" step in `.github/workflows/release.yml`:

```yaml
body: |
  ## Custom Release Notes
  
  Your custom text here...
  
  ${{ steps.changelog.outputs.changelog }}
```

## 📊 Version History

Track all versions in your project:

```bash
# List all tags
git tag -l

# View specific release
git show v1.2.3

# Compare versions
git log v1.2.3..v1.3.0 --oneline
```

## 🔄 Migration from Old System

If you were using the previous manual tag system:

1. **Old workflow** (`.github/workflows/build-installers.yml`): Can be removed or kept as backup
2. **New workflow** (`.github/workflows/release.yml`): Fully automated
3. **Commit messages**: Start using conventional format
4. **Version management**: Handled automatically

## 💡 Best Practices

### 1. **Use Clear Commit Messages**
```bash
# Good
git commit -m "feat: add export to PNG feature"
git commit -m "fix: resolve memory leak in image processing"

# Bad
git commit -m "updates"
git commit -m "stuff"
```

### 2. **Batch Related Changes**
```bash
# Combine related fixes in one commit
git add file1.py file2.py
git commit -m "fix: resolve multiple UI issues"
```

### 3. **Test Before Pushing to Main**
```bash
# Use feature branches for development
git checkout -b feature/new-feature
# ... make changes ...
git push origin feature/new-feature
# Create PR, review, then merge
```

### 4. **Review Release Notes**
- After automatic release, you can edit release notes on GitHub
- Add screenshots, breaking change warnings, etc.

## 🆘 Emergency Procedures

### Rollback a Release

```bash
# 1. Delete the release from GitHub UI

# 2. Delete the tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# 3. Revert the version commit
git revert HEAD
git push
```

### Hotfix for Production Issue

```bash
# 1. Create hotfix
git commit -m "fix!: critical security patch"

# 2. Push immediately
git push origin main

# 3. Automatic release will create new version
#    with "fix!" → patch bump → v1.2.4
```

## 📚 Additional Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)

## 🎉 Success Indicators

Your CI/CD is working correctly when:

✅ Commits to main automatically create releases
✅ Version numbers follow semantic versioning
✅ All three platform installers are built
✅ Changelog is auto-generated
✅ No manual version management needed
