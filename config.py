import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

    @classmethod
    def validate(cls):
        if not cls.NEO4J_PASSWORD:
            raise EnvironmentError(
                "NEO4J_PASSWORD not set. Copy .env.example to .env and fill it in."
            )