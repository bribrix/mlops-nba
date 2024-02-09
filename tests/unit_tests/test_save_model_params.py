import unittest
import os
from mlops_nba.models.young_potential_stars import my_function
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path

class TestSaveModelParams(unittest.TestCase):
    def test_save_model_params_creates_file(self):
        # Create a RandomForestRegressor and set some parameters
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        
        # Define a filename for the test
        filename = 'test_model_params.txt'
        
        # Run the save_model_params function
        save_model_params(model, filename)
        
        # Check that the file was created
        self.assertTrue(Path(filename).is_file())
        
        # Read the file and check if the content is correct
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.assertIn("n_estimators: 10\n", lines)
            self.assertIn("random_state: 42\n", lines)
        
        # Clean up the file after test
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
