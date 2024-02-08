import unittest
from pathlib import Path
from functions import merge_and_store_data, process_file
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))


class TestDataIntegration(unittest.TestCase):
    def test_data_processing_integration(self):
        # Path to the CSV file in the raw directory
        test_file_path = Path(__file__).parent.parent / 'dataset/curated/raw/nba_player_global_stats_2024-02-03.csv'
        
        # Ensure the test file exists
        self.assertTrue(test_file_path.exists(), "Test CSV file does not exist.")
        
        # Process the file using your function
        processed_data = process_file(test_file_path)
        self.assertIsNotNone(processed_data, "process_file should return data")
        
        # Assuming merge_and_store_data returns a path to a file, and you're passing a list of DataFrames
        merged_data_file_path = merge_and_store_data([processed_data])
        
        # Verify that the merged data file exists
        self.assertTrue(merged_data_file_path.exists(), "Output file should exist after merging data")
        
        # Clean up any output files created during the test
        if merged_data_file_path.exists():
            merged_data_file_path.unlink()

if __name__ == '__main__':
    unittest.main()
