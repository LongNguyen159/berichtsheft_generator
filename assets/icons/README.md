# App Icons

This directory contains the application icons for different platforms.

## Required Files

Place your icon files in this directory with these exact names:

- **Windows**: `app_icon.ico` (ICO format)
- **macOS**: `app_icon.icns` (ICNS format)  
- **Linux**: `app_icon.png` (PNG format)

## Creating Icons

### From PNG to ICO (Windows)
You can use online converters or tools like:
- Online: https://convertio.co/png-ico/
- Command line: `magick convert icon.png -resize 256x256 app_icon.ico`

### From PNG to ICNS (macOS)
```bash
# Create iconset directory
mkdir app_icon.iconset

# Generate different sizes (you need a 1024x1024 PNG source)
sips -z 16 16 icon.png --out app_icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out app_icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon.png --out app_icon.iconset/icon_32x32.png
sips -z 64 64 icon.png --out app_icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon.png --out app_icon.iconset/icon_128x128.png
sips -z 256 256 icon.png --out app_icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon.png --out app_icon.iconset/icon_256x256.png
sips -z 512 512 icon.png --out app_icon.iconset/icon_256x256@2x.png
sips -z 512 512 icon.png --out app_icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out app_icon.iconset/icon_512x512@2x.png

# Create ICNS
iconutil -c icns app_icon.iconset
```

## Recommended Icon Specifications

- **Size**: 1024x1024 pixels (high resolution)
- **Format**: PNG with transparency support
- **Design**: Simple, clear, recognizable at small sizes
- **Colors**: High contrast, readable

## Notes

- The build script automatically detects your OS and uses the appropriate icon
- If no icon is found, the app will build with the default Python/PyInstaller icon
- Icons should be square (1:1 aspect ratio) for best results
