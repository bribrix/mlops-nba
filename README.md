# NBA Data Analysis and Prediction by Briac Marchandise

This Python script is designed to process, analyze, and predict data related to the National Basketball Association (NBA) using machine learning. It encapsulates a typical machine learning project workflow, including data preparation, model training, prediction, and saving the results.

## Global Operation

### Data Preparation

- **Reads data from CSV files** located in a specified directory, with automatic delimiter detection.
- **Cleans and prepares data** by adding NBA-specific features and defining rising stars based on certain business logic.

### Curated Data Storage

- **Saves curated data in CSV format** for later use, facilitating data access and manipulation.

### Model Training

- **Utilizes a pipeline** that includes pre-processing (standardization of numerical variables and one-hot encoding of categorical variables) and a regression model (RandomForestRegressor) to predict player points scored (PTS).
- **Divides the data into training and test sets**, trains the model, and evaluates its performance using the root mean square error (RMSE).
- **Saves the trained model and model parameters** for future use.

### Prediction and Results Storage

- **Makes predictions on the test set** and stores actual and predicted results in a CSV file.

## Requirements

To run this script, you will need:

- Python 3.8+
- pandas
- scikit-learn
- joblib

Install the necessary packages using pip:

```bash
pip install pandas scikit-learn joblib
