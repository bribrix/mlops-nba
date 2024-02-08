import pandas as pd
from pathlib import Path
from config import RAW_DATA_DIR, CURATED_DATA_DIR,OUTPUT_DIR
from common.io import create_folder
from common.dates import get_now
from potential_stars.extract import create_nba_features, stars_definition
import re
import logging
import time
import joblib
import datetime
import csv
import os


from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamestimatedmetrics



def save_model_params(model, filename):
    with open(filename, 'w') as file:
        for param, value in model.get_params().items():
            file.write(f"{param}: {value}\n")


 
def read_kaggle_data(file_path, encoding='utf-8'):
    """Read the Kaggle dataset with automatic delimiter detection."""
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            first_line = file.readline()
        delimiter = ';' if ';' in first_line else ','
        return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='latin1', delimiter=delimiter)
 



def store_curated_data(players, file_name):
    """Store the processed data in the curated directory."""
    create_folder(CURATED_DATA_DIR)
    current_date = get_now(for_files=True)
    output_file = CURATED_DATA_DIR / f"{file_name}-curated-{current_date}.csv"
    players.to_csv(output_file, index=False)
 



def process_file(file_path):
    """Process a single file and return processed data."""
    start_time = time.time()
    logging.info(f"Processing {file_path.name}...")
    kaggle_data = read_kaggle_data(file_path)
 
    year_match = re.search(r'\d{4}-\d{4}', file_path.name)
    year = year_match.group() if year_match else 'Unknown'
    kaggle_data['Year'] = year
 
    processed_data = create_nba_features(kaggle_data)
    processed_data["rising_stars"] = processed_data.apply(stars_definition, axis=1)
 
    processing_time = time.time() - start_time
    logging.info(f"Data processed for {file_path.name}, DataFrame shape: {processed_data.shape} in {processing_time:.2f} seconds")
    return processed_data
 



def merge_and_store_data(all_data):
    """Merge and store all processed data in a single CSV file and return the merged DataFrame."""
    merged_data = pd.concat(all_data, ignore_index=True)
    merged_data.sort_values(by=['Year'], inplace=True)
    create_folder(CURATED_DATA_DIR)
    current_date = get_now(for_files=True)
    output_file = CURATED_DATA_DIR / f"curated_player-{current_date}.csv"
    merged_data.to_csv(output_file, index=False)
    logging.info(f"Merged data stored in {output_file}")
 
    return merged_data  # Returning the merged DataFrame
 

 
def train_model(data):
    """Train the model on the given data."""
    # Define preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['Pos', 'Tm'])
        ])
 
    # Define model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor())
    ])
 
    # Split data into training and test sets for PTS
    X = data.drop(['Player', 'PTS', 'FG%'], axis=1)
    y_pts = data['PTS']
    X_train_pts, X_test_pts, y_train_pts, y_test_pts = train_test_split(X, y_pts, test_size=0.2, random_state=42)
 
    # Train model to predict PTS
    model.fit(X_train_pts, y_train_pts)
    pts_preds = model.predict(X_test_pts)
 
    rmse_pts = mean_squared_error(y_test_pts, pts_preds, squared=False)
    logging.info(f'RMSE for PTS prediction: {rmse_pts}')
 
    # Generate a timestamp
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
 
    # Ensure the model output directory exists
    model_output_dir = Path("models/train")
    model_output_dir.mkdir(parents=True, exist_ok=True)
 
    # Save the model with the timestamp in the filename
    model_filename = f'pts_prediction_model_{current_time}.joblib'
    joblib.dump(model, model_output_dir / model_filename)
    logging.info(f"Model saved as {model_filename}")
 
    # Save model's parameters to a simple format file
    params_filename = f'model_params_{current_time}.txt'
    save_model_params(model, model_output_dir / params_filename)
    logging.info(f"Model parameters saved as {params_filename}")
 
    return model, X_test_pts, y_test_pts,rmse_pts


 
def predict_and_store_output(model, X_test, y_test):
    predictions = model.predict(X_test)
    output_df = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
   
    # Generate a timestamp
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = OUTPUT_DIR / f"predictions_{current_time}.csv"
    output_df.to_csv(output_file, index=False)
    logging.info(f"Predictions stored in {output_file}")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path_schedule = os.path.join(BASE_DIR, "../dataset/NBASchedule23-24.csv")

def read_first_column_of_csv(file_path_schedule):
    with open(file_path_schedule, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Extraction de la première colonne pour chaque ligne
        column_data = [row[1] for row in reader if row]  # S'assure que la ligne n'est pas vide
    return column_data

def read_schedule(file_path_schedule):
    with open(file_path_schedule, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        schedule = {}
        for row in reader:
            date, match = row[0], row[1]  # Ajustez les indices selon votre fichier CSV
            if date in schedule:
                schedule[date].append(match)
            else:
                schedule[date] = [match]
    return schedule