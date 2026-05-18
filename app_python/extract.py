import pandas as pd
import json
from pathlib import Path
import logging

log=logging.getLogger(__name__)

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"/"archive"

def extract_games() -> pd.DataFrame:
    log.info("Extracting games.csv ...")
    return pd.read_csv(DATA_DIR/"games.csv")

def extract_metadata() -> list:
    log.info("Extracting games_metadata.json ...")
    data=[]
    with open(DATA_DIR/"games_metadata.json", 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data
