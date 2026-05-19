# Steam Analytics & ETL Data Warehouse

A complete, end-to-end Data Engineering and Analytics project that extracts, transforms, and loads (ETL) a massive Kaggle Steam dataset into a local Microsoft SQL Server database using Python, Pandas, and Docker.

---

## Part 1: Project Overview & Key Ideas

This project was built to handle, clean, and analyze a massive dataset of over 41 million Steam user reviews and 50,000+ games. Because processing this much data locally can crash a standard machine, we engineered a highly optimized pipeline. 

**As our Data is more than the github limit of files 500mb we are nto able to upload it but here is the Kaggle link of it.**
https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam?select=users.csv


### Core Engineering Concepts
* **Memory Optimization (Chunking):** Instead of loading a 41-million-row CSV into RAM all at once, our Python orchestrator streams the data in chunks of 200,000 rows. It processes the chunk, pushes it to SQL, dumps the memory, and grabs the next one.
* **Representative Sampling:** We applied a deterministic `15%` random sample to the massive recommendations file, shrinking it down to a highly efficient `~5.5 million` rows for local processing without losing the statistical integrity of the data.
* **The Snowflake Schema:** We designed a fully normalized relational database architecture. We use a central Fact table for transactions (reviews), surrounding Dimension tables (games, users, tags), and a Many-to-Many Bridge table to connect games to their multiple genres/tags.
* **JSON Parsing:** Handled messy `JSON Lines` metadata formats by unpacking arrays and mapping them properly to our SQL bridge tables.

###The 10 Analytical Questions We Answered
Using advanced SQL features like Window Functions (`ROW_NUMBER`, `NTILE`, `RANK`), CTEs, and multi-table Joins, we built a `queries.sql` file that answers these core business questions:

1. **The Tag Synergy Matrix:** Which combination of tags produces the highest ratio of positive reviews and playtime?
2. **The Loyalty Tier Breakdown:** If we group users into 4 quartiles based on library size, how does engagement differ?
3. **Review Bomber Detection:** Identifying toxic users who review-bomb games without actually playing them.
4. **Platform Tax & Deck Boost:** Do multi-platform (Win/Mac/Linux) games charge a premium compared to Windows-only games?
5. **Hype vs. Longevity Curve:** How does a game's positive ratio change from Launch Month vs 1+ years later?
6. **The Meme Game Detector:** Which specific genres/tags generate the highest ratio of "Funny" to "Helpful" votes?
7. **The Discount Diver Behavior:** Do users who only buy heavily discounted games play longer than full-price buyers?
8. **The Sleeper Hit Curve:** Identifying games where Year 2 reviews completely doubled Year 1 reviews.
9. **Reviewer Fatigue:** Do hardcore reviewers become more critical over time?
10. **The Lockdown Phenomenon:** Which games became absolute viral hits during the peak of the 2020-2021 pandemic?

---

## Part 2: How to Install & Run Locally

Follow these steps to spin this project up on your own local machine.

### Prerequisites
* **Python 3.9+** installed.
* **Git** installed.
* **MS SQL Server** running locally (either via Docker or natively).

### Step 1: Clone the Repository
Open your terminal and pull down the project:

    git clone https://github.com/YourOrganizationName/sql_project.git
    cd sql_project

### Step 2: Configure Your Database Settings !
Before running anything, you must update the connection credentials to match your own machine! Open the `load.py` file and change these variables:

    DB_USER = 'Your_SQL_Username'
    DB_PASSWORD = 'Your_Actual_Password'
    DB_HOST = 'localhost'
    DB_PORT = '1433'
    DB_NAME = 'SteamAnalytics'

### Step 3: Install Dependencies & Build Schema
Install the required libraries to run the ETL pipeline:

    pip install pandas sqlalchemy pymssql

Next, open your SQL client, connect to your server, and run the `sql/schema.sql` file to create the empty database tables.

### Step 4: Run the ETL Pipeline
Fire off the main orchestrator script. This will extract the data, clean it, and stream all 5.5 million rows straight into your database:

    python app_python/main.py

### Step 5: Run the Analytics
Once the terminal says "PIPELINE COMPLETE", open `sql/queries.sql`. You can execute the entire file to view the answers to all 10 analytical questions!
