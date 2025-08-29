import os

structure = {
    "treedir": {
        "treedir": [
            "__init__.py",
            "core.py",
            "parser.py",
            "visualizer.py",
            "utils.py"
        ],
        "tests": [
            "__init__.py",
            "test_core.py",
            "test_parser.py",
            "test_visualizer.py"
        ],
        "examples": [
            "sample_structure.txt",
            "example_usage.py"
        ],
        ".": [
            "setup.py",
            "pyproject.toml",
            "README.md",
            "LICENSE",
            "MANIFEST.in",
            "requirements.txt"
        ]
    }
}

def create_structure(base_path, structure):
    for key, value in structure.items():
        key_path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(key_path, exist_ok=True)
            create_structure(key_path, value)
        elif isinstance(value, list):
            os.makedirs(base_path, exist_ok=True)
            for file_name in value:
                file_path = os.path.join(base_path, key, file_name) if key != "." else os.path.join(base_path, file_name)
                if key != ".":
                    os.makedirs(os.path.join(base_path, key), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write("")  # create empty file

# Run the function
create_structure(".", structure["treedir"])
