from recommendation import MovieRecommender

recommender = MovieRecommender(
    "bolt://localhost:7687",
    "neo4j",
    "Yogi@3205"
)

username = input("Enter User Name (John/Alice/Bob): ")

print("\nMovies Rated By User:\n")

movies = recommender.get_user_movies(username)

for movie in movies:
    print(
        f"{movie['movie']} | Rating: {movie['rating']}"
    )

print("\nRecommended Movies:\n")

recommendations = recommender.recommend(username)

if recommendations:
    for movie in recommendations:
        print(
            f"{movie['movie']} | "
            f"Avg Rating: {movie['rating']} | "
            f"Common Interests: {movie['similarity']}"
        )
else:
    print("No recommendations found.")

recommender.close()