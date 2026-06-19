import streamlit as st
from db import GraphDB
from recommend import recommend

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title("🎬 Graph-Based Movie Recommender")
st.caption("Neo4j + collaborative filtering, with genre-based cold-start fallback")


@st.cache_resource
def get_db():
    return GraphDB()


@st.cache_data(ttl=180)
def get_all_user_ids(_db):
    rows = _db.query("MATCH (u:User) RETURN u.userId AS userId ORDER BY userId")
    return [r["userId"] for r in rows]


@st.cache_data(ttl=180)
def get_user_history(_db, user_id):
    return _db.query(
        """
        MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)
        RETURN m.title AS title, r.rating AS rating
        ORDER BY r.rating DESC LIMIT 10
        """,
        {"userId": user_id},
    )


db = get_db()
user_ids = get_all_user_ids(db)

if not user_ids:
    st.warning("No users found. Run `python data/load_movielens.py` first to load data.")
    st.stop()

user_id = st.selectbox("Select a user", user_ids)

with st.expander("This user's top-rated movies"):
    history = get_user_history(db, user_id)
    if history:
        for h in history:
            st.write(f"⭐ {h['rating']} — {h['title']}")
    else:
        st.write("No ratings yet (new / cold-start user).")

if st.button("Get Recommendations", type="primary"):
    with st.spinner("Computing similarity and ranking candidates..."):
        recs = recommend(db, user_id)

    strategy_label = {
        "collaborative_filtering": "🤝 Collaborative filtering (similar users)",
        "cold_start": "🌱 Cold-start (genre/popularity based)",
    }
    st.info(f"Strategy used: **{strategy_label.get(recs['strategy'], recs['strategy'])}**")

    if not recs["results"]:
        st.warning("No recommendations could be generated.")
    else:
        for row in recs["results"]:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{row['title']}**")
            with col2:
                st.write(f"⭐ {row['predictedRating']}")