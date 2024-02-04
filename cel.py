import fp
from celery import Celery
import feedparser
import logging

# Configure logging
logging.basicConfig(filename='feed_parser.log', level=logging.INFO)

app = Celery('feed_parser', broker='amqp://guest:guest@localhost:5672//')

@app.task
def parse_feed(feed_url):
    try:
        article_data =[]
        def extract_articles_from_feed(feed_url):
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
                if any(article['link'] == existing_article['link'] for existing_article in article):
                    continue
                article_data.append(article)  
        feeds = [
        'http://rss.cnn.com/rss/cnn_topstories.rss',
        'http://qz.com/feed',
        'http://feeds.foxnews.com/foxnews/politics',
        'http://feeds.reuters.com/reuters/businessNews',
        'http://feeds.feedburner.com/NewshourWorld',
        'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
        ]

          
       
        for feed_url in feeds:
            extract_articles_from_feed(feed_url)

        process_article.delay(article_data)

        logging.info(f"Article from {feed_url} successfully processed and enqueued.")
    except Exception as e:
        logging.error(f"Error processing feed {feed_url}: {str(e)}")




# celery_worker.py
from celery import Celery
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import psycopg2

app = Celery('feed_parser', broker='amqp://admin:admin@localhost:5672/myvhost')

# Connect to PostgreSQL database
conn = psycopg2.connect("dbname=news_article user=admin password=admin")

@app.task
def process_article(article_data):
    # article processing logic here
    try:

        category = classify_category(article_data['content'])
        save_to_database(article_data, category)
        logging.info(f"Article '{article_data['title']}' processed and saved to the database.")
    except Exception as e:
        logging.error(f"Error processing article '{article_data['title']}': {str(e)}")    

def classify_category(content):
    # category classification logic here

    # Tokenize, remove stop words and punctuation, and stem words
    tokens = word_tokenize(content.lower())
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Perform stemming using Porter Stemmer
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    # Check for keywords related to different categories
    terrorism_keywords = ['terrorism', 'protest', 'political', 'unrest', 'riot']
    positive_keywords = ['positive', 'uplifting']
    natural_disaster_keywords = ['natural', 'disaster']

    if any(keyword in stemmed_tokens for keyword in terrorism_keywords):
        return 'Terrorism/Protest/Political Unrest/Riot'
    elif any(keyword in stemmed_tokens for keyword in positive_keywords):
        return 'Positive/Uplifting'
    elif any(keyword in stemmed_tokens for keyword in natural_disaster_keywords):
        return 'Natural Disasters'
    else:
        return 'Others'

def save_to_database(article_data, category):
    # database saving logic here
    # Ensure to handle duplicates
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articles (title, content, pub_date, source_url, category)
        VALUES (%s, %s, %s, %s, %s)
    """, (article_data['title'], article_data['content'], article_data['pub_date'], article_data['link'], category))
    conn.commit()
    cursor.close()
    print("Article saved to the database.")
