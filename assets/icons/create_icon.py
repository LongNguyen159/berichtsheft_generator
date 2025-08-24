#!/usr/bin/env python3
"""
Simple script to generate a basic app icon using Python PIL/Pillow
Run this script to create a sample icon: python create_icon.py
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_report_icon(size=1024):
        """Create a simple report/document icon"""
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        paper_color = (255, 255, 255, 255)  # White paper
        border_color = (200, 200, 200, 255)  # Light gray border
        lines_color = (180, 180, 180, 255)   # Gray lines
        accent_color = (52, 152, 219, 255)   # Blue accent
        
        # Document dimensions
        margin = size // 8
        doc_width = size - 2 * margin
        doc_height = int(doc_width * 1.3)  # A4-ish ratio
        doc_x = margin
        doc_y = (size - doc_height) // 2
        
        # Draw document shadow
        shadow_offset = size // 40
        draw.rectangle([
            doc_x + shadow_offset, doc_y + shadow_offset,
            doc_x + doc_width + shadow_offset, doc_y + doc_height + shadow_offset
        ], fill=(0, 0, 0, 80))
        
        # Draw document
        draw.rectangle([doc_x, doc_y, doc_x + doc_width, doc_y + doc_height], 
                      fill=paper_color, outline=border_color, width=size//200)
        
        # Draw folded corner
        corner_size = size // 8
        corner_points = [
            (doc_x + doc_width - corner_size, doc_y),
            (doc_x + doc_width, doc_y + corner_size),
            (doc_x + doc_width, doc_y),
        ]
        draw.polygon(corner_points, fill=border_color)
        
        # Draw lines on document
        line_spacing = size // 20
        line_start_x = doc_x + size // 16
        line_end_x = doc_x + doc_width - size // 16
        
        for i in range(5):
            y = doc_y + size // 6 + (i * line_spacing)
            if i == 0:  # Header line
                draw.rectangle([line_start_x, y, line_end_x, y + size//80], fill=accent_color)
            else:  # Regular lines
                draw.line([line_start_x, y, line_end_x, y], fill=lines_color, width=size//200)
        
        return img
    
    def main():
        # Create the icon
        icon = create_report_icon(1024)
        
        # Save as PNG
        png_path = "app_icon.png"
        icon.save(png_path, "PNG")
        print(f"✅ Created PNG icon: {png_path}")
        
        # Try to create ICO for Windows (requires PIL)
        try:
            # Create multiple sizes for ICO
            sizes = [16, 32, 48, 64, 128, 256]
            ico_images = []
            for size in sizes:
                resized = icon.resize((size, size), Image.Resampling.LANCZOS)
                ico_images.append(resized)
            
            ico_path = "app_icon.ico"
            ico_images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in ico_images])
            print(f"✅ Created ICO icon: {ico_path}")
        except Exception as e:
            print(f"⚠️  Could not create ICO: {e}")
        
        print("\nTo create ICNS for macOS, use the commands in README.md")
        print("Or use online converters to convert the PNG to ICNS format")

    if __name__ == "__main__":
        main()
        
except ImportError:
    print("❌ PIL/Pillow not installed. Install it with: pip install Pillow")
    print("Or manually create your icon files and place them in this directory")
