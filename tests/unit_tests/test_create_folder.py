import unittest
from pathlib import Path
from mlops_nba.common.io import create_folder
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))  # Ajoute le répertoire racine du projet



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
