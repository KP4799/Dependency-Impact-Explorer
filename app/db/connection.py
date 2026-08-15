from pathlib import Path
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

def get_driver():
    return GraphDatabase.driver(
        os.getenv("COGNODB_URI"),
        auth=(
            os.getenv("COGNODB_USERNAME"),
            os.getenv("COGNODB_PASSWORD"),
        ),
    )