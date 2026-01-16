# Creating a Release

This document explains how to create a new release of Image to PDF.

## Quick Start

To create a new release, simply create and push a version tag:

```bash
# Create a new version tag (e.g., v1.0.0)
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

That's it! GitHub Actions will automatically:
1. Build installers for macOS, Linux, and Windows
2. Create a new GitHub Release
3. Attach all installers to the release
4. Generate release notes

## Version Tag Format

Use semantic versioning with a `v` prefix:
- `v1.0.0` - Major release
- `v1.0.1` - Patch release
- `v1.1.0` - Minor release
- `v2.0.0-beta.1` - Pre-release

## Step-by-Step Release Process

### 1. Update Version in pyproject.toml

```toml
[project]
name = "img-to-pdf"
version = "1.0.0"  # Update this
```

### 2. Commit Version Bump

```bash
git add pyproject.toml
git commit -m "chore: bump version to 1.0.0"
git push
```

### 3. Create and Push Tag

```bash
# Create annotated tag with message
git tag -a v1.0.0 -m "Release v1.0.0"

# Push to GitHub
git push origin v1.0.0
```

### 4. Monitor Build

1. Go to the **Actions** tab in your GitHub repository
2. Watch the "Build Installers" workflow run
3. Wait for all three builds (macOS, Linux, Windows) to complete

### 5. Verify Release

1. Go to the **Releases** section of your repository
2. You should see a new release with:
   - Version tag (e.g., v1.0.0)
   - Auto-generated release notes
   - Three installer downloads:
     - `ImageToPDF.app.zip` (macOS)
     - `ImageToPDF-linux.tar.gz` (Linux)
     - `ImageToPDF-windows.zip` (Windows)

## Edit Release Notes (Optional)

After the release is created, you can edit it to add:
- A description of new features
- Bug fixes
- Breaking changes
- Installation instructions

1. Go to the release page
2. Click "Edit release"
3. Update the description
4. Click "Update release"

## Pre-releases

To create a pre-release (beta, alpha, rc):

```bash
# Create a pre-release tag
git tag v1.0.0-beta.1

# Push it
git push origin v1.0.0-beta.1
```

The workflow will automatically mark it as a pre-release if the tag contains:
- `alpha`
- `beta`
- `rc`

## Testing Without Release

If you want to test builds without creating a release:

1. Push to the `main` branch (without tags)
2. Builds will run and artifacts will be uploaded
3. Download artifacts from the Actions run
4. No release will be created

## Troubleshooting

### Build Failed

If any of the builds fail:
1. Check the Actions logs
2. Fix the issue
3. Delete the tag: `git tag -d v1.0.0 && git push origin :refs/tags/v1.0.0`
4. Create the tag again after pushing the fix

### Release Not Created

If builds succeed but no release appears:
- Make sure the tag starts with `v` (e.g., `v1.0.0` not `1.0.0`)
- Check that you pushed the tag with `git push origin v1.0.0`

### Wrong Files in Release

If the wrong files are attached:
1. Delete the release
2. Delete the tag: `git push origin :refs/tags/v1.0.0`
3. Fix the workflow
4. Create the tag again

## Deleting a Release

To delete a release and tag:

```bash
# Delete the tag locally
git tag -d v1.0.0

# Delete the tag on GitHub
git push origin :refs/tags/v1.0.0

# Manually delete the release from GitHub web interface
```

## Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Test the application locally
- [ ] Commit and push version bump
- [ ] Create version tag
- [ ] Push tag to GitHub
- [ ] Monitor Actions workflow
- [ ] Verify all three builds succeed
- [ ] Check release is created
- [ ] Test downloaded installers
- [ ] Edit release notes if needed
- [ ] Announce the release

## Examples

### First Release (v1.0.0)

```bash
# Update version
echo 'version = "1.0.0"' >> pyproject.toml

# Commit
git add pyproject.toml
git commit -m "chore: bump version to 1.0.0"
git push

# Tag and release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

### Patch Release (v1.0.1)

```bash
# After fixing bugs, bump version
git commit -m "fix: critical bug fix"
git push

# Tag
git tag v1.0.1 -m "Bug fix release"
git push origin v1.0.1
```

### Beta Release (v2.0.0-beta.1)

```bash
# For testing new features
git tag v2.0.0-beta.1 -m "Beta release for v2.0.0"
git push origin v2.0.0-beta.1
```

## Automated Release Notes

The workflow automatically generates release notes including:
- All commits since the last release
- Contributors
- Merged pull requests

You can customize the format by editing the workflow or the release after creation.

## Support

For issues with the release process, check:
- `.github/workflows/build-installers.yml` - The workflow file
- `BUILD_SYSTEM.md` - Build system documentation
- GitHub Actions logs - For build errors
