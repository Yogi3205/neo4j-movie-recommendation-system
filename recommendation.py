from neo4j import GraphDatabase


class MovieRecommender:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    def recommend(self, username):

        query = """
        MATCH (u:User {name:$username})-[:RATED]->(commonMovie:Movie)<-[:RATED]-(other:User)

        WHERE other <> u

        WITH u, other, COUNT(commonMovie) AS commonMovies

        MATCH (other)-[r:RATED]->(recommended:Movie)

        WHERE NOT EXISTS {
            MATCH (u)-[:RATED]->(recommended)
        }

        RETURN
            recommended.title AS movie,
            AVG(r.rating) AS avgRating,
            commonMovies

        ORDER BY commonMovies DESC, avgRating DESC

        LIMIT 10
        """

        with self.driver.session(
            database="movie-recommandation-system"
        ) as session:

            result = session.run(
                query,
                username=username
            )

            return [
                {
                    "movie": record["movie"],
                    "rating": round(record["avgRating"], 2),
                    "similarity": record["commonMovies"]
                }
                for record in result
            ]

    def get_user_movies(self, username):

        query = """
        MATCH (u:User {name:$username})-[r:RATED]->(m:Movie)
        RETURN m.title AS movie, r.rating AS rating
        ORDER BY rating DESC
        """

        with self.driver.session(
            database="movie-recommandation-system"
        ) as session:

            result = session.run(
                query,
                username=username
            )

            return [
                {
                    "movie": record["movie"],
                    "rating": record["rating"]
                }
                for record in result
            ]

    def close(self):
        self.driver.close()