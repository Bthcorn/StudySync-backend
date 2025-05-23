import logging

from sqlmodel import Session

from config.db import init_db, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    init()
    logger.info("Initial data has been created")


if __name__ == "__main__":
    main()
