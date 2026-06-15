MATCH (m:Movie {title:'Inception'}),(g:Genre {name:'Sci-Fi'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Interstellar'}),(g:Genre {name:'Sci-Fi'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Avatar'}),(g:Genre {name:'Sci-Fi'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Dune'}),(g:Genre {name:'Sci-Fi'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'The Matrix'}),(g:Genre {name:'Sci-Fi'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'The Dark Knight'}),(g:Genre {name:'Action'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Avengers: Endgame'}),(g:Genre {name:'Action'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Gladiator'}),(g:Genre {name:'Action'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Top Gun: Maverick'}),(g:Genre {name:'Action'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Titanic'}),(g:Genre {name:'Drama'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Forrest Gump'}),(g:Genre {name:'Drama'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Fight Club'}),(g:Genre {name:'Drama'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Oppenheimer'}),(g:Genre {name:'Drama'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'The Shawshank Redemption'}),(g:Genre {name:'Drama'})
CREATE (m)-[:BELONGS_TO]->(g);

MATCH (m:Movie {title:'Joker'}),(g:Genre {name:'Crime'})
CREATE (m)-[:BELONGS_TO]->(g);