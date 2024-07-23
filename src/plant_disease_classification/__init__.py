import logging
import os
import sys

file_dir = "logs"
if not os.path.exists(file_dir):
    os.makedirs(file_dir)
filename = os.path.join("logs", "running_logs")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(filename=filename),
    ],
)


logger = logging.getLogger(__name__)
