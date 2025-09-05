from app.db.session import engine
from app.db import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        logger.info("Creating tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
