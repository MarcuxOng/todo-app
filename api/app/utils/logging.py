import logging
import sys
from pathlib import Path


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                filename=log_dir / "app.log",
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3,
                encoding='utf-8'
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


setup_logging()

logger = logging.getLogger(__name__)
