!pip install streamlit

import streamlit as st
import pickle
import pandas as pd

# Load model and matrix
model = pickle.load(
    open("book_recommender.pkl", "rb")
)

user_book_matrix = pickle.load(
    open("book_matrix.pkl", "rb")
)
book_cover_dict = pickle.load(
    open(
        "book_covers.pkl",
        "rb"
    )
)

# Recommendation function
def recommend_books(book_name):

    if book_name not in user_book_matrix.index:
        return []

    book_index = user_book_matrix.index.get_loc(
        book_name
    )

    distances, suggestions = model.kneighbors(
        user_book_matrix.iloc[
            book_index, :
        ].values.reshape(1, -1),
        n_neighbors=6
    )

    recommendations = []

    for i in range(
        1,
        len(suggestions[0])
    ):
        recommendations.append(
            user_book_matrix.index[
                suggestions[0][i]
            ]
        )

    return recommendations


# Page configuration
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="centered"
)

# Title
st.title("📚 Book Recommendation System")

st.markdown(
    """
    Select a book you have enjoyed and get
    personalized recommendations.
    """
)

# Dropdown
selected_book = st.selectbox(
    "Choose a Book",
    sorted(user_book_matrix.index)
)

# Button
if st.button("Recommend Books"):

    recommendations = recommend_books(
        selected_book
    )

    st.subheader(
        "Recommended Books"
    )

    for book in recommendations:

        col1, col2 = st.columns([1,3])

        with col1:
            st.image(
                book_cover_dict.get(book),
                width=100
            )

        with col2:
            st.write(book)
