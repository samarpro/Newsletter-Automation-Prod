"""
Migration script to import data from JSON files to database
"""
import json
import asyncio
from datetime import datetime
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal, init_db
from ..models import Article, Subscriber


async def migrate_articles(db: AsyncSession, json_path: str):
    """Migrate articles from JSON file"""
    print(f"Migrating articles from {json_path}...")

    if not Path(json_path).exists():
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        articles_data = json.load(f)

    migrated_count = 0
    skipped_count = 0

    for article_data in articles_data:
        try:
            # Check if article already exists
            existing = await db.execute(
                f"SELECT id FROM articles WHERE link = '{article_data['link']}'"
            )
            if existing.first():
                skipped_count += 1
                continue

            # Parse published date
            published = None
            if article_data.get("published") and article_data["published"] != "N/A":
                try:
                    published = datetime.fromisoformat(article_data["published"])
                except:
                    pass

            # Create article
            article = Article(
                title=article_data["title"],
                link=article_data["link"],
                categories=article_data.get("Category", []),
                published=published,
                summary=article_data.get("summary", ""),
                content=article_data.get("content", ""),
                ai_content=article_data.get("ai_content", ""),
                status="draft",
            )
            db.add(article)
            migrated_count += 1

        except Exception as e:
            print(f"Error migrating article '{article_data.get('title', 'Unknown')}': {e}")
            continue

    await db.commit()
    print(f"Migrated {migrated_count} articles, skipped {skipped_count} duplicates")


async def migrate_subscribers(db: AsyncSession, json_path: str):
    """Migrate subscribers from JSON file"""
    print(f"Migrating subscribers from {json_path}...")

    if not Path(json_path).exists():
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subscribers_data = data.get("subscribers", [])
    migrated_count = 0
    skipped_count = 0

    for sub_data in subscribers_data:
        try:
            # Check if subscriber already exists
            existing = await db.execute(
                f"SELECT id FROM subscribers WHERE email = '{sub_data['email']}'"
            )
            if existing.first():
                skipped_count += 1
                continue

            # Parse subscribed_at date
            subscribed_at = datetime.utcnow()
            if sub_data.get("subscribed_at"):
                try:
                    subscribed_at = datetime.fromisoformat(sub_data["subscribed_at"])
                except:
                    pass

            # Create subscriber
            subscriber = Subscriber(
                email=sub_data["email"],
                name=sub_data.get("name", ""),
                subscribed_at=subscribed_at,
                active=sub_data.get("active", True),
            )
            db.add(subscriber)
            migrated_count += 1

        except Exception as e:
            print(f"Error migrating subscriber '{sub_data.get('email', 'Unknown')}': {e}")
            continue

    await db.commit()
    print(f"Migrated {migrated_count} subscribers, skipped {skipped_count} duplicates")


async def run_migration():
    """Run the complete migration"""
    print("Starting migration...")

    # Initialize database
    await init_db()

    # Get database session
    async with AsyncSessionLocal() as db:
        # Migrate articles
        await migrate_articles(db, "../output/scraped_content.json")

        # Migrate subscribers
        await migrate_subscribers(db, "../output/subscribers.json")

    print("Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(run_migration())
