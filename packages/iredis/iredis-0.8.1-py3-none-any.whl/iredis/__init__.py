import os
import logging
from pathlib import Path

__version__ = "0.8.1"


logging.basicConfig(
    filename=os.path.join(os.getenv("HOME"), ".iredis.log"),
    filemode="a",
    format="%(levelname)5s %(message)s",
    level="DEBUG",
)

logger = logging.getLogger(__name__)
logger.info("------ iRedis ------")
project_path = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
