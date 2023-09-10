# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
playlist_df = pd.read_csv('playlist_2010to2022.csv')

# === GENRE TRENDS ANALYSIS ===
# Filter the dataset for the years 2010 to 2022
filtered_df = playlist_df[playlist_df['year'].between(2010, 2022)]

# Count occurrences of each genre for each year
genre_counts = {}
for _, row in filtered_df.iterrows():
    year = row['year']
    genres = eval(row['artist_genres'])
    for genre in genres:
        if year not in genre_counts:
            genre_counts[year] = {}
        if genre not in genre_counts[year]:
            genre_counts[year][genre] = 0
        genre_counts[year][genre] += 1

# Convert genre counts to DataFrame and get percentage distribution of tracks for each genre per year
genre_counts_df = pd.DataFrame(genre_counts).fillna(0).transpose()
genre_percentage_distribution = genre_counts_df.divide(genre_counts_df.sum(axis=1), axis=0) * 100

# Identify the top 5 genres over the period for detailed analysis
top_5_genres = set()
for _, genres in genre_counts.items():
    top_genres = sorted(genres, key=genres.get, reverse=True)[:5]
    top_5_genres.update(top_genres)

# Plot the yearly genre distribution for the top 5 genres
plt.figure(figsize=(16, 8))
for genre in top_5_genres:
    plt.plot(genre_percentage_distribution.index, genre_percentage_distribution[genre], label=genre, marker='o')
plt.title('Yearly Genre Distribution (2010-2022)')
plt.xlabel('Year')
plt.ylabel('Percentage of Tracks (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === AUDIO FEATURES ANALYSIS ===
# Extract average values of audio features for each of the top 5 genres over the years
audio_features = [
    'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo'
]
genre_audio_features = {}
for genre in top_5_genres:
    genre_rows = filtered_df[filtered_df['artist_genres'].str.contains(genre)]
    for feature in audio_features:
        if genre not in genre_audio_features:
            genre_audio_features[genre] = {}
        genre_audio_features[genre][feature] = genre_rows.groupby('year')[feature].mean()

# Plot energy and valence for the top 5 genres
energy_data = pd.DataFrame({genre: genre_audio_features[genre]['energy'] for genre in top_5_genres})
valence_data = pd.DataFrame({genre: genre_audio_features[genre]['valence'] for genre in top_5_genres})
fig, ax = plt.subplots(2, 1, figsize=(16, 12))
for genre in top_5_genres:
    ax[0].plot(energy_data.index, energy_data[genre], label=genre, marker='o')
    ax[1].plot(valence_data.index, valence_data[genre], label=genre, marker='o')
ax[0].set_title('Energy Trend for Top 5 Genres (2010-2022)')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Energy')
ax[1].set_title('Valence Trend for Top 5 Genres (2010-2022)')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('Valence')
for axis in ax:
    axis.legend()
    axis.grid(True)
plt.tight_layout()
plt.show()

# === POPULARITY ANALYSIS ===
# Extract average artist and track popularity for each of the top 5 genres over the years
artist_popularity_data = {}
track_popularity_data = {}
for genre in top_5_genres:
    genre_rows = filtered_df[filtered_df['artist_genres'].str.contains(genre)]
    artist_popularity_data[genre] = genre_rows.groupby('year')['artist_popularity'].mean()
    track_popularity_data[genre] = genre_rows.groupby('year')['track_popularity'].mean()

# Plot artist and track popularity for the top 5 genres
fig, ax = plt.subplots(2, 1, figsize=(16, 12))
for genre in top_5_genres:
    ax[0].plot(artist_popularity_data[genre].index, artist_popularity_data[genre], label=genre, marker='o')
    ax[1].plot(track_popularity_data[genre].index, track_popularity_data[genre], label=genre, marker='o')
ax[0].set_title('Artist Popularity Trend for Top 5 Genres (2010-2022)')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Artist Popularity')
ax[1].set_title('Track Popularity Trend for Top 5 Genres (2010-2022)')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('Track Popularity')
for axis in ax:
    axis.legend()
    axis.grid(True)
plt.tight_layout()
plt.show()
