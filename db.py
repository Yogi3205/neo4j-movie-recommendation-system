import logging
from neo4j import GraphDatabase
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphDB:
    def __init__(self):
        Config.validate()
        self._driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD),
        )

    def close(self):
        self._driver.close()

    def query(self, cypher: str, parameters: dict | None = None):
        parameters = parameters or {}
        try:
            with self._driver.session(database=Config.NEO4J_DATABASE) as session:
                result = session.run(cypher, parameters)
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"query failed: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()