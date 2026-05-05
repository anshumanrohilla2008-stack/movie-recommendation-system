import streamlit as st
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches


# LOAD DATA

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Merge for collaborative
data = pd.merge(ratings, movies, on="movieId")


# CONTENT-BASED SETUP

movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))

mlb = MultiLabelBinarizer()
genre_matrix = mlb.fit_transform(movies["genres"])
genre_df = pd.DataFrame(genre_matrix, columns=mlb.classes_)

cosine_sim = cosine_similarity(genre_df)

indices = pd.Series(movies.index, index=movies["title"])


def recommend(title):
    if title not in indices:
        return None

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]

    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]

    result = pd.DataFrame({
        "title": movies["title"].iloc[movie_indices].values,
        "similarity_score": scores
    })

    return result



# COLLABORATIVE SETUP

user_movie_matrix = data.pivot_table(
    index="userId",
    columns="title",
    values="rating"
)

user_movie_matrix_filled = user_movie_matrix.fillna(0)

user_similarity = cosine_similarity(user_movie_matrix_filled)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)


def get_similar_users(user_similarity_df, target_user, top_k=5):
    similar_users = user_similarity_df[target_user].sort_values(ascending=False)
    return similar_users[1:top_k+1]


def get_candidate_movies(user_movie_matrix, similar_users, target_user):
    user_movies = user_movie_matrix.loc[target_user]
    watched_movies = user_movies[user_movies > 0].index

    candidate_movies = set()

    for user in similar_users.index:
        movies_ = user_movie_matrix.loc[user]
        movies_ = movies_[movies_ > 0].index
        candidate_movies.update(movies_)

    candidate_movies = candidate_movies - set(watched_movies)
    return candidate_movies


def score_movies(candidate_movies, similar_users, user_movie_matrix):
    movie_scores = {}

    for movie in candidate_movies:
        ratings_with_similarity = []

        for user in similar_users.index:
            rating = user_movie_matrix.loc[user, movie]
            similarity = similar_users[user]

            if rating > 0:
                ratings_with_similarity.append((rating, similarity))

        if ratings_with_similarity:
            sum_rating_times_sim = 0
            sum_sim = 0

            for rating, similarity in ratings_with_similarity:
                sum_rating_times_sim += rating * similarity
                sum_sim += similarity

            movie_scores[movie] = sum_rating_times_sim / sum_sim

    return movie_scores


def rank_movies(movie_scores, top_n=5):
    ranked_pairs = sorted(
        movie_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = [pair[0] for pair in ranked_pairs[:top_n]]
    return recommendations


def recommend_movies(user_similarity_df, user_movie_matrix, target_user, top_k=5, top_n=5):
    similar_users = get_similar_users(user_similarity_df, target_user, top_k)
    candidate_movies = get_candidate_movies(user_movie_matrix, similar_users, target_user)
    movie_scores = score_movies(candidate_movies, similar_users, user_movie_matrix)
    recommendations = rank_movies(movie_scores, top_n)
    return recommendations



# STREAMLIT UI

st.title("🎬 Movie Recommendation System")

# Content-based 
st.header("📌 Movie-based Recommendation (Content-Based)")

movie_input = st.text_input("Enter a movie name")

titles = movies["title"].tolist()
titles_lower = [t.lower() for t in titles]

selected_movie = None

if movie_input:
    matches = get_close_matches(
        movie_input.lower(),
        titles_lower,
        n=5,
        cutoff=0.2
    )

    if matches:
        matches = [titles[titles_lower.index(m)] for m in matches]
        selected_movie = st.selectbox("Did you mean:", matches)
    else:
        st.error("No close matches found.")


if st.button("Recommend Movies"):
    if not selected_movie:
        st.warning("Please enter and select a valid movie.")
    else:
        recommendations = recommend(selected_movie)

        if recommendations is not None:
            st.subheader("🎯 Recommended Movies:")
            st.dataframe(recommendations)
        else:
            st.error("Movie not found.")

# Collaborative 
st.header("👥 User-based Recommendation (Collaborative Demo)")

user_input = st.text_input("Enter User ID")

if st.button("Recommend for User"):
    if not user_input:
        st.warning("Please enter a User ID.")
    else:
        try:
            user_id = int(user_input)

            if user_id not in user_movie_matrix.index:
                st.error("User ID not found.")
            else:
                recommendations = recommend_movies(
                    user_similarity_df,
                    user_movie_matrix,
                    user_id
                )

                st.subheader("🎯 Recommended Movies:")
                for i, movie in enumerate(recommendations, 1):
                    st.write(f"{i}. {movie}")

        except:
            st.error("Please enter a valid number.")