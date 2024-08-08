import subprocess
import os
from .crud import reset_colleges_table
from .database import AsyncSessionLocal

async def start_crawl_job():
    # Create a new session
    async with AsyncSessionLocal() as db:
        # Reset the colleges table using SQLAlchemy
        await reset_colleges_table(db)
    
    # Change to the correct directory
    os.chdir(os.path.join(os.path.dirname(__file__), '../', 'collegescraper'))
    
    # Run the scrapy command
    subprocess.run(["scrapy", "crawl", "colleges"])
