import streamlit as st
import pickle
import pandas as pd

# Load data
music = pickle.load(open('music.pkl', 'rb'))
musicdf = pd.DataFrame(music)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Helper function to convert Spotify URI to a web URL
def uri_to_url(uri):
    if isinstance(uri, str) and uri.startswith("spotify:track:"):
        track_id = uri.split(":")[-1]
        return f"https://open.spotify.com/track/{track_id}"
    return "#"

# Sidebar navigation
st.sidebar.title("🎵 Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "All Tracks"])

# About Page
if page == "About":
    st.title("ℹ️ About This Recommender System")
    st.write("""
    This system recommends music tracks based on your selected favorite.  
    It uses content-based filtering via cosine similarity between track features.
    """)
    
    st.subheader("📌 How It Works:")
    st.markdown("""
    1. **Select a track** from the dropdown list.  
    2. **Click "Get Recommendations"** to generate suggestions.  
    3. Each recommendation shows a **Spotify link** and an optional **audio preview**.  
    4. Explore all available tracks using the **"All Tracks"** tab.  
    """)

# All Tracks Page
elif page == "All Tracks":
    st.title("🎶 All Available Tracks")
    st.dataframe(musicdf[['Track_Name', 'Artist_Name', 'Track_URI']], height=600)

# Home Page (Recommendation System)
else:
    st.title("🎧 Music Recommender System")
    st.markdown("_P-92 (Group-6)_")

    # Sidebar controls
    no_recommend = st.sidebar.slider('Number of Recommendations', 5, 20, 5)
    music_list = musicdf['Track_Name'].values
    selected_music_name = st.selectbox("🎼 Select a Music Track", music_list)

    # Recommendation function
    def recommend(track_name):
        index = musicdf[musicdf['Track_Name'] == track_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended = []
        for i in distances[1:no_recommend + 1]:  # skip the first (same song)
            recommended.append(musicdf.iloc[i[0]])
        return recommended

    # Recommendation Output
    if st.button('🚀 Get Recommendations'):
        recommendations = recommend(selected_music_name)
        for track in recommendations:
            name = track['Track_Name']
            uri = track.get('Track_URI', 'N/A')
            preview = track.get('Track_Preview', 'No preview available')
            url = uri_to_url(uri)

            st.markdown(f"""
            **🎵 {name}**  
            🔗 [Listen on Spotify]({url})  
            🎧 Preview: {preview if preview != 'No preview available' else '*Not available*'}
            """)
