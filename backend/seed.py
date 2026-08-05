import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import async_session, engine, Base
from app.models.user import User
from app.models.profile import CreatorProfile
from app.models.settings import UserSettings
from app.core.security import get_password_hash
from app.services.seed import seed_user_data


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == "harsh@creatoros.com"))
        existing = result.scalar_one_or_none()
        if existing:
            print("Demo user already exists, skipping seed.")
            return

        user = User(
            email="harsh@creatoros.com",
            hashed_password=get_password_hash("password123"),
            is_verified=True,
        )
        db.add(user)
        await db.flush()

        profile = CreatorProfile(
            user_id=user.id,
            name="Harsh",
            channel_name="TechWithHarsh",
            subscriber_count=284000,
            creator_type="YouTuber",
            niche="Web Development & AI",
        )
        db.add(profile)

        settings = UserSettings(user_id=user.id)
        db.add(settings)

        await db.flush()
        await seed_user_data(db, user.id)

        await db.commit()
        print(f"Demo user created: harsh@creatoros.com / password123 (id: {user.id})")


if __name__ == "__main__":
    asyncio.run(seed())
