
# zaneco-scraper

## Project Overview
This project is a web scraper designed to extract and archive live status updates of power interruptions from ZANECO's (Zamboanga del Norte Electric Cooperative) public monitoring spreadsheet. The goal is to build a long-term historical database of power interruptions for analysis and reference.


## Files
- **main.py**: Contains the scraper script. It fetches the latest data from ZANECO's live Google Sheet, sanitizes and deduplicates entries, saves a backup CSV, and upserts the data into a MongoDB database.
- **docker-compose.yml**: Defines the services for the Docker stack, including the scraper and a MongoDB database. The scraper is configured to run every hour.


## Setup Instructions
1. Ensure you have Docker and Docker Compose installed on your machine.
2. Clone this repository to your local machine:
   ```
   git clone https://github.com/TristanDBioC/zaneco-scraper.git
   cd zaneco-scraper
   ```
3. Create a `.env` file in the `scraper` directory based on `.env.example`, and fill in the required values (e.g., Google Sheet ID, MongoDB URI).
4. Build and start the stack:
   ```
   docker compose up --build
   ```


## Usage
To start the scraper and database, run:
```
docker compose up --build
```
This will build the Docker images (if needed) and start both the scraper and MongoDB services. The scraper will fetch and update data every hour.


## Future Enhancements
- Add more robust error handling and logging for better monitoring of the scraper's performance.
- Provide a simple API or dashboard for querying the historical database.