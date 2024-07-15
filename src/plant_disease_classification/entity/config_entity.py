from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    roo_dir:Path
    source_URL:list
    local_data_file: Path
    unzip_dir: Path
