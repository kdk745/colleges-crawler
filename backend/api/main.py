from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from .scraper import start_crawl_job
from .crud import get_all_colleges
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
    # Run the Scrapy job and wait for it to complete
    await start_crawl_job()
    
    # Fetch the results from the database
    colleges = await get_all_colleges(db)
    return colleges

@app.get("/api/get-results", response_model=List[CollegeSchema])
async def get_results(db: AsyncSession = Depends(get_db)):
    # Fetch the results from the database
    colleges = await get_all_colleges(db)
    return colleges
