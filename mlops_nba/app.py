import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
from math import pi

# Set the base directory for the data
BASE_DIR = 'dataset/'

@st.cache_data
def load_data(file_name):
    data = pd.DataFrame()
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    return data

# Define the function to create the correlation heatmap
def plot_correlation_heatmap(df):
    # Select only numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_df = df[numeric_columns]

    # Compute correlation matrix
    correlation_matrix = numeric_df.corr()

    # Plot heatmap
    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, annot=False, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={'shrink': .5})
    st.pyplot(plt.gcf())
    plt.clf()

# Function to plot top Teams by points
def plot_top_teams(df, column='PTS', title='Top 10 Teams by Points'):
    top_teams = df.sort_values(column, ascending=False).head(20)
    plt.figure(figsize=(14, 10))
    sns.barplot(x=column, y='TEAM_ABBREVIATION', data=top_teams, palette='coolwarm')
    plt.title(title)
    plt.xlabel('Points per Season')
    plt.ylabel('TEAM_ABBREVIATION')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

# Function to plot top Teams by assists per game
def plot_top_teams_by_assists(df, title='Top 20 Teams by Assists per Game'):
    top_teams_by_assists = df.sort_values('AST', ascending=False).head(20)
    plt.figure(figsize=(14, 10))
    sns.barplot(x='AST', y='TEAM_ABBREVIATION', data=top_teams_by_assists, palette='coolwarm')
    plt.title(title)
    plt.xlabel('Assists per Game')
    plt.ylabel('Team Abbreviation')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

# Function to plot scatter plot for REB vs PTS
def plot_reb_vs_pts(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='REB', y='PTS', data=df)
    plt.title('Rebounds vs Points')
    plt.xlabel('Rebounds')
    plt.ylabel('Points')
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.clf()


# Main function to run the app
def main():
    st.title('NBA Player Stats Dashboard')

    # Load the player stats data
    df = 'nba_games_stats_2024-02-08.csv'
    player_stats = load_data(df)

    if player_stats.empty:
        st.error(f'File not found: {df}')
        return
    
    
    

    # Show the loaded data
    st.write("Loaded data:", player_stats)

    # Show the correlation heatmap
    plot_correlation_heatmap(player_stats)

    # Show the barplot of the top players by points
    plot_top_teams(player_stats)

    # Show the barplot of the top players by assists per game
    plot_top_teams_by_assists(player_stats)

    # Plot scatter plot for REB vs PTS
    plot_reb_vs_pts(player_stats)

    # Sample DataFrame 'team_stats_2023_24' assumed to be sorted by 'PTS'
    # Select the top 5 teams by points scored
    top_teams = player_stats.sort_values('PTS', ascending=False).head(5)

    # Define the number of variables
    categories = ['REB', 'BLK', 'PTS', 'STL', 'FG3A']
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
    for i, (_, row) in enumerate(top_teams.iterrows()):
        data = row[categories].tolist()
        data += data[:1]  # Repeat the first value to close the circle
        ax.plot(angles, data, linewidth=1, linestyle='solid', label=row['TEAM_ABBREVIATION'])
        ax.fill(angles, data, alpha=0.25)

    # Add a legend and title
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Top 5 NBA Teams by Points - Radar Chart')

    # Show plot
    st.pyplot(fig)
    plt.clf()

if __name__ == '__main__':
    main()
