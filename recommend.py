from db import GraphDB

MIN_COMMON_MOVIES = 3
MIN_RATINGS_FOR_CF = 4
TOP_K_SIMILAR_USERS = 25
TOP_N_RECOMMENDATIONS = 10


def get_similar_users(db: GraphDB, user_id: int):
    cypher = """
    MATCH (u1:User {userId: $userId})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
    WHERE u1 <> u2
    WITH u1, u2, collect({r1: r1.rating, r2: r2.rating}) AS pairs
    WHERE size(pairs) >= $minCommon
    WITH u2,
         size(pairs) AS commonCount,
         reduce(s = 0.0, p IN pairs | s + p.r1 * p.r2) AS dot,
         sqrt(reduce(s = 0.0, p IN pairs | s + p.r1 ^ 2)) AS norm1,
         sqrt(reduce(s = 0.0, p IN pairs | s + p.r2 ^ 2)) AS norm2
    WHERE norm1 > 0 AND norm2 > 0
    RETURN u2.userId AS userId, dot / (norm1 * norm2) AS similarity, commonCount
    ORDER BY similarity DESC, commonCount DESC
    LIMIT $topK
    """
    return db.query(cypher, {
        "userId": user_id,
        "minCommon": MIN_COMMON_MOVIES,
        "topK": TOP_K_SIMILAR_USERS,
    })


def recommend_collaborative(db: GraphDB, user_id: int):
    similar_users = get_similar_users(db, user_id)
    if not similar_users:
        return []

    cypher = """
    UNWIND $similarUsers AS su
    MATCH (other:User {userId: su.userId})-[r:RATED]->(rec:Movie)
    WHERE NOT EXISTS {
        MATCH (:User {userId: $userId})-[:RATED]->(rec)
    }
    WITH rec, su.similarity AS sim, r.rating AS rating
    WITH rec,
         sum(sim * rating) AS weightedSum,
         sum(sim) AS simSum,
         count(*) AS supportCount
    RETURN rec.title AS title,
           round(weightedSum / simSum, 2) AS predictedRating,
           supportCount
    ORDER BY predictedRating DESC, supportCount DESC
    LIMIT $topN
    """
    return db.query(cypher, {
        "userId": user_id,
        "similarUsers": similar_users,
        "topN": TOP_N_RECOMMENDATIONS,
    })


def recommend_cold_start(db: GraphDB, user_id: int):
    cypher = """
    MATCH (u:User {userId: $userId})-[:RATED]->(:Movie)-[:BELONGS_TO]->(g:Genre)
    WITH u, collect(DISTINCT g.name) AS likedGenres
    MATCH (rec:Movie)-[:BELONGS_TO]->(g:Genre)
    WHERE g.name IN likedGenres
      AND NOT EXISTS { MATCH (u)-[:RATED]->(rec) }
    MATCH (rec)<-[r:RATED]-(:User)
    WITH rec, avg(r.rating) AS avgRating, count(r) AS numRatings
    WHERE numRatings >= 5
    WITH rec, avgRating, numRatings,
         (avgRating * numRatings + 3.0 * 10) / (numRatings + 10) AS bayesianScore
    RETURN rec.title AS title, round(bayesianScore, 2) AS predictedRating, numRatings AS supportCount
    ORDER BY bayesianScore DESC
    LIMIT $topN
    """
    results = db.query(cypher, {"userId": user_id, "topN": TOP_N_RECOMMENDATIONS})
    if results:
        return results

    cypher_global = """
    MATCH (rec:Movie)<-[r:RATED]-(:User)
    WITH rec, avg(r.rating) AS avgRating, count(r) AS numRatings
    WHERE numRatings >= 20
    WITH rec, avgRating, numRatings,
         (avgRating * numRatings + 3.0 * 10) / (numRatings + 10) AS bayesianScore
    RETURN rec.title AS title, round(bayesianScore, 2) AS predictedRating, numRatings AS supportCount
    ORDER BY bayesianScore DESC
    LIMIT $topN
    """
    return db.query(cypher_global, {"topN": TOP_N_RECOMMENDATIONS})


def recommend(db: GraphDB, user_id: int):
    existing_ratings = db.query(
        "MATCH (:User {userId: $userId})-[r:RATED]->() RETURN count(r) AS c",
        {"userId": user_id},
    )
    n_ratings = existing_ratings[0]["c"] if existing_ratings else 0

    if n_ratings < MIN_RATINGS_FOR_CF:
        return {"strategy": "cold_start", "results": recommend_cold_start(db, user_id)}

    results = recommend_collaborative(db, user_id)
    if not results:
        return {"strategy": "cold_start", "results": recommend_cold_start(db, user_id)}
    return {"strategy": "collaborative_filtering", "results": results}


if __name__ == "__main__":
    user_id = int(input("Enter userId (e.g. 1): "))
    with GraphDB() as db:
        result = recommend(db, user_id)
        print(f"\nStrategy used: {result['strategy']}\n")
        for row in result["results"]:
            print(f"{row['title']} | Predicted: {row['predictedRating']} "
                  f"| Support: {row['supportCount']}")