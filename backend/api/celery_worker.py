from celery import Celery
import logging
import subprocess
import os
import redis
from scrapy.crawler import CrawlerProcess
from .crud import reset_colleges_table
from .database import AsyncSessionLocal
from collegescraper.collegescraper.spiders.colleges import CollegesSpider

# Initialize Celery with SQLAlchemy as the broker
# celery_app = Celery(
#     "collegescraper",
#     broker="redis://localhost:6379/0",  # Use Redis as the broker
#     backend="redis://localhost:6379/0",  # Use Redis as the results backend
# )

redis_url = os.getenv('REDIS_URL')

# Set up a Redis connection pool with a maximum number of connections
redis_pool = redis.ConnectionPool.from_url(redis_url, max_connections=20)  # Adjust max_connections as needed

celery_app = Celery(
    "collegescraper",
    broker=redis_url,  # Use Redis as the broker
    backend=redis_url,  # Use Redis as the results backend
)
celery_app.conf.update(
    broker_transport_options={
        'pool_class': 'redis.BlockingConnectionPool',
        'max_connections': 20,  # Ensure this matches the max_connections in the pool
        'timeout': 10,  # Timeout for acquiring a connection from the pool
    },
    result_expires=3600,  # Customize as needed
)

logger = logging.getLogger(__name__)

@celery_app.task
def start_crawl_job():
    
    # Change to the correct directory
    os.chdir(os.path.join(os.path.dirname(__file__), '../', 'collegescraper'))
    
    # Run the scrapy command
    subprocess.run(["scrapy", "crawl", "colleges"])
    return "Scrapy crawl completed"



@celery_app.task
def add(x, y):
    return x + y

if __name__ == "__main__":
    print('starting')
    result = add.delay(4, 6)
    print("Task ID:", result.id)
    print("Result:", result.get(timeout=10))