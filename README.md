# TreeDir - Directory Structure Parser and Manager

[![PyPI version](https://badge.fury.io/py/treedir.svg)](https://badge.fury.io/py/treedir)
[![Python Support](https://img.shields.io/pypi/pyversions/treedir.svg)](https://pypi.org/project/treedir/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for parsing directory structures from text files and implementing them in target folders with various operation modes.

## Features

- **Multiple Input Formats**: Support for tree format, dictionary format, and simple path format
- **Flexible Operations**: Additive and strict enforcement modes
- **Visualization**: Tree-style visualization of directory structures
- **Sandbox Mode**: Preview changes before applying them
- **Search Functions**: Find files and folders with absolute or relative paths
- **Backup Creation**: Automatic backups before destructive operations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
pip install treedir-py
```

## Quick Start

```python
import treedir

# Create directory structure from file (additive mode)
treedir.run('structure.txt', 'my_project')

# Strictly enforce structure (removes extra files)
treedir.urun('structure.txt', 'my_project')

# Visualize current directory
print(treedir.vis('my_project'))

# Find a file
path = treedir.find('main.py', 'my_project')

# Preview changes before applying
preview = treedir.sandbox(treedir.run, 'structure.txt', 'my_project')
print(preview)
```

## Supported Input Formats

### Tree Format
```
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

### Dictionary Format
```json
{
  "src": {
    "main.py": null,
    "utils.py": null
  },
  "tests": {
    "test_main.py": null
  },
  "README.md": null
}
```

### Path Format
```
src/main.py
src/utils.py
tests/test_main.py
README.md
```

## API Reference

### Core Functions

#### `run(structure_file, target="current")`
Additive file system execution. Only adds new files/directories, preserves existing ones.

**Parameters:**
- `structure_file` (str): Path to structure definition file
- `target` (str): Target directory path or "current" for current directory

**Returns:** `bool` - True if successful

#### `urun(structure_file, target="current")`
Unconditional run - strictly enforce structure. Keeps common files intact but removes files not in the structure.

**Parameters:**
- `structure_file` (str): Path to structure definition file
- `target` (str): Target directory path or "current" for current directory

**Returns:** `bool` - True if successful

#### `reset(target="current")`
Reset target folder (remove all contents).

**Parameters:**
- `target` (str): Target directory path or "current" for current directory

**Returns:** `bool` - True if successful

#### `vis(target="current")`
Visualize directory structure in tree format.

**Parameters:**
- `target` (str): Target directory path or "current" for current directory

**Returns:** `str` - Tree representation of directory structure

#### `find(filename, target="current")`
Find file/folder and return absolute path.

**Parameters:**
- `filename` (str): Name of file/folder to find
- `target` (str): Target directory path or "current" for current directory

**Returns:** `str` or `None` - Absolute path if found, None otherwise

#### `findr(filename, target="current")`
Find file/folder and return relative path.

**Parameters:**
- `filename` (str): Name of file/folder to find
- `target` (str): Target directory path or "current" for current directory

**Returns:** `str` or `None` - Relative path if found, None otherwise

#### `sandbox(operation_func, *args, **kwargs)`
Visualize how directory will look after changes without actually executing them.

**Parameters:**
- `operation_func`: Function to simulate (run, urun, etc.)
- `*args`: Arguments for the operation function
- `**kwargs`: Keyword arguments for the operation function

**Returns:** `str` - Preview of resulting directory tree

## Advanced Usage

### Using Classes Directly

```python
from treedir import TreeDir, TreeParser, TreeVisualizer

# Initialize components
td = TreeDir()
parser = TreeParser()
visualizer = TreeVisualizer()

# Parse structure file
structure = parser.parse_file('my_structure.txt')

# Create structure
td._create_structure(structure, '/path/to/target', mode='additive')

# Compare two directories
comparison = visualizer.compare_structures('dir1', 'dir2')
print(comparison)
```

### Generating Structure Files

```python
from treedir import TreeVisualizer

tv = TreeVisualizer()

# Generate tree format from existing directory
tree_content = tv.generate_structure_file('my_project', 'tree')

# Generate dictionary format
dict_content = tv.generate_structure_file('my_project', 'dict')

# Generate path format
path_content = tv.generate_structure_file('my_project', 'path')
```

### Error Handling

```python
import treedir

try:
    result = treedir.run('structure.txt', 'target_folder')
    if result:
        print("Structure created successfully!")
    else:
        print("Failed to create structure")
except FileNotFoundError:
    print("Structure file not found")
except ValueError as e:
    print(f"Invalid structure format: {e}")
```

## Examples

### Example 1: Basic Project Setup

Create a `project_structure.txt`:
```
my_app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── README.md
├── requirements.txt
└── setup.py
```

Run:
```python
import treedir

# Create the structure
treedir.run('project_structure.txt', 'new_project')

# Visualize result
print(treedir.vis('new_project'))
```

### Example 2: Using Sandbox Mode

```python
import treedir

# Preview what will happen
preview = treedir.sandbox(treedir.run, 'structure.txt', 'test_folder')
print("Preview:")
print(preview)

# If satisfied, apply changes
treedir.run('structure.txt', 'test_folder')
```

### Example 3: Finding Files

```python
import treedir

# Find a specific file
main_py_path = treedir.find('main.py', 'my_project')
if main_py_path:
    print(f"Found main.py at: {main_py_path}")

# Get relative path
rel_path = treedir.findr('main.py', 'my_project')
print(f"Relative path: {rel_path}")
```

## Safety Features

- **Automatic Backups**: `urun()` and `reset()` automatically create backups
- **Sandbox Mode**: Preview changes before applying them
- **Path Validation**: Validates file and directory names
- **Error Handling**: Comprehensive error handling and reporting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0
- Initial release
- Support for tree, dictionary, and path formats
- Core functionality: run, urun, reset, vis, find, findr, sandbox
- Automatic backup creation
- Cross-platform compatibility