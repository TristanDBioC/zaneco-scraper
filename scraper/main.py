import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
sheet_id = os.getenv("SHEET_ID")
mongo_uri = os.getenv("MONGO_URI")
gid = "0"

csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Read the sheet into a DataFrame
df_new = pd.read_csv(csv_url)

# Sanitize: Replace U+202F (narrow no-break space) with regular space in all string columns
df_new = df_new.applymap(
    lambda x: x.replace('\u202f', ' ') if isinstance(x, str) else x
)

# Columns to use as unique key
unique_cols = ["POWER INTERRUPTION", "DATE", "AFFECTED AREA/S", "TIME INTERRUPTED"]

# Save to CSV as backup
data_folder = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_folder, exist_ok=True)
filename = datetime.now().strftime("%m-%Y.csv")
filepath = os.path.join(data_folder, filename)
if os.path.exists(filepath):
    df_existing = pd.read_csv(filepath)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=unique_cols, keep='last')
    df_combined.to_csv(filepath, index=False)
else:
    df_new.to_csv(filepath, index=False)

print(f"Data saved to {filepath}")

# Save to MongoDB
client = MongoClient(mongo_uri)
db = client.get_default_database()
collection = db.interruptions

# Prepare bulk upsert operations
operations = []
for _, row in df_new.iterrows():
    query = {col: row[col] for col in unique_cols}
    update = {"$set": row.to_dict()}
    operations.append(UpdateOne(query, update, upsert=True))

if operations:
    result = collection.bulk_write(operations)
    print(f"MongoDB: {result.upserted_count} new, {result.modified_count} updated.")

print(df_new.head())