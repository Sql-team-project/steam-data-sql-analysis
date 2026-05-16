import pandas as pd
from sqlalchemy import create_engine
import logging

log=logging.getLogger(__name__)

DB_USER='SA'
DB_PASSWORD='077809766E1' 
DB_HOST='localhost'
DB_PORT='1433'
DB_NAME='SteamAnalytics'

def get_db_engine():
    connection_string=f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def push_table(df: pd.DataFrame, table_name: str, engine):
    log.info(f"Pushing {len(df)} rows to '{table_name}'...")
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        log.info(f"  -> {table_name} loaded successfully.")
    except Exception as e:
        log.error(f"  -> Error loading {table_name}: {e}")