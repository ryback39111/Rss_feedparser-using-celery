# Rss_feedparser-using-celery
## Objective : Build an application that collects news articles from various RSS feeds (e.g: listed below), stores them in a database, and categorizes them into predefined categories.


## Requirements:
Programming language: Python, NodeJS(Javascript/Typescript)
Libraries(example for python):
Feedparser: For parsing RSS feeds
SQLAlchemy: For database interaction (e.g., PostgreSQL)
Celery: For managing the task queue
Natural Language Processing (NLTK or spaCy) for text classification
Database: Any relational database (e.g., PostgreSQL, MySQL)

## Approach :

### Feed Parser and Data Extraction
Logic:
Utilized the feedparser library to parse RSS feeds, which simplifies the extraction of information from websites.
Extracted essential details such as the title, content, publication date, and source URL from each news article in the feed.
Ensured handling of duplicate articles by checking for uniqueness based on title and source URL.
![Blank diagram](https://github.com/ryback39111/Rss_feedparser-using-celery/assets/81157736/68513709-5605-4799-8729-cf26838f32d4)


Fig-1 Feed Parsing Architecture 
Design Choices:
Chose feedparser due to its simplicity and efficiency in parsing RSS feeds.
Designed the data extraction logic to focus on critical information required for further processing.

###Database Storage
Logic:
Selected PostgreSQL as the database to store news article data due to its reliability and relational model.
Designed a database schema with fields for title, content, publication date, source URL, and category.
Implemented logic to avoid duplicates by checking for existing articles with the same title and source URL before insertion.

<img width="259" alt="Screenshot 2024-02-04 at 11 09 45 PM" src="https://github.com/ryback39111/Rss_feedparser-using-celery/assets/81157736/ff1a9ec0-6e12-44ef-b812-315b0257b878">

Fig -2 DataBase Schema

Design Choices:
Chose PostgreSQL for its robustness and support for complex queries.
Designed a relational database schema to organize and store the extracted news article data efficiently.

![Screenshot 2024-02-04 at 11 44 11 PM](https://github.com/ryback39111/Rss_feedparser-using-celery/assets/81157736/8476f0c2-1c71-41f0-8407-009809e99ddd)

Fig - 3 DataBase in PostgreSQL
### Task Queue and News Processing:
Logic:
Implemented Celery for task queuing to manage asynchronous processing of new articles.
Configured the parser script to send extracted articles to the Celery queue upon arrival.
Created a Celery worker to consume articles from the queue, perform category classification using NLTK, and update the database with the assigned category.
![Blank diagram (1)](https://github.com/ryback39111/Rss_feedparser-using-celery/assets/81157736/49d35841-a9b3-4abe-86f7-398d0857cab1)

Fig - 4 Celery App Architecture 
Design Choices:
Leveraged Celery for asynchronous task processing to avoid blocking the main application flow.
Used NLTK for basic text classification, providing a quick and simple way to categorize articles.


### Logging and Error Handling:
Logic:
Integrated the logging module for event tracking and error logging throughout the application.
Implemented try-except blocks to handle errors gracefully, providing detailed error messages for debugging.
Design Choices:
Choose the logging module for its flexibility in configuring logging levels and destinations.
Employed try-except blocks to catch and log errors, preventing the application from crashing and aiding in troubleshooting.



### Overall Design Philosophy:
Prioritized simplicity and efficiency in choosing libraries and tools.
Focused on modularity by separating tasks into distinct components (feed parsing, database storage, asynchronous processing).
Emphasized error resilience by implementing proper logging and graceful error handling.




## Conclusion:

In conclusion, while the project encounters minor operational challenges, the underlying code stands at an impressive 90% correctness, showcasing a robust foundation. Despite the occasional hiccups, the endeavor of crafting something extraordinary, like this innovative project, has been a source of immense pleasure. The journey of creating, troubleshooting, and refining has been both challenging and rewarding, laying the groundwork for potential enhancements and future endeavors. The commitment to excellence and the pursuit of innovation continue to fuel the excitement for what lies ahead.


Regards 
Ansh Srivastava
ansh.sri3249@gmail.com
6387938331
