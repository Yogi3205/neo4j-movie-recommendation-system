# 🎬 Movie Recommendation System using Neo4j and Python

## 📌 Project Overview

This project demonstrates a Movie Recommendation System built using Neo4j Graph Database and Python.

The system stores users, movies, genres, actors, and directors as graph nodes and leverages graph relationships to generate personalized movie recommendations.

Unlike traditional relational databases, Neo4j efficiently handles highly connected data, making it ideal for recommendation systems.

---

## 🚀 Features

* Store movie information in Neo4j
* Store user ratings as graph relationships
* Manage genres, actors, and directors
* Find users with similar movie preferences
* Generate personalized movie recommendations
* Integrate Neo4j with Python
* Execute Cypher queries from Python

---

## 🛠️ Technologies Used

* Neo4j Graph Database
* Cypher Query Language
* Python 3.x
* Neo4j Python Driver
* Git & GitHub

---

## 📊 Graph Data Model

### Nodes

* User
* Movie
* Genre
* Actor
* Director

### Relationships

```text
(User)-[:RATED]->(Movie)

(Movie)-[:BELONGS_TO]->(Genre)

(Actor)-[:ACTED_IN]->(Movie)

(Director)-[:DIRECTED]->(Movie)
```

---

## 🏗️ System Architecture

```text
+-------------------+
|      User         |
+-------------------+
          |
          v
+-------------------+
| Python Application|
+-------------------+
          |
          v
+-------------------+
| Neo4j Driver      |
+-------------------+
          |
          v
+-------------------+
| Neo4j Database    |
+-------------------+
```

---

## 📁 Project Structure

```text
movie-recommendation-system/
│
├── app.py
├── recommendation.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── screenshots/
│   ├── graph.png
│   ├── recommendation_output.png
│
└── queries/
    ├── create_data.cypher
    └── recommendation_query.cypher
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/neo4j-movie-recommendation-system.git

cd neo4j-movie-recommendation-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Neo4j Setup

1. Install Neo4j Desktop
2. Create a database instance
3. Start the database
4. Open Neo4j Browser
5. Execute the Cypher scripts to create sample data

Example connection:

```python
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "your_password"
```

---

## ▶️ Running the Project

```bash
python app.py
```

Example:

```text
Enter User Name (John/Alice/Bob): Alice
```

---

## 🧠 Recommendation Logic

The recommendation engine uses Collaborative Filtering.

### Steps

1. Find users who have rated similar movies.
2. Calculate common movie interests.
3. Identify movies rated by similar users.
4. Exclude movies already watched by the target user.
5. Rank recommendations by:

   * Common interests
   * Average rating

### Recommendation Query Concept

```text
Alice
  |
  +--> Interstellar
  |
  +--> Dune
  |
  +--> The Matrix

          ^
          |
         John

John also liked:

Inception
Avatar
Oppenheimer

=> Recommend to Alice
```

---

## 🔍 Sample Cypher Queries

### View User Ratings

```cypher
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.name, m.title, r.rating
```

### Find Similar Users

```cypher
MATCH (u:User {name:'Alice'})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
WHERE other <> u
RETURN other.name, COUNT(m) AS CommonMovies
ORDER BY CommonMovies DESC
```

### Find Recommended Movies

```cypher
MATCH (u:User {name:'Alice'})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
MATCH (other)-[:RATED]->(recommended:Movie)
WHERE NOT EXISTS {
 MATCH (u)-[:RATED]->(recommended)
}
RETURN DISTINCT recommended.title
```

---

## 📈 Sample Output

```text
Enter User Name (John/Alice/Bob): Alice

Movies Rated By User:

Interstellar | Rating: 5
Titanic | Rating: 5
Dune | Rating: 5
Forrest Gump | Rating: 5
The Matrix | Rating: 4

Recommended Movies:

Inception | Avg Rating: 5.0 | Common Interests: 3
The Dark Knight | Avg Rating: 5.0 | Common Interests: 1
Avatar | Avg Rating: 4.0 | Common Interests: 1
Oppenheimer | Avg Rating: 4.0 | Common Interests: 1
```

---

## 🎯 Learning Outcomes

Through this project, I learned:

* Graph Database Fundamentals
* Neo4j Architecture
* Cypher Query Language
* Graph Modeling
* Relationship Traversal
* Collaborative Filtering
* Python-Neo4j Integration
* Git and GitHub Workflow

---

## 🔮 Future Enhancements

* Streamlit Web Interface
* Movie Search Functionality
* MovieLens Dataset Integration
* Neo4j Graph Data Science Algorithms
* User Authentication
* REST API Integration
* Docker Deployment

---

## 👨‍💻 Author

Yogi K.

Neo4j Movie Recommendation System Project

Built for learning Graph Databases, Neo4j, and Recommendation Systems.
