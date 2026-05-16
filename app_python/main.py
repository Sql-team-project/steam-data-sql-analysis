import logging
import pandas as pd
import extract
import transform
import load

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

def run_pipeline():
    log.info("STARTING STEAM DATA PIPELINE...")
    
    raw_games=extract.extract_games()
    raw_metadata=extract.extract_metadata()
    raw_users=extract.extract_users()
    
    clean_games=transform.transform_games(raw_games)
    dim_games=transform.build_dim_games(clean_games)
    valid_games=set(dim_games['game_id'])
    
    dim_tags,bridge_game_tags=transform.process_metadata(raw_metadata, valid_game_ids=valid_games)
    dim_users=transform.build_dim_users(raw_users)

    engine=load.get_db_engine()
    
    load.push_table(dim_games, 'dim_games', engine)
    load.push_table(dim_tags, 'dim_tags', engine)
    load.push_table(bridge_game_tags, 'bridge_game_tags', engine)
    load.push_table(dim_users,'dim_users',engine)
    
    log.info("STARTING MASSIVE RECOMMENDATIONS STREAM (15% SAMPLE)...")
    
    chunk_size=200_000
    total_pushed=0
    
    for i, chunk in enumerate(pd.read_csv(extract.DATA_DIR/"recommendations.csv", chunksize=chunk_size)):
        clean_chunk=transform.transform_recs_chunk(chunk, valid_games, sample_rate=0.15)
        if len(clean_chunk) > 0:
            load.push_table(clean_chunk, 'fact_recommendations', engine)
            total_pushed+=len(clean_chunk)
        log.info(f"Processed chunk {i+1}... Total rows pushed to SQL so far: {total_pushed}")

    log.info(f"BOOM! PIPELINE COMPLETE. Total recommendations loaded: {total_pushed}")

if __name__=="__main__":
    run_pipeline()