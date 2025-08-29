#!/usr/bin/env python3
"""
Command-line interface for TreeDir library.
"""

import argparse
import sys
import os
from . import run, urun, reset, vis, find, findr, sandbox
from .visualizer import TreeVisualizer


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='TreeDir - Directory Structure Parser and Manager',
        epilog='Examples:\n'
               '  treedir run structure.txt my_project\n'
               '  treedir vis .\n'
               '  treedir find main.py my_project\n'
               '  treedir sandbox run structure.txt test_dir',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Create directory structure (additive mode)')
    run_parser.add_argument('structure_file', help='Path to structure definition file')
    run_parser.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    
    # Urun command
    urun_parser = subparsers.add_parser('urun', help='Create directory structure (strict mode)')
    urun_parser.add_argument('structure_file', help='Path to structure definition file')
    urun_parser.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset target directory')
    reset_parser.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    reset_parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompt')
    
    # Vis command
    vis_parser = subparsers.add_parser('vis', help='Visualize directory structure')
    vis_parser.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    vis_parser.add_argument('--format', choices=['tree', 'dict', 'path'], default='tree',
                           help='Output format (default: tree)')
    
    # Find command
    find_parser = subparsers.add_parser('find', help='Find file or directory')
    find_parser.add_argument('filename', help='Name of file/directory to find')
    find_parser.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    find_parser.add_argument('--relative', '-r', action='store_true', help='Show relative path')
    
    # Sandbox command
    sandbox_parser = subparsers.add_parser('sandbox', help='Preview changes without applying them')
    sandbox_subparsers = sandbox_parser.add_subparsers(dest='sandbox_command', help='Operation to preview')
    
    sandbox_run = sandbox_subparsers.add_parser('run', help='Preview run operation')
    sandbox_run.add_argument('structure_file', help='Path to structure definition file')
    sandbox_run.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    
    sandbox_urun = sandbox_subparsers.add_parser('urun', help='Preview urun operation')
    sandbox_urun.add_argument('structure_file', help='Path to structure definition file')
    sandbox_urun.add_argument('target', nargs='?', default='current', help='Target directory (default: current)')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate structure file from existing directory')
    gen_parser.add_argument('target', nargs='?', default='current', help='Source directory (default: current)')
    gen_parser.add_argument('--format', choices=['tree', 'dict', 'path'], default='tree',
                           help='Output format (default: tree)')
    gen_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return execute_command(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def execute_command(args):
    """Execute the specified command"""
    
    if args.command == 'run':
        result = run(args.structure_file, args.target)
        if result:
            print(f"✓ Structure created successfully in '{args.target}'")
            return 0
        else:
            print("✗ Failed to create structure", file=sys.stderr)
            return 1
    
    elif args.command == 'urun':
        if not confirm_destructive_operation('urun', args.target):
            return 1
        
        result = urun(args.structure_file, args.target)
        if result:
            print(f"✓ Structure enforced successfully in '{args.target}'")
            return 0
        else:
            print("✗ Failed to enforce structure", file=sys.stderr)
            return 1
    
    elif args.command == 'reset':
        if not hasattr(args, 'confirm') or not args.confirm:
            if not confirm_destructive_operation('reset', args.target):
                return 1
        
        result = reset(args.target)
        if result:
            print(f"✓ Directory '{args.target}' reset successfully")
            return 0
        else:
            print("✗ Failed to reset directory", file=sys.stderr)
            return 1
    
    elif args.command == 'vis':
        if args.format == 'tree':
            result = vis(args.target)
        else:
            tv = TreeVisualizer()
            result = tv.generate_structure_file(args.target, args.format)
        
        print(result)
        return 0
    
    elif args.command == 'find':
        if args.relative:
            result = findr(args.filename, args.target)
        else:
            result = find(args.filename, args.target)
        
        if result:
            print(result)
            return 0
        else:
            print(f"✗ '{args.filename}' not found in '{args.target}'", file=sys.stderr)
            return 1
    
    elif args.command == 'sandbox':
        if args.sandbox_command == 'run':
            result = sandbox(run, args.structure_file, args.target)
        elif args.sandbox_command == 'urun':
            result = sandbox(urun, args.structure_file, args.target)
        else:
            print("✗ Invalid sandbox command", file=sys.stderr)
            return 1
        
        print(result)
        return 0
    
    elif args.command == 'generate':
        tv = TreeVisualizer()
        result = tv.generate_structure_file(args.target, args.format)
        
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✓ Structure file saved to '{args.output}'")
            except Exception as e:
                print(f"✗ Failed to save file: {e}", file=sys.stderr)
                return 1
        else:
            print(result)
        
        return 0
    
    elif args.command == 'version':
        from . import __version__
        print(f"TreeDir {__version__}")
        return 0
    
    else:
        print(f"✗ Unknown command: {args.command}", file=sys.stderr)
        return 1


def confirm_destructive_operation(operation: str, target: str) -> bool:
    """Confirm destructive operations with user"""
    target_display = target if target != 'current' else 'current directory'
    
    print(f"⚠️  Warning: '{operation}' will modify/delete files in '{target_display}'")
    print("   A backup will be created automatically.")
    
    try:
        response = input("Do you want to continue? (y/N): ").strip().lower()
        return response in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        return False


if __name__ == '__main__':
    sys.exit(main())