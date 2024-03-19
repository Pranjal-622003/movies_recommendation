import difflib
import streamlit as st 
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=66862ec077a533abc19c22e85570925e&&language=en-US'.format(movie_id))
    data=response.json()
    return 'https://image.tmdb.org/t/p/original'+data['poster_path']

mv_movie=pd.read_csv('movieList.csv')
similarity=pickle.load(open('similarity.pkl','rb'))

list_of_all_titles= mv_movie['title'].tolist()

recommend_movie_poster=[]
recommend_movie_name=[]

def local_css(st, file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)          

def recommend(movie):    
    find_close_match = difflib.get_close_matches(movie, list_of_all_titles)
    close_match = find_close_match[0]
    index_of_the_movie = mv_movie[mv_movie.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
    
    for movie in sorted_similar_movies[1:6]:
        index = movie[0]
        id=mv_movie[mv_movie.index==index]['id'].values[0]
        title_from_index = mv_movie[mv_movie.index==index]['title'].values[0]
        try:
            poster_url= fetch_poster(id)
        except:
            poster_url= 'https://image.tmdb.org/t/p/original/kyeqWdyUXW608qlYkRqosgbbJyK.jpg'
        
        recommend_movie_name.append(title_from_index)
        recommend_movie_poster.append(poster_url)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select Your Favourite Movie',list_of_all_titles)

if st.button('Recommend'):
    recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)

    for i in range(5):
        with eval(f"col{i+1}"):
            st.write('<div class="movie-container">', unsafe_allow_html=True)
            st.image(recommend_movie_poster[i])
            st.write(f'<p class="movie-name">{recommend_movie_name[i]}</p>', unsafe_allow_html=True)
            st.write('</div>', unsafe_allow_html=True)

local_css(st, "style.css")
