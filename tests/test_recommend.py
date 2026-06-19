import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recommend import recommend, MIN_RATINGS_FOR_CF


def make_mock_db(rating_count, cf_results=None, cold_start_results=None):
    db = MagicMock()

    def fake_query(cypher, params=None):
        if "count(r) AS c" in cypher:
            return [{"c": rating_count}]
        if "u1, u2, collect" in cypher:
            return [{"userId": 2, "similarity": 0.9, "commonCount": 3}] if cf_results else []
        if "weightedSum" in cypher:
            return cf_results or []
        if "likedGenres" in cypher or "bayesianScore" in cypher:
            return cold_start_results or []
        return []

    db.query.side_effect = fake_query
    return db


def test_new_user_gets_cold_start():
    db = make_mock_db(
        rating_count=0,
        cold_start_results=[{"title": "Popular Movie", "predictedRating": 4.2, "supportCount": 50}],
    )
    result = recommend(db, user_id=999)
    assert result["strategy"] == "cold_start"
    assert result["results"][0]["title"] == "Popular Movie"


def test_active_user_gets_cf():
    db = make_mock_db(
        rating_count=MIN_RATINGS_FOR_CF + 5,
        cf_results=[{"title": "Inception", "predictedRating": 4.8, "supportCount": 3}],
    )
    result = recommend(db, user_id=1)
    assert result["strategy"] == "collaborative_filtering"
    assert result["results"][0]["title"] == "Inception"


def test_cf_falls_back_when_no_results():
    db = make_mock_db(
        rating_count=MIN_RATINGS_FOR_CF + 5,
        cf_results=None,
        cold_start_results=[{"title": "Fallback Movie", "predictedRating": 3.9, "supportCount": 20}],
    )
    result = recommend(db, user_id=1)
    assert result["strategy"] == "cold_start"
    assert result["results"][0]["title"] == "Fallback Movie"


def test_threshold_is_enforced():
    db_below = make_mock_db(
        rating_count=MIN_RATINGS_FOR_CF - 1,
        cold_start_results=[{"title": "X", "predictedRating": 4.0, "supportCount": 10}],
    )
    db_above = make_mock_db(
        rating_count=MIN_RATINGS_FOR_CF + 1,
        cf_results=[{"title": "Y", "predictedRating": 4.0, "supportCount": 2}],
    )

    assert recommend(db_below, user_id=1)["strategy"] == "cold_start"
    assert recommend(db_above, user_id=1)["strategy"] == "collaborative_filtering"