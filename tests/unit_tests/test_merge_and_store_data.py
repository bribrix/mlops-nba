import unittest
import pandas as pd
from functions import merge_and_store_data, fetch_nba_player_stats, filter_players_to_tot
from pathlib import Path
import tempfile
import shutil

class TestMergeAndStoreData(unittest.TestCase):
    def setUp(self):
        # Create temporary directory to store test data files
        self.test_dir = tempfile.mkdtemp()

        # Generate sample data similar to your notebook's data
        self.df1 = fetch_nba_player_stats('2023-24')
        self.df1['source'] = 'df1'
        self.df2 = filter_players_to_tot(self.df1.copy())
        self.df2['source'] = 'df2'

    def test_merge_and_store_data(self):
        # Use the function to merge the data
        output_file_path = merge_and_store_data([self.df1, self.df2], output_dir=self.test_dir)
        
        # Check if the file was created
        self.assertTrue(Path(output_file_path).is_file())
        
        # Check the contents of the file
        merged_df = pd.read_csv(output_file_path)
        self.assertEqual(len(merged_df), len(self.df1) + len(self.df2))  # Assuming a vertical merge (stacking)
        self.assertIn('source', merged_df.columns)  # Check if the source column is in the merged file
        
        # Clean up the created file and directory
        shutil.rmtree(self.test_dir)

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()
