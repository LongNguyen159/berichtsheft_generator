import platform
import subprocess
import sys
import os
import shutil


def cleanup_directories():
    """Clean up build and dist directories before packaging"""
    directories_to_clean = ['build', 'dist']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            print(f"Cleaning up {directory}/ directory...")
            try:
                shutil.rmtree(directory)
                print(f"✅ Removed {directory}/ directory")
            except Exception as e:
                print(f"❌ Error removing {directory}/ directory: {str(e)}")
                sys.exit(1)



def run_nicegui_pack():
    system = platform.system()
    print(f'Detected OS: {system}')

    # Check if nicegui is installed
    try:
        from nicegui import __version__ as nicegui_version
        print(f"Using NiceGUI version: {nicegui_version}")
    except ImportError:
        print("❌ Error: 'nicegui' is not installed in the current environment.")
        sys.exit(1)
    
    # Clean up old build artifacts first
    cleanup_directories()

    # Determine the correct path separator for --add-data based on OS
    path_separator = ';' if system == 'Windows' else ':'
    
    # Determine icon file based on OS
    icon_file = None
    if system == 'Windows':
        icon_path = 'assets/icons/app_icon.ico'
    elif system == 'Darwin':  # macOS
        icon_path = 'assets/icons/app_icon.icns'
    else:  # Linux
        icon_path = 'assets/icons/app_icon.png'

    # Check if icon file exists
    if os.path.exists(icon_path):
        icon_file = icon_path
        print(f"Using icon: {icon_file}")
    else:
        print(f"⚠️ Icon file not found: {icon_path}")
        print("App will be built without custom icon")
    
    cmd = [
        'nicegui-pack', 
        '--onefile', 
        '--windowed', # console off
        '--name', 'Report Generator',
        '--add-data', f'assets/templates{path_separator}assets/templates',  # Include templates folder
    ]
    
    # Add icon if available
    if icon_file:
        cmd.extend(['--icon', icon_file])

    cmd.append('src/main.py')

    print(f'Running command: {" ".join(cmd)}')
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Check if PyInstaller actually succeeded by looking for error messages
        if "ERROR:" in result.stdout or "ERROR:" in result.stderr:
            print('❌ Build failed - PyInstaller encountered errors.')
            print(f'Output: {result.stdout}')
            print(f'Errors: {result.stderr}')
            sys.exit(1)
        
        print('✅ Build completed successfully.')
        print('Your application is available in the dist/ directory')
    except subprocess.CalledProcessError as e:
        print('❌ Build failed.')
        print(f'Return code: {e.returncode}')
        if e.stdout:
            print(f'Output: {e.stdout}')
        if e.stderr:
            print(f'Errors: {e.stderr}')
        sys.exit(e.returncode)
    except Exception as e:
        print('❌ Build failed - Unexpected error occurred.')
        print(f'Error type: {type(e).__name__}')
        print(f'Error message: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    run_nicegui_pack()