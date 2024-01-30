from database import engine
import models

import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv("MY_APIFY_TOKEN")
DATASET = os.getenv("APIFY_DATASET")

oauth_url = f"https://api.apify.com/v2/datasets/{DATASET}/items?token={API_KEY}"
models.Base.metadata.create_all(bind=engine)

res = requests.get(url=oauth_url)

with open("token.json", "w") as f:
    f.write(json.dumps(res.json(), indent=4))

df = pd.DataFrame(res.json())

# Function to safely serialize a column to JSON string
def safe_json_serialize(s):
    try:
        return json.dumps(s) if not pd.isnull(s) else None
    except (TypeError, ValueError):
        return None

# Serialize JSON-like columns to JSON strings
json_like_columns = ['hashtags', 'mentions', 'taggedUsers', 'latestComments', 'childPosts']
for col in json_like_columns:
    df[col] = df[col].apply(lambda x: safe_json_serialize(json.loads(x)) if isinstance(x, str) else None)

# Convert 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Replace 'NaN' with None to ensure compatibility with database
df = df.where(pd.notnull(df), None)

# Display changes and data types to verify adjustments
print(df.head())
print(df.dtypes)

# Convert 'timestamp' to datetime format, if not already
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Handle 'isPinned' column if it contains mixed types (True/False/None)
df['isPinned'] = df['isPinned'].apply(lambda x: True if x == 'True' else False if x == 'False' else None)
# Rename the 'inputUrl' column to 'input_url' to match the database schema
df.rename(columns={
    'inputUrl': 'input_url',
    'shortCode': 'short_code',
    'commentsCount': 'comments_count',
    'firstComment': 'first_comment',
    'latestComments': 'latest_comments',
    'dimensionsHeight': 'dimensions_height',
    'dimensionsWidth': 'dimensions_width',
    'displayUrl': 'display_url',
    'videoUrl': 'video_url',
    'likesCount': 'likes_count',
    'videoViewCount': 'video_view_count',
    'videoPlayCount': 'video_play_count',
    'timestamp': 'timestamp',
    'childPosts': 'child_posts',
    'ownerFullName': 'owner_full_name',
    'ownerUsername': 'owner_username',
    'ownerId': 'owner_id',
    'productType': 'product_type',
    'videoDuration': 'video_duration',
    'isSponsored': 'is_sponsored',
    'taggedUsers': 'tagged_users',
    'isPinned': 'is_pinned',
    'locationName': 'location_name',
    'locationId': 'location_id'
}, 
inplace=True
)
# Now you can attempt to insert the DataFrame into the PostgreSQL table again
df = df.drop_duplicates(subset=['id'])
df.to_sql('instagram_posts', engine, if_exists='append', index=False)
