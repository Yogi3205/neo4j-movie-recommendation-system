MATCH (n) RETURN n LIMIT 100;

MATCH (u:User {userId: 1})-[r:RATED]->(m:Movie)-[:BELONGS_TO]->(g:Genre)
RETURN u, r, m, g
LIMIT 50;

MATCH path = (u1:User {userId: 1})-[:RATED]->(m:Movie)<-[:RATED]-(u2:User)
RETURN path
LIMIT 30;

MATCH (n) RETURN labels(n)[0] AS type, count(*) AS count;

MATCH (u:User)-[r:RATED]->()
WITH u, count(r) AS c
WHERE c < 4
RETURN u.userId, c LIMIT 10;