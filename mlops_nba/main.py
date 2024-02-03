from pathlib import Path
import logging
import time
import sys
from config import RAW_DATA_DIR, CURATED_DATA_DIR, OUTPUT_DIR
from functions import merge_and_store_data, train_model, process_file
from common.io import create_folder


# Create a logs folder if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
 
# Configure logging with a timestamp in the file name
current_time = time.strftime("%Y%m%d-%H%M%S")
log_filename = f'nba_data_processing_{current_time}.log'
logging.basicConfig(filename=LOGS_DIR / log_filename, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
 
   
if __name__ == "__main__":

    print("Starting NBA data preprocessing...")
 
    if not create_folder(RAW_DATA_DIR):
        print(f"Raw data directory {RAW_DATA_DIR} exists.")
    else:
        print(f"Raw data directory {RAW_DATA_DIR} created.")
 
    if not create_folder(CURATED_DATA_DIR):
        print(f"Curated data directory {CURATED_DATA_DIR} exists.")
    else:
        print(f"Curated data directory {CURATED_DATA_DIR} created.")
 
    raw_data_files = list(RAW_DATA_DIR.glob("*.csv"))
    if not raw_data_files:
        print(f"No CSV files found in {RAW_DATA_DIR}. Please check your data source.")
        sys.exit(1)
 
    all_processed_data = []
    for file_path in sorted(RAW_DATA_DIR.glob('*.csv'), key=lambda x: x.stat().st_mtime):
        print(f"Processing file: {file_path.name}")
        processed_data = process_file(file_path)
        if processed_data is not None:
            all_processed_data.append(processed_data)
        else:
            print(f"Warning: No data returned for {file_path.name}")
 
    if all_processed_data:
        merged_data = merge_and_store_data(all_processed_data)
        logging.info("Starting model training...")
        model, X_test, y_test ,rmse_pts= train_model(merged_data)
        logging.info(f"Model training completed with RMSE: {rmse_pts}")
 
        logging.info("Starting prediction...")
        # predict_and_store_output(model, X_test, y_test)
        logging.info("Prediction completed.")
    else:
        logging.info("No data to train model.")
 
    print("NBA data preprocessing, model training, and prediction completed.")

