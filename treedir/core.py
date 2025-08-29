"""
Core functionality for TreeDir library.
"""

import os
import shutil
from typing import Dict, List, Union, Optional
from .parser import TreeParser
from .utils import resolve_target_path, create_backup


class TreeDir:
    """Main class for directory structure operations"""
    
    def __init__(self):
        self.parser = TreeParser()
    
    def run(self, structure_file: str, target: str = "current") -> bool:
        """
        Additive file system execution.
        Only adds new files/directories, preserves existing ones.
        
        Args:
            structure_file: Path to structure definition file
            target: Target directory path or "current"
            
        Returns:
            True if successful, False otherwise
        """
        try:
            target_path = resolve_target_path(target)
            structure = self.parser.parse_file(structure_file)
            
            if not self.parser.validate_structure(structure):
                raise ValueError("Invalid structure format")
            
            return self._create_structure(structure, target_path, mode='additive')
        
        except Exception as e:
            print(f"Error in run(): {e}")
            return False
    
    def urun(self, structure_file: str, target: str = "current") -> bool:
        """
        Unconditional run - strictly enforce structure.
        Keeps common files intact, removes files not in structure.
        
        Args:
            structure_file: Path to structure definition file
            target: Target directory path or "current"
            
        Returns:
            True if successful, False otherwise
        """
        try:
            target_path = resolve_target_path(target)
            structure = self.parser.parse_file(structure_file)
            
            if not self.parser.validate_structure(structure):
                raise ValueError("Invalid structure format")
            
            # Create backup before unconditional run
            backup_path = create_backup(target_path)
            print(f"Backup created at: {backup_path}")
            
            return self._create_structure(structure, target_path, mode='strict')
        
        except Exception as e:
            print(f"Error in urun(): {e}")
            return False
    
    def reset(self, target: str = "current") -> bool:
        """
        Reset target folder (remove all contents).
        
        Args:
            target: Target directory path or "current"
            
        Returns:
            True if successful, False otherwise
        """
        try:
            target_path = resolve_target_path(target)
            
            if not os.path.exists(target_path):
                print(f"Target path does not exist: {target_path}")
                return False
            
            # Create backup before reset
            backup_path = create_backup(target_path)
            print(f"Backup created at: {backup_path}")
            
            # Remove all contents
            for item in os.listdir(target_path):
                item_path = os.path.join(target_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            
            print(f"Reset completed: {target_path}")
            return True
        
        except Exception as e:
            print(f"Error in reset(): {e}")
            return False
    
    def find(self, filename: str, target: str = "current") -> Optional[str]:
        """
        Find file/folder and return absolute path.
        
        Args:
            filename: Name of file/folder to find
            target: Target directory path or "current"
            
        Returns:
            Absolute path if found, None otherwise
        """
        target_path = resolve_target_path(target)
        
        for root, dirs, files in os.walk(target_path):
            # Check files
            if filename in files:
                return os.path.abspath(os.path.join(root, filename))
            # Check directories
            if filename in dirs:
                return os.path.abspath(os.path.join(root, filename))
        
        return None
    
    def findr(self, filename: str, target: str = "current") -> Optional[str]:
        """
        Find file/folder and return relative path.
        
        Args:
            filename: Name of file/folder to find
            target: Target directory path or "current"
            
        Returns:
            Relative path if found, None otherwise
        """
        absolute_path = self.find(filename, target)
        if absolute_path:
            target_path = resolve_target_path(target)
            return os.path.relpath(absolute_path, target_path)
        return None
    
    def _create_structure(self, structure: Dict, target_path: str, mode: str = 'additive') -> bool:
        """
        Create directory structure based on dictionary.
        
        Args:
            structure: Dictionary representing directory structure
            target_path: Target directory path
            mode: 'additive' or 'strict'
            
        Returns:
            True if successful
        """
        # Ensure target directory exists
        os.makedirs(target_path, exist_ok=True)
        
        if mode == 'strict':
            # Remove files/directories not in structure
            existing_items = set(os.listdir(target_path))
            structure_items = set(structure.keys())
            
            for item in existing_items - structure_items:
                item_path = os.path.join(target_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                print(f"Removed: {item_path}")
        
        # Create structure
        self._create_items(structure, target_path, mode)
        return True
    
    def _create_items(self, structure: Dict, current_path: str, mode: str):
        """Recursively create items from structure dictionary"""
        for name, content in structure.items():
            item_path = os.path.join(current_path, name)
            
            if content is None:  # File
                if not os.path.exists(item_path):
                    # Create empty file
                    with open(item_path, 'w') as f:
                        pass
                    print(f"Created file: {item_path}")
                elif mode == 'additive':
                    print(f"File exists, skipped: {item_path}")
            
            elif isinstance(content, dict):  # Directory
                if not os.path.exists(item_path):
                    os.makedirs(item_path)
                    print(f"Created directory: {item_path}")
                elif mode == 'additive':
                    print(f"Directory exists, updating: {item_path}")
                
                # Recursively create subdirectories and files
                if mode == 'strict' and os.path.exists(item_path):
                    # Remove items not in structure
                    existing_items = set(os.listdir(item_path))
                    structure_items = set(content.keys())
                    
                    for item in existing_items - structure_items:
                        sub_item_path = os.path.join(item_path, item)
                        if os.path.isdir(sub_item_path):
                            shutil.rmtree(sub_item_path)
                        else:
                            os.remove(sub_item_path)
                        print(f"Removed: {sub_item_path}")
                
                self._create_items(content, item_path, mode)
    
    def get_structure_dict(self, target: str = "current") -> Dict:
        """
        Get current directory structure as dictionary.
        
        Args:
            target: Target directory path or "current"
            
        Returns:
            Dictionary representing current structure
        """
        target_path = resolve_target_path(target)
        
        if not os.path.exists(target_path):
            return {}
        
        return self._scan_directory(target_path)
    
    def _scan_directory(self, path: str) -> Dict:
        """Recursively scan directory and return structure dictionary"""
        structure = {}
        
        if not os.path.isdir(path):
            return structure
        
        try:
            items = os.listdir(path)
        except PermissionError:
            return structure
        
        for item in sorted(items):
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                structure[item] = self._scan_directory(item_path)
            else:
                structure[item] = None
        
        return structure