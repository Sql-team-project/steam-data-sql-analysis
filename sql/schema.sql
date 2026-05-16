-- First create the database and use it before running SQL code to create the tables.

-- 1.
-- CREATE DATABASE SteamAnalytics;
-- USE SteamAnalytics;

-- 2.
-- CREATE TABLE dim_games (
--     game_id INT PRIMARY KEY,
--     title NVARCHAR(MAX),
--     date_release DATE,
--     price_final FLOAT,
--     price_original FLOAT,
--     discount FLOAT,
--     win BIT,
--     mac BIT,
--     linux BIT,
--     steam_deck BIT
-- );

-- CREATE TABLE dim_users (
--     user_id INT PRIMARY KEY,
--     products INT,
--     reviews INT
-- );

-- CREATE TABLE dim_tags (
--     tag_id INT PRIMARY KEY,
--     tag_name NVARCHAR(255)
-- );

-- CREATE TABLE bridge_game_tags (
--     game_id INT FOREIGN KEY REFERENCES dim_games(game_id),
--     tag_id INT FOREIGN KEY REFERENCES dim_tags(tag_id),
--     PRIMARY KEY (game_id, tag_id)
-- );

-- CREATE TABLE fact_recommendations (
--     review_id INT IDENTITY(1,1) PRIMARY KEY,
--     user_id INT FOREIGN KEY REFERENCES dim_users(user_id),
--     game_id INT FOREIGN KEY REFERENCES dim_games(game_id),
--     hours_played FLOAT,
--     review_date DATE,
--     sentiment VARCHAR(50),
--     helpful INT,
--     funny INT
-- );