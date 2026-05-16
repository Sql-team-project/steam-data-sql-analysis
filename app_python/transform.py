import pandas as pd
import logging

log=logging.getLogger(__name__)

MIN_REVIEWS=500
MIN_YEAR=2010

def transform_games(raw_games: pd.DataFrame) -> pd.DataFrame:
    log.info("Transforming games ...")
    df=raw_games.copy()

    df["date_release"]=pd.to_datetime(df["date_release"], errors="coerce")
    df["release_year"]=df["date_release"].dt.year
    df["price_final"]=pd.to_numeric(df["price_final"], errors="coerce").fillna(0.0)
    df["price_original"]=pd.to_numeric(df["price_original"], errors="coerce").fillna(0.0)

    before=len(df)
    df=df[(df["user_reviews"]>=MIN_REVIEWS) & (df["release_year"]>=MIN_YEAR)]
    log.info(f"Games sliced: {before} -> {len(df)} rows")

    return df.reset_index(drop=True)

def build_dim_games(games: pd.DataFrame) -> pd.DataFrame:
    cols=["app_id", "title", "date_release", "price_final", "price_original", "discount", "win", "mac", "linux", "steam_deck"]
    return games[cols].rename(columns={"app_id":"game_id"})

def build_dim_users(raw_users: pd.DataFrame) -> pd.DataFrame:
    log.info("Building dim_users ...")
    df=raw_users.copy()
    df["products"]=pd.to_numeric(df["products"], errors="coerce").fillna(0).astype(int)
    df["reviews"]=pd.to_numeric(df["reviews"], errors="coerce").fillna(0).astype(int)
    return df[["user_id", "products", "reviews"]].drop_duplicates(subset=["user_id"])

def process_metadata(raw_metadata: list, valid_game_ids: set):
    log.info("Parsing JSON metadata for tags...")
    
    meta_df=pd.DataFrame(raw_metadata)
    meta_df=meta_df[meta_df['app_id'].isin(valid_game_ids)]
    
    exploded=meta_df[['app_id', 'tags']].explode('tags').dropna()
    exploded=exploded.rename(columns={'app_id':'game_id', 'tags':'tag_name'})
    
    unique_tags=exploded[['tag_name']].drop_duplicates().reset_index(drop=True)
    unique_tags['tag_id']=unique_tags.index+1 
    
    bridge=pd.merge(exploded, unique_tags, on='tag_name', how='left')
    bridge_game_tags=bridge[['game_id', 'tag_id']]
    
    log.info(f"Generated {len(unique_tags)} unique tags and {len(bridge_game_tags)} bridge connections.")
    
    return unique_tags, bridge_game_tags

def transform_recs_chunk(chunk: pd.DataFrame, valid_game_ids: set, sample_rate: float=0.15) -> pd.DataFrame:
    df=chunk[chunk["app_id"].isin(valid_game_ids)].copy()
    if len(df)==0: return df
    
    df=df.sample(frac=sample_rate, random_state=42)
    
    df["date"]=pd.to_datetime(df["date"], errors="coerce")
    df["hours"]=pd.to_numeric(df["hours"], errors="coerce").fillna(0.0)
    df["is_recommended"]=df["is_recommended"].astype(bool)
    df["sentiment"]=df["is_recommended"].map({True: "Positive", False: "Negative"})
    
    return df.rename(columns={
        "app_id": "game_id",
        "date": "review_date",
        "hours": "hours_played",
    })[["user_id", "game_id", "hours_played", "review_date", "sentiment", "helpful", "funny"]].reset_index(drop=True)