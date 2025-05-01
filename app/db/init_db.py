import asyncio
from app.db.database import engine, Base
from app.models.user import User
from app.models.skill import Skill

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("tables created successfully")

if __name__ == "__main__":
    asyncio.run(init_models())
