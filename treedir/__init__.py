"""
TreeDir - Directory Structure Parser and Manager

A Python library for parsing directory structures from text files and 
implementing them in target folders with various operation modes.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import TreeDir
from .parser import TreeParser
from .visualizer import TreeVisualizer

# Main API functions
def run(structure_file, target="current"):
    """Additive file system execution"""
    td = TreeDir()
    return td.run(structure_file, target)

def urun(structure_file, target="current"):
    """Unconditional run - strictly enforce structure"""
    td = TreeDir()
    return td.urun(structure_file, target)

def reset(target="current"):
    """Reset target folder"""
    td = TreeDir()
    return td.reset(target)

def vis(target="current"):
    """Visualize directory structure"""
    tv = TreeVisualizer()
    return tv.visualize(target)

def find(filename, target="current"):
    """Find file/folder and return absolute path"""
    td = TreeDir()
    return td.find(filename, target)

def findr(filename, target="current"):
    """Find file/folder and return relative path"""
    td = TreeDir()
    return td.findr(filename, target)

def sandbox(operation_func, *args, **kwargs):
    """Visualize how directory will look after changes"""
    tv = TreeVisualizer()
    return tv.sandbox(operation_func, *args, **kwargs)

__all__ = [
    'TreeDir', 'TreeParser', 'TreeVisualizer',
    'run', 'urun', 'reset', 'vis', 'find', 'findr', 'sandbox'
]