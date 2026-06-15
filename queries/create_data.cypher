// Users
CREATE
(:User {name:'John'}),
(:User {name:'Alice'}),
(:User {name:'Bob'});

// Genres
CREATE
(:Genre {name:'Sci-Fi'}),
(:Genre {name:'Action'}),
(:Genre {name:'Drama'}),
(:Genre {name:'Crime'});

// Movies
CREATE
(:Movie {title:'Inception', year:2010}),
(:Movie {title:'Interstellar', year:2014}),
(:Movie {title:'The Dark Knight', year:2008}),
(:Movie {title:'Avatar', year:2009}),
(:Movie {title:'Titanic', year:1997}),
(:Movie {title:'Oppenheimer', year:2023}),
(:Movie {title:'Dune', year:2021}),
(:Movie {title:'Joker', year:2019}),
(:Movie {title:'Avengers: Endgame', year:2019}),
(:Movie {title:'The Matrix', year:1999}),
(:Movie {title:'Fight Club', year:1999}),
(:Movie {title:'Forrest Gump', year:1994}),
(:Movie {title:'Gladiator', year:2000}),
(:Movie {title:'The Shawshank Redemption', year:1994}),
(:Movie {title:'Top Gun: Maverick', year:2022});