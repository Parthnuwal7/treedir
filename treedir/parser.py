"""
Tree structure parser module for handling different directory structure formats.
"""

import os
import re
from typing import Dict, List, Union, Tuple


class TreeParser:
    """Parse directory structures from various text formats"""
    
    def __init__(self):
        self.supported_formats = ['tree', 'dict', 'path']
    
    def parse_file(self, structure_file: str) -> Dict:
        """
        Parse structure file and return directory structure dictionary
        
        Args:
            structure_file: Path to the structure file
            
        Returns:
            Dictionary representing the directory structure
        """
        if not os.path.exists(structure_file):
            raise FileNotFoundError(f"Structure file not found: {structure_file}")
        
        with open(structure_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Detect format and parse accordingly
        format_type = self._detect_format(content)
        
        if format_type == 'tree':
            return self._parse_tree_format(content)
        elif format_type == 'dict':
            return self._parse_dict_format(content)
        elif format_type == 'path':
            return self._parse_path_format(content)
        else:
            raise ValueError(f"Unsupported or unrecognized format in {structure_file}")
    
    def _detect_format(self, content: str) -> str:
        """Detect the format of the structure content"""
        lines = content.split('\n')
        
        # Check for tree format (contains ├── or └── or │)
        if any(re.search(r'[├└│]', line) for line in lines):
            return 'tree'
        
        # Check for dictionary-like format (contains { } [ ])
        if '{' in content and '}' in content:
            return 'dict'
        
        # Default to path format (simple file paths)
        return 'path'
    
    def _parse_tree_format(self, content: str) -> Dict:
        """
        Parse tree command output format
        Example:
        project/
        ├── src/
        │   ├── main.py
        │   └── utils.py
        └── README.md
        """
        lines = content.split('\n')
        structure = {}
        stack = [(structure, 0)]  # (current_dict, level)
        
        for line in lines:
            if not line.strip():
                continue
            
            # Calculate indentation level
            clean_line = re.sub(r'[├└│─\s]+', '', line)
            if not clean_line:
                continue
            
            # Count the depth based on tree symbols
            level = 0
            for char in line:
                if char in '├└│':
                    level += 1
                elif char == ' ':
                    continue
                else:
                    break
            
            # Adjust level based on tree structure
            if '├──' in line or '└──' in line:
                level = line.find('├') if '├' in line else line.find('└')
                level = level // 4  # Assume 4 spaces per level
            
            name = clean_line.strip()
            is_dir = name.endswith('/')
            if is_dir:
                name = name[:-1]  # Remove trailing slash
            
            # Find the correct parent dictionary
            while len(stack) > level + 1:
                stack.pop()
            
            current_dict = stack[-1][0]
            
            if is_dir:
                current_dict[name] = {}
                stack.append((current_dict[name], level + 1))
            else:
                current_dict[name] = None  # File
        
        return structure
    
    def _parse_dict_format(self, content: str) -> Dict:
        """
        Parse dictionary-like format
        Example:
        {
          "src": {
            "main.py": null,
            "utils.py": null
          },
          "README.md": null
        }
        """
        try:
            import json
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to parse as Python dictionary
            try:
                return eval(content)
            except:
                raise ValueError("Invalid dictionary format")
    
    def _parse_path_format(self, content: str) -> Dict:
        """
        Parse simple path format
        Example:
        src/main.py
        src/utils.py
        README.md
        """
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        structure = {}
        
        for path in lines:
            parts = path.split('/')
            current = structure
            
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Last part
                    # Check if it's a file (has extension) or directory
                    if '.' in part and not part.startswith('.'):
                        current[part] = None  # File
                    else:
                        if part not in current:
                            current[part] = {}  # Directory
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        
        return structure
    
    def structure_to_paths(self, structure: Dict, base_path: str = "") -> List[str]:
        """Convert structure dictionary to list of file paths"""
        paths = []
        
        for name, content in structure.items():
            current_path = os.path.join(base_path, name) if base_path else name
            
            if content is None:  # File
                paths.append(current_path)
            elif isinstance(content, dict):  # Directory
                paths.append(current_path + "/")  # Mark as directory
                paths.extend(self.structure_to_paths(content, current_path))
        
        return paths
    
    def validate_structure(self, structure: Dict) -> bool:
        """Validate the parsed structure"""
        if not isinstance(structure, dict):
            return False
        
        for key, value in structure.items():
            if not isinstance(key, str):
                return False
            if value is not None and not isinstance(value, dict):
                return False
            if isinstance(value, dict) and not self.validate_structure(value):
                return False
        
        return True