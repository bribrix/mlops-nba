import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import os

# Define the base directory for the data
BASE_DIR = 'dataset/'

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
    top_teams = df.groupby('TEAM_ABBREVIATION')[column].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(14, 10))
    top_teams.plot(kind='barh', color='skyblue')
    plt.title(title)
    plt.xlabel('Total Points')
    plt.ylabel('Team')
    st.pyplot(plt.gcf())
    plt.clf()
    
def plot_top_teams_by_ast(df, column='AST', title='Top 10 Teams by Assists'):
    top_teams = df.groupby('TEAM_ABBREVIATION')[column].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(14, 10))
    top_teams.plot(kind='barh', color='skyblue')
    plt.title(title)
    plt.xlabel('Total Assists')
    plt.ylabel('Team')
    st.pyplot(plt.gcf())
    plt.clf()

def plot_radar_chart(df):
    # Select the top teams by points scored
    top_teams = df.groupby('TEAM_ABBREVIATION')['PTS'].sum().sort_values(ascending=False).head(5).index
    top_teams_stats = df[df['TEAM_ABBREVIATION'].isin(top_teams)].groupby('TEAM_ABBREVIATION')[['PTS', 'AST', 'REB', 'STL', 'BLK']].mean()
    
    # Define the number of variables
    categories = list(top_teams_stats)
    N = len(categories)
    
    # Create a list of angles for the radar chart, one for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Initialize the radar plot
    fig, ax = plt.subplots(subplot_kw={'polar': True}, figsize=(10, 10))
    
    # Draw one axe per variable and add labels
    plt.xticks(angles[:-1], categories)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    
    # Plot data and fill with color for each team
    for team, row in top_teams_stats.iterrows():
        data = row.tolist()
        data += data[:1]  # Repeat the first value to close the circle
        ax.plot(angles, data, linewidth=1, linestyle='solid', label=team)
        ax.fill(angles, data, alpha=0.25)
    
    # Add a legend and title
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Top 5 NBA Teams by Points - Radar Chart')
    
    # Show plot
    st.pyplot(plt.gcf())
    plt.clf()

# Main function to run the app
def main():
    st.image("frontend/static/Website banner 5.jpg")
    st.title('NBA Predictions')
    
    # Load data
    df = load_data('nba_games_stats_2024-02-08.csv')
    
    if not df.empty:
        st.write("Loaded data:")
        st.dataframe(df.head())
        
        # Display plots
        plot_correlation_heatmap(df)
        plot_top_teams(df)
        plot_top_teams_by_ast(df)
        plot_radar_chart(df)
       

if __name__ == '__main__':
    main()