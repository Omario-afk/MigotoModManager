"""
Archive extraction utilities for ZIP and RAR files.
"""
import os
import zipfile
import rarfile
from tkinter import messagebox
from utils.zip import UnRAR
import subprocess

# Create a single UnRAR instance for the module
_unrar = UnRAR()

def install_winrar():
    """
    Install WinRAR using the installer in the same directory.
    
    Returns:
        bool: True if installation was successful or already installed, False otherwise
    """
    try:
        # Check for installer in the executables directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        executables_dir = os.path.join(script_dir, "executables")
        installer_path = os.path.join(executables_dir, "winrar-x64-711.exe")
        
        if not os.path.exists(installer_path):
            return False
            
        # Run the installer silently
        subprocess.run([installer_path, "/S"], check=True)
        return True
        
    except Exception as e:
        print(f"Failed to install WinRAR: {str(e)}")
        return False

def check_unrar_installed():
    """
    Check if UnRAR is installed and properly configured.
    First checks for unrar.exe in the executables directory.
    If not found, attempts to install WinRAR from the local installer.
    
    Returns:
        bool: True if UnRAR is available, False otherwise
    """
    try:
        # First check for unrar.exe in the executables directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        executables_dir = os.path.join(script_dir, "executables")
        local_unrar = os.path.join(executables_dir, "UnRAR.exe")
        if os.path.exists(local_unrar):
            rarfile.UNRAR_TOOL = local_unrar
            return True
            
        # Also check for Rar.exe in the executables directory
        local_rar = os.path.join(executables_dir, "Rar.exe")
        if os.path.exists(local_rar):
            rarfile.UNRAR_TOOL = local_rar
            return True
            
        # If not found locally, check common installation paths
        if os.name == 'nt':  # Windows
            # Common installation paths for WinRAR
            possible_paths = [
                r"C:\Program Files\WinRAR\UnRAR.exe",
                r"C:\Program Files (x86)\WinRAR\UnRAR.exe",
                r"C:\Program Files\WinRAR\Rar.exe",
                r"C:\Program Files (x86)\WinRAR\Rar.exe"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    rarfile.UNRAR_TOOL = path
                    return True
            
            # If not found in common paths, try to install WinRAR
            if install_winrar():
                # Check again after installation
                for path in possible_paths:
                    if os.path.exists(path):
                        rarfile.UNRAR_TOOL = path
                        return True
                    
            # If still not found, check if it's in PATH
            rarfile.UNRAR_TOOL = "unrar"  # Try using PATH
            return True
            
        else:  # Linux/Mac
            rarfile.UNRAR_TOOL = "unrar"  # Should be in PATH
            return True
            
    except Exception:
        return False

def extract_archive(archive_path, extract_to=None, progress_window=None):
    """
    Extract a ZIP or RAR archive to the specified directory.
    
    Args:
        archive_path (str): Path to the archive file
        extract_to (str, optional): Directory to extract to. If None, creates a directory named after the archive.
        progress_window: Optional progress window to update
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        if progress_window:
            progress_window.show_error(f"Archive not found: {archive_path}")
        return False
        
    # If no extract directory specified, create one named after the archive
    if extract_to is None:
        archive_name = os.path.splitext(os.path.basename(archive_path))[0]
        extract_to = os.path.join(os.path.dirname(archive_path), archive_name)
    else:
        # If extract_to is provided, create a subfolder named after the archive
        archive_name = os.path.splitext(os.path.basename(archive_path))[0]
        extract_to = os.path.join(extract_to, archive_name)
        
    # Create extract directory if it doesn't exist
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    
    try:
        # Get file extension
        _, ext = os.path.splitext(archive_path.lower())
        
        success = False
        if ext == '.zip':
            success = extract_zip(archive_path, extract_to)
        elif ext == '.rar':
            if not _unrar.is_installed():
                error_msg = (
                    "UnRAR is not installed or not found. Please install WinRAR (Windows) or unrar (Linux/Mac).\n\n"
                    "Windows: Download and install WinRAR from https://www.win-rar.com/\n"
                )
                if progress_window:
                    progress_window.show_error(error_msg)
                return False
            success = extract_rar(archive_path, extract_to)
        else:
            error_msg = f"Unsupported archive format: {ext}"
            if progress_window:
                progress_window.show_error(error_msg)
            return False
            
        # If extraction was successful and delete_after_extract is enabled, delete the archive
        if success:
            from config.settings import load_data
            settings = load_data()
            if settings.get("archive_settings", {}).get("delete_after_extract", 0) == 1:
                try:
                    os.remove(archive_path)
                except Exception as e:
                    print(f"Failed to delete archive: {str(e)}")
            
        return success
            
    except Exception as e:
        error_msg = f"Failed to extract archive: {str(e)}"
        if progress_window:
            progress_window.show_error(error_msg)
        return False

def extract_zip(zip_path, extract_to):
    """
    Extract a ZIP file to the specified directory.
    
    Args:
        zip_path (str): Path to the ZIP file
        extract_to (str): Directory to extract to
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all contents directly to the specified directory
            zip_ref.extractall(extract_to)
        return True
        
    except Exception as e:
        print(f"Failed to extract ZIP: {str(e)}")
        return False

def extract_rar(rar_path, extract_to):
    """
    Extract a RAR file to the specified directory.
    
    Args:
        rar_path (str): Path to the RAR file
        extract_to (str): Directory to extract to
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with rarfile.RarFile(rar_path, 'r') as rar_ref:
            # Extract all contents directly to the specified directory
            rar_ref.extractall(extract_to)
        return True
        
    except Exception as e:
        print(f"Failed to extract RAR: {str(e)}")
        return False

