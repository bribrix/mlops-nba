import unittest
import pandas as pd
from functions import train_model
from sklearn.model_selection import train_test_split

class TestTrainModel(unittest.TestCase):
    def setUp(self):
        # Load a sample of the dataset
        # Replace '../dataset/nba_player_stats_sample.csv' with the path to your actual sample dataset
        sample_data_path = '../dataset/nba_player_stats_sample.csv'
        self.df = pd.read_csv(sample_data_path)

        # Ensure that 'PTS' is the target variable and is not used as a feature
        self.features = self.df.drop(columns=['PTS']).select_dtypes(include=['float64', 'int64']).columns.tolist()
        self.target = 'PTS'

    def test_train_model(self):
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.df[self.features], self.df[self.target], test_size=0.2, random_state=42)

        # Train the model using the training data
        model, X_test, y_test, rmse = train_model(X_train, y_train, X_test, y_test)
        
        # Ensure a model object is returned
        self.assertIsNotNone(model)
        
        # Check that the RMSE is a float value
        self.assertIsInstance(rmse, float)
        
        # Assert that test datasets are not empty
        self.assertGreater(len(X_test), 0)
        self.assertGreater(len(y_test), 0)

if __name__ == '__main__':
    unittest.main()
