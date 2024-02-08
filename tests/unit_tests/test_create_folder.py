import unittest
from pathlib import Path
from common.io import create_folder

class TestCreateFolder(unittest.TestCase):
    def test_create_folder(self):
        # Temporary directory for testing
        temp_dir = Path('test_dir')
        
        # Ensure the directory does not exist
        if temp_dir.exists():
            temp_dir.rmdir()
        
        # Test if the function creates the directory
        create_folder(temp_dir)
        self.assertTrue(temp_dir.exists())
        
        # Clean up
        if temp_dir.exists():
            temp_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
