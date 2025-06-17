"""
UnRAR utilities for handling RAR file extraction.
"""
import os
import subprocess
import rarfile

class UnRAR:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.installer_path = os.path.join(self.script_dir, "winrar-x64-711.exe")
        self.installed = False
        self._setup()
    
    def _setup(self):
        """Set up UnRAR by installing WinRAR if needed."""
        if not self._check_installation():
            self._install_winrar()
            self._check_installation()
    
    def _check_installation(self):
        """Check if WinRAR is installed and configure rarfile."""
        try:
            # Check common installation paths
            possible_paths = [
                r"C:\Program Files\WinRAR\UnRAR.exe",
                r"C:\Program Files (x86)\WinRAR\UnRAR.exe",
                r"C:\Program Files\WinRAR\Rar.exe",
                r"C:\Program Files (x86)\WinRAR\Rar.exe"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    rarfile.UNRAR_TOOL = path
                    self.installed = True
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _install_winrar(self):
        """Install WinRAR using the local installer."""
        try:
            if not os.path.exists(self.installer_path):
                return False
                
            # Run the installer silently
            subprocess.run([self.installer_path, "/S"], check=True)
            return True
            
        except Exception as e:
            print(f"Failed to install WinRAR: {str(e)}")
            return False
    
    def is_installed(self):
        """Check if WinRAR is installed and ready to use."""
        return self.installed
    
    def get_unrar_path(self):
        """Get the path to the UnRAR executable."""
        return rarfile.UNRAR_TOOL if self.installed else None
