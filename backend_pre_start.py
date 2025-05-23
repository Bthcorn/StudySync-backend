import logging

from sqlalchemy import Engine
from sqlmodel import Session, select

from config.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_retries = 60 * 5  # 5 minutes
wait_time = 1  # 1 second


def init_db(engine: Engine) -> None:
    try:
        with Session(engine) as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing database")
    init_db(engine)
    logger.info("Database initialized")


if __name__ == "__main__":
    main()
