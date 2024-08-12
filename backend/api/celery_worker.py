from celery import Celery
import logging
import subprocess
import os
import redis
from scrapy.crawler import CrawlerProcess
from .crud import reset_colleges_table
from .database import AsyncSessionLocal
from collegescraper.collegescraper.spiders.colleges import CollegesSpider

# Check the environment
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
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
else:
    celery_app = Celery(
        "collegescraper",
        broker="redis://localhost:6379/0",  # Use Redis as the broker
        backend="redis://localhost:6379/0",  # Use Redis as the results backend
    )

logger = logging.getLogger(__name__)

@celery_app.task
def start_crawl_job():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the correct directory
    os.chdir(os.path.abspath(os.path.join(current_directory, os.pardir, 'collegescraper')))

    scrapy_executable = os.path.join(current_directory, '..', 'crawler', 'Scripts', 'scrapy.exe')

    
    # Run the scrapy command
    subprocess.run([scrapy_executable, "crawl", "colleges"])
    return "Scrapy crawl completed"
