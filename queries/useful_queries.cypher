Show all movies

    MATCH (m:Movie)
    RETURN m.title,m.year

Show user ratings

    MATCH (u:User)-[r:RATED]->(m:Movie)
    RETURN u.name,m.title,r.rating

Show similar users

    MATCH (u:User {name:'Alice'})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
    WHERE other <> u
    RETURN other.name, COUNT(m) AS CommonMovies
    ORDER BY CommonMovies DESC

Show recommendations

    MATCH (u:User {name:'Alice'})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)

    MATCH (other)-[r:RATED]->(recommended:Movie)

    WHERE NOT EXISTS {
        MATCH (u)-[:RATED]->(recommended)
    }

    RETURN
    recommended.title,
    AVG(r.rating) AS AvgRating
    ORDER BY AvgRating DESC

Top Rated Movies

    MATCH (:User)-[r:RATED]->(m:Movie)
    RETURN
    m.title,
    AVG(r.rating) AS AvgRating,
    COUNT(r) AS TotalRatings
    ORDER BY AvgRating DESC