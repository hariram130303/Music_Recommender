import streamlit as st
import pickle
import pandas as pd
import webbrowser

# Load models
music = pickle.load(open('music.pkl', 'rb'))
musicdf = pd.DataFrame(music)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "All Tracks"])

if page == "About":
    st.title("About System")
    st.write("Here, the system uses your likes in order to recommend you with things that you might like. It uses the information provided by you over the dropdown and the ones it is able to gather and then it curate recommendations according to that")
    st.header("Working :")
    st.write("1. Type or Select a Music from Dropdown ")
    st.write("2. Click (Get Recommendations) Button")
    st.write("3. It will Recommend you Top 10 Music Tracks ")
    st.write("4. Click on URL of any Music Tracks ")
    st.write("5. It will direct you to the Spotify")
    st.write("6. You can also have a look on (All Tracks) in the sidebar")
    st.write("7. If you want to know about how the system works then click a button called (All Tracks) on the sidebar ")


elif page == "All Tracks":
    st.title("🎶 All Available Tracks")
    st.dataframe(musicdf, 3000, 500)

else:
    st.title("🎧 Music Recommender System")
    st.text('P-92 (Group-6)')

    no_recommend = st.sidebar.slider('How many Recommendations?', 5, 20, 5)
    music_list = musicdf['Track_Name'].values
    selected_music_name = st.selectbox("Search or Select a Music Track", music_list)

    def recommend(musics):
        index = musicdf[musicdf['Track_Name'] == musics].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_music_names = []
        for i in distances[:no_recommend]:
            recommended_music_names.append(musicdf.iloc[i[0]].Track_Name)
        return recommended_music_names
    
    # Function to open Spotify URI
    def open_spotify_uri(uri):
        if uri.startswith("spotify:track:"):
            track_id = uri.split(":")[-1]
            webbrowser.open(f"https://open.spotify.com/track/{track_id}")
        else:
            print("Invalid Spotify track URI")


    if st.button('Get Recommendations'):
        recommendations = recommend(selected_music_name)
        for name in recommendations:
            index_no = musicdf[musicdf["Track_Name"] == name].index[0]
            uri = musicdf['Track_URI'][index_no] if 'Track_URI' in musicdf.columns else 'N/A'
            preview = musicdf['Track_Preview'][index_no] if 'Track_Preview' in musicdf.columns else 'No preview available'
            st.markdown(f"**{name}**  \n[🔗 Listen on Spotify]({open_spotify_uri(uri)})  \n🎧 Preview: {preview}")
