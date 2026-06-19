import io
import zipfile
import urllib.request
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import GraphDB

ML_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"


def download_dataset() -> dict:
    print("downloading movielens small dataset...")
    with urllib.request.urlopen(ML_URL) as resp:
        data = resp.read()
    z = zipfile.ZipFile(io.BytesIO(data))
    movies = pd.read_csv(z.open("ml-latest-small/movies.csv"))
    ratings = pd.read_csv(z.open("ml-latest-small/ratings.csv"))
    return {"movies": movies, "ratings": ratings}


def load_movies(db: GraphDB, movies: pd.DataFrame):
    rows = []
    for _, row in movies.iterrows():
        genres = [g for g in row["genres"].split("|") if g != "(no genres listed)"]
        rows.append({
            "movieId": int(row["movieId"]),
            "title": row["title"],
            "genres": genres,
        })

    cypher = """
    UNWIND $rows AS row
    MERGE (m:Movie {movieId: row.movieId})
    SET m.title = row.title
    WITH m, row
    UNWIND row.genres AS genreName
    MERGE (g:Genre {name: genreName})
    MERGE (m)-[:BELONGS_TO]->(g)
    """
    batch_size = 1000
    for i in range(0, len(rows), batch_size):
        db.query(cypher, {"rows": rows[i:i + batch_size]})
        print(f"  movies loaded: {i + len(rows[i:i + batch_size])}/{len(rows)}")


def load_ratings(db: GraphDB, ratings: pd.DataFrame):
    rows = ratings.to_dict("records")

    cypher = """
    UNWIND $rows AS row
    MERGE (u:User {userId: row.userId})
    WITH u, row
    MATCH (m:Movie {movieId: row.movieId})
    MERGE (u)-[r:RATED]->(m)
    SET r.rating = row.rating, r.timestamp = row.timestamp
    """
    batch_size = 2000
    for i in range(0, len(rows), batch_size):
        db.query(cypher, {"rows": rows[i:i + batch_size]})
        print(f"  ratings loaded: {i + len(rows[i:i + batch_size])}/{len(rows)}")


def main():
    data = download_dataset()
    print(f"movies: {len(data['movies'])}, ratings: {len(data['ratings'])}, "
          f"users: {data['ratings']['userId'].nunique()}")

    with GraphDB() as db:
        print("loading movies + genres...")
        load_movies(db, data["movies"])
        print("loading users + ratings...")
        load_ratings(db, data["ratings"])

    print("done")


if __name__ == "__main__":
    main()