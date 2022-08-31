#--- How to Run ---
#--- Typy this in command line ---
#cd Desktop\PythonCode_Movie_recommend
#Then Type Streamlit run movies-recommender-system.py
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests

# Creating Function to fetch Posters

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=255610c0608d97dd4278c44c9179cfed&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Creating Function Recommend

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_df[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
        
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch Poster From API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Importing new_df DataFrame from jupyter notebook
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Importing Similarity_df DataFrame from jupyter notebook
similarity_df = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# Creating Select Box for searching movies
movie_list = movies['title'].values
selected_movie= st.selectbox(
    'Type or select a movie from the dropdown',
    movie_list
)

# Creating Recommend Button and calling Recommend Function

if st.button('Show Recommendation'):
    recommended_movies_names,recommended_movies_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4])

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#https://api.themoviedb.org/3/movie/{movie_id}?api_key=255610c0608d97dd4278c44c9179cfed&language=en-US