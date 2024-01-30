from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ARRAY, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InstagramPost(Base):
    __tablename__ = 'instagram_posts'

    id = Column(BigInteger, primary_key=True)
    input_url = Column(String)
    type = Column(String)
    short_code = Column(String)
    caption = Column(String)
    hashtags = Column(ARRAY(String))  # Use ARRAY for PostgreSQL. Adjust if using another DBMS
    mentions = Column(ARRAY(String))  # Use ARRAY for PostgreSQL. Adjust if using another DBMS
    url = Column(String)
    comments_count = Column(Integer)
    first_comment = Column(String)
    latest_comments = Column(String)
    dimensions_height = Column(Integer)
    dimensions_width = Column(Integer)
    display_url = Column(String)
    images = Column(String)  # Consider changing to ARRAY if storing multiple image URLs
    video_url = Column(String)
    alt = Column(String)
    likes_count = Column(Integer)
    video_view_count = Column(Float)
    video_play_count = Column(Float)
    timestamp = Column(DateTime)
    child_posts = Column(String)  # Consider changing to ARRAY or another structure if storing multiple child posts
    owner_full_name = Column(String)
    owner_username = Column(String)
    owner_id = Column(BigInteger)
    product_type = Column(String)
    video_duration = Column(Float)
    is_sponsored = Column(Boolean)
    tagged_users = Column(String)  # Consider changing to ARRAY or JSON if storing structured data
    is_pinned = Column(Boolean)
    location_name = Column(String)
    location_id = Column(Float)
