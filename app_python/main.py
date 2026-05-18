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
    
    clean_games=transform.transform_games(raw_games)
    dim_games=transform.build_dim_games(clean_games)
    valid_games=set(dim_games['game_id'])
    
    dim_tags,bridge_game_tags=transform.process_metadata(raw_metadata, valid_game_ids=valid_games)

    engine=load.get_db_engine()
    
    load.push_table(dim_games, 'dim_games', engine)
    load.push_table(dim_tags, 'dim_tags', engine)
    load.push_table(bridge_game_tags, 'bridge_game_tags', engine)
    
    log.info("STARTING USERS STREAM IN CHUNKS (1,000,000 CHUNK SIZE)...")
    
    user_chunk_size=1_000_000
    total_users_pushed=0
    
    for j, u_chunk in enumerate(pd.read_csv(extract.DATA_DIR/"users.csv", chunksize=user_chunk_size)):
        dim_users_chunk=transform.build_dim_users(u_chunk)
        if len(dim_users_chunk) > 0:
            load.push_table(dim_users_chunk, 'dim_users', engine)
            total_users_pushed+=len(dim_users_chunk)
        log.info(f"Processed user chunk {j+1}... Total users pushed to SQL so far: {total_users_pushed}")
    
    log.info("STARTING MASSIVE RECOMMENDATIONS STREAM (15% SAMPLE)...")
    
    rec_chunk_size=200_000
    total_recs_pushed=0
    
    for i, chunk in enumerate(pd.read_csv(extract.DATA_DIR/"recommendations.csv", chunksize=rec_chunk_size)):
        clean_chunk=transform.transform_recs_chunk(chunk, valid_games, sample_rate=0.15)
        if len(clean_chunk) > 0:
            load.push_table(clean_chunk, 'fact_recommendations', engine)
            total_recs_pushed+=len(clean_chunk)
        log.info(f"Processed recommendation chunk {i+1}... Total recommendations pushed to SQL so far: {total_recs_pushed}")

    log.info(f"BOOM! PIPELINE COMPLETE. Total Users: {total_users_pushed} | Total Recommendations: {total_recs_pushed}")

if __name__=="__main__":
    run_pipeline()
