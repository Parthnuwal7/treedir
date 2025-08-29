"""
Tests for TreeDir core functionality.
"""

import unittest
import tempfile
import os
import shutil
from treedir.core import TreeDir
from treedir.parser import TreeParser


class TestTreeDir(unittest.TestCase):
    """Test TreeDir core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_structure = {
            'src': {
                'main.py': None,
                'config.py': None,
                'utils': {
                    'helpers.py': None
                }
            },
            'tests': {
                'test_main.py': None
            },
            'README.md': None
        }
        self.treedir = TreeDir()
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_structure_additive(self):
        """Test creating structure in additive mode"""
        result = self.treedir._create_structure(
            self.test_structure, 
            self.temp_dir, 
            mode='additive'
        )
        
        self.assertTrue(result)
        
        # Check if files and directories are created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src', 'main.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src', 'utils')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src', 'utils', 'helpers.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'tests', 'test_main.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'README.md')))
    
    def test_create_structure_strict(self):
        """Test creating structure in strict mode"""
        # First create some extra files
        extra_file = os.path.join(self.temp_dir, 'extra.txt')
        with open(extra_file, 'w') as f:
            f.write('extra content')
        
        result = self.treedir._create_structure(
            self.test_structure, 
            self.temp_dir, 
            mode='strict'
        )
        
        self.assertTrue(result)
        
        # Check that extra file is removed
        self.assertFalse(os.path.exists(extra_file))
        
        # Check that required files exist
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src', 'main.py')))
    
    def test_get_structure_dict(self):
        """Test getting structure dictionary from directory"""
        # Create test structure
        self.treedir._create_structure(self.test_structure, self.temp_dir)
        
        # Get structure dict
        result_structure = self.treedir.get_structure_dict(self.temp_dir)
        
        # Verify structure
        self.assertIn('src', result_structure)
        self.assertIn('tests', result_structure)
        self.assertIn('README.md', result_structure)
        self.assertIsNone(result_structure['README.md'])  # Files should be None
        
        # Check nested structure
        self.assertIn('main.py', result_structure['src'])
        self.assertIn('utils', result_structure['src'])
        self.assertIn('helpers.py', result_structure['src']['utils'])
    
    def test_find_file(self):
        """Test finding files"""
        # Create test structure
        self.treedir._create_structure(self.test_structure, self.temp_dir)
        
        # Find existing file
        found_path = self.treedir.find('main.py', self.temp_dir)
        expected_path = os.path.join(self.temp_dir, 'src', 'main.py')
        
        self.assertEqual(os.path.abspath(found_path), os.path.abspath(expected_path))
        
        # Find non-existing file
        not_found = self.treedir.find('nonexistent.py', self.temp_dir)
        self.assertIsNone(not_found)
    
    def test_findr_relative_path(self):
        """Test finding files with relative path"""
        # Create test structure
        self.treedir._create_structure(self.test_structure, self.temp_dir)
        
        # Find with relative path
        rel_path = self.treedir.findr('helpers.py', self.temp_dir)
        expected_rel_path = os.path.join('src', 'utils', 'helpers.py')
        
        self.assertEqual(os.path.normpath(rel_path), os.path.normpath(expected_rel_path))
    
    def test_reset_directory(self):
        """Test resetting directory"""
        # Create test structure
        self.treedir._create_structure(self.test_structure, self.temp_dir)
        
        # Verify files exist
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src')))
        
        # Reset directory
        result = self.treedir.reset(self.temp_dir)
        self.assertTrue(result)
        
        # Verify directory is empty
        self.assertEqual(len(os.listdir(self.temp_dir)), 0)


class TestTreeParser(unittest.TestCase):
    """Test TreeParser functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = TreeParser()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_detect_tree_format(self):
        """Test detecting tree format"""
        tree_content = """
        project/
        ├── src/
        │   └── main.py
        └── README.md
        """
        
        format_type = self.parser._detect_format(tree_content)
        self.assertEqual(format_type, 'tree')
    
    def test_detect_dict_format(self):
        """Test detecting dictionary format"""
        dict_content = '{"src": {"main.py": null}, "README.md": null}'
        
        format_type = self.parser._detect_format(dict_content)
        self.assertEqual(format_type, 'dict')
    
    def test_detect_path_format(self):
        """Test detecting path format"""
        path_content = """
        src/main.py
        src/config.py
        README.md
        """
        
        format_type = self.parser._detect_format(path_content)
        self.assertEqual(format_type, 'path')
    
    def test_parse_dict_format(self):
        """Test parsing dictionary format"""
        dict_content = '{"src": {"main.py": null}, "README.md": null}'
        
        result = self.parser._parse_dict_format(dict_content)
        
        self.assertIn('src', result)
        self.assertIn('README.md', result)
        self.assertIn('main.py', result['src'])
        self.assertIsNone(result['README.md'])
    
    def test_parse_path_format(self):
        """Test parsing path format"""
        path_content = """src/main.py
src/config.py
tests/test_main.py
README.md"""
        
        result = self.parser._parse_path_format(path_content)
        
        self.assertIn('src', result)
        self.assertIn('tests', result)
        self.assertIn('README.md', result)
        self.assertIn('main.py', result['src'])
        self.assertIn('config.py', result['src'])
        self.assertIn('test_main.py', result['tests'])
    
    def test_structure_to_paths(self):
        """Test converting structure to paths"""
        structure = {
            'src': {
                'main.py': None,
                'utils': {
                    'helpers.py': None
                }
            },
            'README.md': None
        }
        
        paths = self.parser.structure_to_paths(structure)
        
        expected_paths = [
            'src/',
            'src/main.py',
            'src/utils/',
            'src/utils/helpers.py',
            'README.md'
        ]
        
        for expected_path in expected_paths:
            self.assertIn(expected_path, paths)
    
    def test_validate_structure(self):
        """Test structure validation"""
        valid_structure = {
            'src': {
                'main.py': None
            },
            'README.md': None
        }
        
        invalid_structure = {
            'src': 'invalid_value',  # Should be dict or None
            123: None  # Keys should be strings
        }
        
        self.assertTrue(self.parser.validate_structure(valid_structure))
        self.assertFalse(self.parser.validate_structure(invalid_structure))
    
    def test_parse_file_not_found(self):
        """Test parsing non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file('nonexistent.txt')


if __name__ == '__main__':
    unittest.main()