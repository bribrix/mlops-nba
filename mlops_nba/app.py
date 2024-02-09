import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
from math import pi

# Define the base directory for the data
BASE_DIR = 'dataset/'

@st.experimental_memo
def load_data(file_name):
    data = pd.DataFrame()
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    return data


def plot_correlation_heatmap(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_df = df[numeric_columns]
    correlation_matrix = numeric_df.corr()
    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, annot=False, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={'shrink': .5})
    st.pyplot(plt.gcf())
    plt.clf()

def plot_top_teams(df, column='PTS', title='Top 10 Teams by Points'):
    top_teams = df.sort_values(column, ascending=False).head(20)
    plt.figure(figsize=(14, 10))
    sns.barplot(x=column, y='TEAM_ABBREVIATION', data=top_teams, palette='coolwarm')
    plt.title(title)
    plt.xlabel('Points per Season')
    plt.ylabel('TEAM_ABBREVIATION')
    st.pyplot(plt.gcf())
    plt.clf()

def plot_top_teams_by_assists(df, title='Top 20 Teams by Assists per Game'):
    top_teams_by_assists = df.sort_values('AST', ascending=False).head(20)
    plt.figure(figsize=(14, 10))
    sns.barplot(x='AST', y='TEAM_ABBREVIATION', data=top_teams_by_assists, palette='coolwarm')
    plt.title(title)
    plt.xlabel('Assists per Game')
    plt.ylabel('Team Abbreviation')
    st.pyplot(plt.gcf())
    plt.clf()

def plot_reb_vs_pts(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='REB', y='PTS', data=df)
    plt.title('Rebounds vs Points')
    plt.xlabel('Rebounds')
    plt.ylabel('Points')
    st.pyplot(plt.gcf())
    plt.clf()

# Main function to run the app
def main():
    st.image("frontend\static\Website banner 5.jpg")
    st.title('NBA Predictions')
    st.header('Predict the number of points of a player using ML')

    # Date selection
    date = st.date_input("Select a date:")
    # Assuming you have a function to get matches for a specific date
    matches = get_matches_for_date(date)
    
    match = st.selectbox("Choose a match:", ["Choose the day match..."] + matches)
    
    if match != "Choose the day match...":
        # Display match data or predictions
        st.write("You selected:", match)
        # You would include logic here to display stats or predictions for the selected match

    # Display data
    df = load_data('nba_games_stats_2024-02-08.csv')
    if not df.empty:
        st.write("Loaded data:")
        st.dataframe(df.head())
        plot_correlation_heatmap(df)
        plot_top_teams(df)
        plot_top_teams_by_assists(df)
        plot_reb_vs_pts(df)

def get_matches_for_date(date):
    # Placeholder function to simulate fetching matches
    # You would replace this with actual logic to load matches
    if date:
        return [f"Match {i}" for i in range(1, 6)]
    return []

if __name__ == '__main__':
    main()
