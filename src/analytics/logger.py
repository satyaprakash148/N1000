import logging

def setup_logger():
    logging.basicConfig(
        filename="output/ratio_engine.log",
        level=logging.WARNING,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )