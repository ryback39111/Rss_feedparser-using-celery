import feedparser



# Define the list to store the extracted articles
article_1 = []
# Define the function to extract articles from a single RSS feed
def extract_articles_from_feed(feed_url):
    # Parse the RSS feed using feedparser
    feed = feedparser.parse(feed_url)

    # Loop through each entry in the feed
    for entry in feed.entries:
        # Extract the relevant information
        article = {
            'title': entry.title,
            'content': entry.get('summary', entry.get('description', '')),
            'pub_date': entry.get('published', entry.get('updated', entry.get('published_parsed', None))),
            'link': entry.link,
            
        }

        # Check for duplicates
        if any(article['link'] == existing_article['link'] for existing_article in article_1):
            continue

        # Add the article to the list
        article_1.append(article)

# Define the list of RSS feeds to parse
feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

# Loop through each feed and extract articles
for feed_url in feeds:
    extract_articles_from_feed(feed_url)

#Print the number of extracted articles
print(f'Extracted {len(article_1)} articles')


#engine = create_engine("postgresql://admin:admin@localhost:5432/news_article")

import psycopg2
from psycopg2 import sql

# Replace these values with your database details
db_params = {
    'dbname': 'news_article',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}


# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(**db_params)
conn = psycopg2.connect(**db_params)
# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the SQL query to insert data into the database
insert_query = sql.SQL("""
    INSERT INTO articles (title, content, pub_date, source_url)
    VALUES (%s, %s, %s, %s)
""")

# Loop through the list of dictionaries and insert data into the database
for feed in article_1:
    cursor.execute(insert_query, (feed['title'], feed['content'], feed['pub_date'], feed['link']))

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

def is_duplicate(article_1):
    cursor = conn.cursor()

    # Check for duplicates based on title and source URL
    cursor.execute("""
        SELECT id FROM articles
        WHERE title = %s AND source_url = %s
    """, (article_1['title'], article_1['link']))

    duplicate = cursor.fetchone() is not None

    cursor.close()
    return duplicate

def save_to_database(article_1, category):
    # Check for duplicates before saving
    if not is_duplicate(article_1):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, content, pub_date, source_url, category)
            VALUES (%s, %s, %s, %s, %s)
        """, (article_1['title'], article_1['content'], article_1['pub_date'], article_1['link'], category))
        conn.commit()
        cursor.close()
        print("Article saved to the database.")
    else:
        print("Duplicate article. Skipped saving to the database.")