from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from .celery_worker import start_crawl_job
from .crud import get_all_colleges, reset_colleges_table
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .schemas import College as CollegeSchema
from typing import List


app = FastAPI()

@app.on_event("startup")
async def startup():
    from .database import create_tables
    await create_tables()

@app.post("/api/start-crawl", response_model=List[CollegeSchema])
async def start_crawl(db: AsyncSession = Depends(get_db)):
    # await reset_colleges_table(db)
    # Run the Scrapy job and wait for it to complete
    result = start_crawl_job.delay()
    try:
        response = result.get(timeout=300)
        print(f"Task Result: {response}")
    except TimeoutError:
        print("Task did not complete within the timeout period.")
    
    # Fetch the results from the database
    colleges = await get_all_colleges(db)
    return colleges

@app.get("/api/get-results", response_model=List[CollegeSchema])
async def get_results(db: AsyncSession = Depends(get_db)):
    # Fetch the results from the database
    colleges = await get_all_colleges(db)
    return colleges
