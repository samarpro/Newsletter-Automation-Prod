"""
Article CRUD service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List, Optional
from ..models import Article
from ..schemas import ArticleCreate, ArticleUpdate


class ArticleService:
    """Service for article operations"""

    @staticmethod
    async def create(db: AsyncSession, article_data: ArticleCreate) -> Article:
        """Create a new article"""
        article = Article(**article_data.model_dump())
        db.add(article)
        await db.commit()
        await db.refresh(article)
        return article

    @staticmethod
    async def get(db: AsyncSession, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        result = await db.execute(
            select(Article).where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_link(db: AsyncSession, link: str) -> Optional[Article]:
        """Get article by link"""
        result = await db.execute(
            select(Article).where(Article.link == link)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> tuple[List[Article], int]:
        """List articles with filters and pagination"""
        query = select(Article)

        # Apply filters
        if status:
            query = query.where(Article.status == status)

        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Article.title.ilike(search_pattern),
                    Article.summary.ilike(search_pattern),
                )
            )

        if category:
            query = query.where(Article.categories.contains([category]))

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.order_by(Article.scraped_at.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        articles = result.scalars().all()

        return list(articles), total

    @staticmethod
    async def update(
        db: AsyncSession, article_id: int, article_data: ArticleUpdate
    ) -> Optional[Article]:
        """Update an article"""
        article = await ArticleService.get(db, article_id)
        if not article:
            return None

        # Update fields
        update_data = article_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(article, field, value)

        await db.commit()
        await db.refresh(article)
        return article

    @staticmethod
    async def delete(db: AsyncSession, article_id: int) -> bool:
        """Delete an article"""
        article = await ArticleService.get(db, article_id)
        if not article:
            return False

        await db.delete(article)
        await db.commit()
        return True
