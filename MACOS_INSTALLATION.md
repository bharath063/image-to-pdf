# macOS Installation Guide

## Installing ImageToPDF on macOS

### Download

1. Go to [Releases](../../releases)
2. Download the latest `ImageToPDF-X.Y.Z-macos.zip`
3. Double-click to unzip

### Installation & First Launch

macOS will prevent the app from running the first time because it was downloaded from the internet. Here's how to safely open it:

#### Method 1: Right-Click to Open (Recommended)

1. **Unzip** the downloaded file
2. **Right-click** (or Control+click) on `ImageToPDF.app`
3. Select **"Open"** from the menu
4. Click **"Open"** in the security dialog that appears
5. The app will launch and macOS will remember your choice

#### Method 2: System Settings

1. Try to open the app normally (it will be blocked)
2. Go to **System Settings** → **Privacy & Security**
3. Scroll down to find the security message about ImageToPDF
4. Click **"Open Anyway"**
5. Confirm by clicking **"Open"**

#### Method 3: Terminal Command

If you're comfortable with the terminal:

```bash
# Navigate to where you unzipped the app
cd ~/Downloads

# Remove quarantine attribute
xattr -cr ImageToPDF.app

# Now open normally
open ImageToPDF.app
```

## Common Issues

### "ImageToPDF is damaged and can't be opened"

This usually means macOS is blocking the app. Use **Method 1** (Right-click → Open) above.

### App Crashes Immediately

If the app crashes right after opening:

1. Make sure you've removed the quarantine attribute (see Method 3 above)
2. Try running from Terminal to see error messages:
   ```bash
   ./ImageToPDF.app/Contents/MacOS/ImageToPDF
   ```
3. Make sure you're on macOS 10.13 or later

### "Cannot verify developer"

This is normal for unsigned apps. Use **Method 1** (Right-click → Open) to bypass this safely.

## Why This Happens

- ImageToPDF is not signed with an Apple Developer certificate
- macOS Gatekeeper protects users by default
- Once you explicitly open it using the methods above, macOS remembers your choice
- The app is safe to use - it only accesses files you explicitly select

## Moving to Applications Folder

After successfully opening the app once:

1. Drag `ImageToPDF.app` to your **Applications** folder
2. You can now launch it normally from Launchpad or Spotlight

## Uninstalling

To remove ImageToPDF:

1. Drag `ImageToPDF.app` from Applications to Trash
2. Empty Trash

No other files or settings are left behind.

## Security Information

- ImageToPDF runs locally on your computer
- No data is sent to the internet
- The app only accesses images you explicitly select
- All PDF generation happens on your device
- Source code is available on GitHub

## Need Help?

If you're still having issues:
1. Check the [GitHub Issues](../../issues)
2. Create a new issue with details about the error
3. Include your macOS version (About This Mac)
