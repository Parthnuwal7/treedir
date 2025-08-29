"""
Visualization module for TreeDir library.
"""

import os
import tempfile
import shutil
from typing import Dict, Callable, Any
from .utils import resolve_target_path
from .core import TreeDir


class TreeVisualizer:
    """Handle visualization and sandbox operations"""
    
    def __init__(self):
        pass
    
    def visualize(self, target: str = "current") -> str:
        """
        Visualize directory structure in tree format.
        
        Args:
            target: Target directory path or "current"
            
        Returns:
            String representation of directory tree
        """
        target_path = resolve_target_path(target)
        
        if not os.path.exists(target_path):
            return f"Path does not exist: {target_path}"
        
        tree_lines = []
        tree_lines.append(os.path.basename(target_path) + "/")
        
        self._build_tree(target_path, "", tree_lines, is_last=True)
        
        return "\n".join(tree_lines)
    
    def _build_tree(self, path: str, prefix: str, tree_lines: list, is_last: bool = True):
        """Recursively build tree visualization"""
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return
        
        # Separate directories and files
        dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        
        all_items = dirs + files
        
        for i, item in enumerate(all_items):
            is_last_item = (i == len(all_items) - 1)
            item_path = os.path.join(path, item)
            
            # Choose the appropriate tree characters
            if is_last_item:
                current_prefix = "└── "
                next_prefix = prefix + "    "
            else:
                current_prefix = "├── "
                next_prefix = prefix + "│   "
            
            # Add item to tree
            if os.path.isdir(item_path):
                tree_lines.append(f"{prefix}{current_prefix}{item}/")
                self._build_tree(item_path, next_prefix, tree_lines, is_last_item)
            else:
                tree_lines.append(f"{prefix}{current_prefix}{item}")
    
    def sandbox(self, operation_func: Callable, *args, **kwargs) -> str:
        """
        Visualize how directory will look after operation without actually executing it.
        
        Args:
            operation_func: Function to simulate (run, urun, etc.)
            *args: Arguments for the operation function
            **kwargs: Keyword arguments for the operation function
            
        Returns:
            String representation of resulting directory tree
        """
        # Extract target from args or kwargs
        target = kwargs.get('target', args[1] if len(args) > 1 else "current")
        target_path = resolve_target_path(target)
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix='treedir_sandbox_')
        
        try:
            # Copy current directory structure to temp
            if os.path.exists(target_path):
                temp_target = os.path.join(temp_dir, 'sandbox_target')
                shutil.copytree(target_path, temp_target)
            else:
                temp_target = os.path.join(temp_dir, 'sandbox_target')
                os.makedirs(temp_target)
            
            # Modify args to use temp directory
            new_args = list(args)
            if len(new_args) > 1:
                new_args[1] = temp_target
            new_kwargs = kwargs.copy()
            new_kwargs['target'] = temp_target
            
            # Execute operation in sandbox
            td = TreeDir()
            
            # Map function names to methods
            func_name = operation_func.__name__ if hasattr(operation_func, '__name__') else str(operation_func)
            
            if func_name == 'run' or operation_func == td.run:
                result = td.run(*new_args, **new_kwargs)
            elif func_name == 'urun' or operation_func == td.urun:
                result = td.urun(*new_args, **new_kwargs)
            elif func_name == 'reset' or operation_func == td.reset:
                result = td.reset(temp_target)
            else:
                raise ValueError(f"Unsupported operation for sandbox: {func_name}")
            
            if not result:
                return "Sandbox operation failed"
            
            # Visualize result
            sandbox_result = self.visualize(temp_target)
            return f"Sandbox Preview:\n{sandbox_result}"
        
        except Exception as e:
            return f"Sandbox error: {e}"
        
        finally:
            # Clean up temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def compare_structures(self, target1: str, target2: str) -> str:
        """
        Compare two directory structures side by side.
        
        Args:
            target1: First directory path
            target2: Second directory path
            
        Returns:
            String representation of comparison
        """
        tree1 = self.visualize(target1)
        tree2 = self.visualize(target2)
        
        lines1 = tree1.split('\n')
        lines2 = tree2.split('\n')
        
        max_lines = max(len(lines1), len(lines2))
        max_width1 = max(len(line) for line in lines1) if lines1 else 0
        
        comparison = []
        comparison.append(f"{'Structure 1':<{max_width1}} | Structure 2")
        comparison.append(f"{'-' * max_width1} | {'-' * max_width1}")
        
        for i in range(max_lines):
            line1 = lines1[i] if i < len(lines1) else ""
            line2 = lines2[i] if i < len(lines2) else ""
            
            comparison.append(f"{line1:<{max_width1}} | {line2}")
        
        return "\n".join(comparison)
    
    def structure_to_dict_string(self, target: str = "current") -> str:
        """
        Return directory structure as a formatted dictionary string.
        
        Args:
            target: Target directory path or "current"
            
        Returns:
            Formatted dictionary string representation
        """
        td = TreeDir()
        structure = td.get_structure_dict(target)
        return self._format_dict(structure, indent=0)
    
    def _format_dict(self, d: Dict, indent: int = 0) -> str:
        """Format dictionary with proper indentation"""
        if not d:
            return "{}"
        
        lines = ["{"]
        items = list(d.items())
        
        for i, (key, value) in enumerate(items):
            is_last = (i == len(items) - 1)
            spaces = "  " * (indent + 1)
            
            if value is None:
                line = f'{spaces}"{key}": null'
            elif isinstance(value, dict):
                if value:
                    nested = self._format_dict(value, indent + 1)
                    line = f'{spaces}"{key}": {nested}'
                else:
                    line = f'{spaces}"{key}": {{}}'
            else:
                line = f'{spaces}"{key}": "{value}"'
            
            if not is_last:
                line += ","
            
            lines.append(line)
        
        lines.append("  " * indent + "}")
        return "\n".join(lines)
    
    def generate_structure_file(self, target: str = "current", format_type: str = "tree") -> str:
        """
        Generate structure file content from existing directory.
        
        Args:
            target: Target directory path or "current"
            format_type: Output format ('tree', 'dict', or 'path')
            
        Returns:
            Structure file content as string
        """
        if format_type == "tree":
            return self.visualize(target)
        elif format_type == "dict":
            return self.structure_to_dict_string(target)
        elif format_type == "path":
            return self._generate_path_format(target)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_path_format(self, target: str) -> str:
        """Generate path format representation"""
        target_path = resolve_target_path(target)
        paths = []
        
        for root, dirs, files in os.walk(target_path):
            # Get relative path from target
            rel_root = os.path.relpath(root, target_path)
            if rel_root == ".":
                rel_root = ""
            
            # Add files
            for file in sorted(files):
                if rel_root:
                    paths.append(f"{rel_root}/{file}")
                else:
                    paths.append(file)
            
            # Add empty directories
            for dir_name in sorted(dirs):
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):  # Empty directory
                    if rel_root:
                        paths.append(f"{rel_root}/{dir_name}/")
                    else:
                        paths.append(f"{dir_name}/")
        
        return "\n".join(paths)