import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("judge-worker: starting up")
    # Phase 2: Trust Judge logic will replace this loop
    while True:
        logger.info("judge-worker: running")
        time.sleep(10)


if __name__ == "__main__":
    main()
