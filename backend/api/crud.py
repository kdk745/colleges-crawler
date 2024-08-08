from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from .models import College

async def get_all_colleges(db: AsyncSession):
    result = await db.execute(select(College))
    return result.scalars().all()

async def reset_colleges_table(db: AsyncSession):
    await db.execute(text('DROP TABLE IF EXISTS colleges'))
    await db.execute(text('''
        CREATE TABLE colleges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT NOT NULL,
            school_city TEXT,
            school_state TEXT,
            college_board_code TEXT
        )
    '''))
    await db.commit()
