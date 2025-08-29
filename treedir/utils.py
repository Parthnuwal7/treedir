"""
Utility functions for TreeDir library.
"""

import os
import shutil
import tempfile
import datetime
from typing import Optional


def resolve_target_path(target: str) -> str:
    """
    Resolve target path, handling 'current' keyword.
    
    Args:
        target: Target path or 'current'
        
    Returns:
        Absolute path to target directory
    """
    if target == "current":
        return os.getcwd()
    
    return os.path.abspath(target)


def create_backup(target_path: str) -> str:
    """
    Create backup of target directory.
    
    Args:
        target_path: Path to directory to backup
        
    Returns:
        Path to backup directory
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target path does not exist: {target_path}")
    
    # Generate backup name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(target_path.rstrip('/\\'))
    backup_name = f"{base_name}_backup_{timestamp}"
    
    # Create backup in temp directory
    temp_dir = tempfile.gettempdir()
    backup_path = os.path.join(temp_dir, backup_name)
    
    if os.path.isdir(target_path):
        shutil.copytree(target_path, backup_path)
    else:
        shutil.copy2(target_path, backup_path)
    
    return backup_path


def validate_filename(filename: str) -> bool:
    """
    Validate if filename is safe for filesystem operations.
    
    Args:
        filename: Filename to validate
        
    Returns:
        True if filename is valid, False otherwise
    """
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        return False
    
    # Check for reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = filename.split('.')[0].upper()
    if name_without_ext in reserved_names:
        return False
    
    # Check for empty filename or filename with only dots/spaces
    if not filename.strip() or filename.strip().replace('.', '').replace(' ', '') == '':
        return False
    
    return True


def safe_remove(path: str) -> bool:
    """
    Safely remove file or directory.
    
    Args:
        path: Path to remove
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except Exception:
        return False


def ensure_directory_exists(path: str) -> bool:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False


def get_file_size_str(path: str) -> str:
    """
    Get human-readable file size.
    
    Args:
        path: File path
        
    Returns:
        Human-readable size string
    """
    try:
        size = os.path.getsize(path)
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        
        return f"{size:.1f} PB"
    except Exception:
        return "Unknown"


def is_empty_directory(path: str) -> bool:
    """
    Check if directory is empty.
    
    Args:
        path: Directory path
        
    Returns:
        True if directory is empty, False otherwise
    """
    try:
        return len(os.listdir(path)) == 0
    except Exception:
        return False


def count_items(path: str) -> tuple:
    """
    Count files and directories in path.
    
    Args:
        path: Directory path
        
    Returns:
        Tuple of (file_count, dir_count)
    """
    file_count = 0
    dir_count = 0
    
    try:
        for root, dirs, files in os.walk(path):
            file_count += len(files)
            dir_count += len(dirs)
    except Exception:
        pass
    
    return file_count, dir_count


def normalize_path_separators(path: str) -> str:
    """
    Normalize path separators for current OS.
    
    Args:
        path: Path with mixed separators
        
    Returns:
        Path with normalized separators
    """
    return os.path.normpath(path)


def get_common_path(paths: list) -> str:
    """
    Get common parent path from list of paths.
    
    Args:
        paths: List of file/directory paths
        
    Returns:
        Common parent path
    """
    if not paths:
        return ""
    
    return os.path.commonpath(paths)


def is_subdirectory(child: str, parent: str) -> bool:
    """
    Check if child is a subdirectory of parent.
    
    Args:
        child: Child directory path
        parent: Parent directory path
        
    Returns:
        True if child is subdirectory of parent
    """
    try:
        parent = os.path.abspath(parent)
        child = os.path.abspath(child)
        return child.startswith(parent + os.sep) or child == parent
    except Exception:
        return False


def get_relative_path_safe(path: str, start: str) -> Optional[str]:
    """
    Safely get relative path.
    
    Args:
        path: Target path
        start: Starting path
        
    Returns:
        Relative path or None if error
    """
    try:
        return os.path.relpath(path, start)
    except Exception:
        return None