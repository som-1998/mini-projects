import requests

TOP_N = 5

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Helper function to get movie index from ID
def get_movie_index(movie_id , movies_df):
    movie = movies_df[movies_df['movie_id'] == movie_id]
    return movie.index.values[0] if not movie.empty else None

def recommended(movie_name=None, movies_df=None, similarity_matrix=None,TOP_N = 2 ):
    movie = movies_df[movies_df['title'].str.lower() == movie_name.lower()]
    # if not movie.empty:
    movie_id = movie['movie_id'].values[0]
    movie_index = movie.index.values[0]
    if movie_index is not None:
        # Get top 10 similar movies
        similar_movies = sorted(list(enumerate(similarity_matrix[movie_index])), reverse=True, key=lambda x: x[1])[1:TOP_N + 1]
        recommendations = []
        for i in similar_movies:
            movie = movies_df.loc[i[0]]
            
            recommendations.append({
                'title': movie['title'],
                # 'poster': fetch_poster(movie['movie_id'])
                'poster': movie['movie_id']
            })
        print(recommendations)
        return recommendations
    else:
        return None