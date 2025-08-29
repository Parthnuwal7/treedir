#!/usr/bin/env python3
"""
Example usage of TreeDir library.
"""

import treedir
import os


def example_basic_usage():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===\n")
    
    # Example 1: Create structure from file
    print("1. Creating directory structure from file:")
    result = treedir.run('examples/sample_structure.txt', 'test_project')
    print(f"Result: {result}\n")
    
    # Example 2: Visualize the created structure
    print("2. Visualizing created structure:")
    tree_view = treedir.vis('test_project')
    print(tree_view)
    print()
    
    # Example 3: Find a file
    print("3. Finding files:")
    main_py = treedir.find('main.py', 'test_project')
    print(f"Found main.py at: {main_py}")
    
    config_py = treedir.findr('config.py', 'test_project')
    print(f"config.py relative path: {config_py}")
    print()


def example_sandbox_mode():
    """Sandbox mode examples"""
    print("=== Sandbox Mode Examples ===\n")
    
    # Preview changes before applying
    print("Preview of run operation:")
    preview = treedir.sandbox(treedir.run, 'examples/sample_structure.txt', 'sandbox_test')
    print(preview)
    print()
    
    # Preview unconditional run
    print("Preview of urun operation:")
    preview_urun = treedir.sandbox(treedir.urun, 'examples/sample_structure.txt', 'sandbox_test')
    print(preview_urun)
    print()


def example_advanced_usage():
    """Advanced usage with classes"""
    print("=== Advanced Usage Examples ===\n")
    
    # Using classes directly
    from treedir import TreeDir, TreeVisualizer, TreeParser
    
    td = TreeDir()
    tv = TreeVisualizer()
    tp = TreeParser()
    
    # Parse structure file
    print("1. Parsing structure file:")
    try:
        structure = tp.parse_file('examples/sample_structure.txt')
        print("Parsed structure successfully")
        print(f"Structure keys: {list(structure.keys())}")
    except Exception as e:
        print(f"Error parsing structure: {e}")
    print()
    
    # Generate structure file from existing directory
    print("2. Generating structure files:")
    if os.path.exists('test_project'):
        tree_format = tv.generate_structure_file('test_project', 'tree')
        print("Generated tree format:")
        print(tree_format[:200] + "..." if len(tree_format) > 200 else tree_format)
        
        dict_format = tv.generate_structure_file('test_project', 'dict')
        print("\nGenerated dict format:")
        print(dict_format[:200] + "..." if len(dict_format) > 200 else dict_format)
    print()


def example_error_handling():
    """Error handling examples"""
    print("=== Error Handling Examples ===\n")
    
    # Handle non-existent structure file
    print("1. Handling non-existent file:")
    try:
        result = treedir.run('non_existent.txt', 'test')
        print(f"Result: {result}")
    except FileNotFoundError as e:
        print(f"Caught expected error: {e}")
    print()
    
    # Handle invalid target
    print("2. Visualizing non-existent directory:")
    result = treedir.vis('non_existent_directory')
    print(f"Result: {result}")
    print()


def cleanup():
    """Clean up test directories"""
    import shutil
    
    test_dirs = ['test_project', 'sandbox_test', 'new_project']
    
    for dir_name in test_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Cleaned up: {dir_name}")
            except Exception as e:
                print(f"Failed to cleanup {dir_name}: {e}")


def main():
    """Run all examples"""
    print("TreeDir Library Examples")
    print("=" * 50)
    
    try:
        example_basic_usage()
        example_sandbox_mode()
        example_advanced_usage()
        example_error_handling()
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")
    finally:
        print("\nCleaning up test directories...")
        cleanup()
        print("Examples completed!")


if __name__ == "__main__":
    main()