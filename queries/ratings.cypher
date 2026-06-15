MATCH (u:User {name:'John'}),(m:Movie {title:'Inception'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'John'}),(m:Movie {title:'Interstellar'})
CREATE (u)-[:RATED {rating:4}]->(m);

MATCH (u:User {name:'John'}),(m:Movie {title:'The Matrix'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'John'}),(m:Movie {title:'Dune'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Alice'}),(m:Movie {title:'Titanic'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Alice'}),(m:Movie {title:'Interstellar'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Alice'}),(m:Movie {title:'Dune'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Alice'}),(m:Movie {title:'The Matrix'})
CREATE (u)-[:RATED {rating:4}]->(m);

MATCH (u:User {name:'Alice'}),(m:Movie {title:'Forrest Gump'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Bob'}),(m:Movie {title:'Avatar'})
CREATE (u)-[:RATED {rating:4}]->(m);

MATCH (u:User {name:'Bob'}),(m:Movie {title:'The Matrix'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Bob'}),(m:Movie {title:'Oppenheimer'})
CREATE (u)-[:RATED {rating:4}]->(m);

MATCH (u:User {name:'Bob'}),(m:Movie {title:'The Dark Knight'})
CREATE (u)-[:RATED {rating:5}]->(m);

MATCH (u:User {name:'Bob'}),(m:Movie {title:'Avengers: Endgame'})
CREATE (u)-[:RATED {rating:4}]->(m);