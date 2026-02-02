"""
Subscriber CRUD service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from ..models import Subscriber
from ..schemas import SubscriberCreate, SubscriberUpdate


class SubscriberService:
    """Service for subscriber operations"""

    @staticmethod
    async def create(db: AsyncSession, subscriber_data: SubscriberCreate) -> Subscriber:
        """Create a new subscriber"""
        subscriber = Subscriber(**subscriber_data.model_dump())
        db.add(subscriber)
        await db.commit()
        await db.refresh(subscriber)
        return subscriber

    @staticmethod
    async def get(db: AsyncSession, subscriber_id: int) -> Optional[Subscriber]:
        """Get subscriber by ID"""
        result = await db.execute(
            select(Subscriber).where(Subscriber.id == subscriber_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[Subscriber]:
        """Get subscriber by email"""
        result = await db.execute(
            select(Subscriber).where(Subscriber.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> tuple[List[Subscriber], int]:
        """List subscribers with pagination"""
        query = select(Subscriber)

        # Filter active subscribers
        if active_only:
            query = query.where(Subscriber.active == True)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.order_by(Subscriber.subscribed_at.desc())
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        subscribers = result.scalars().all()

        return list(subscribers), total

    @staticmethod
    async def update(
        db: AsyncSession, subscriber_id: int, subscriber_data: SubscriberUpdate
    ) -> Optional[Subscriber]:
        """Update a subscriber"""
        subscriber = await SubscriberService.get(db, subscriber_id)
        if not subscriber:
            return None

        # Update fields
        update_data = subscriber_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(subscriber, field, value)

        await db.commit()
        await db.refresh(subscriber)
        return subscriber

    @staticmethod
    async def unsubscribe(db: AsyncSession, subscriber_id: int) -> Optional[Subscriber]:
        """Unsubscribe a subscriber (soft delete)"""
        subscriber = await SubscriberService.get(db, subscriber_id)
        if not subscriber:
            return None

        subscriber.active = False
        subscriber.unsubscribed_at = datetime.utcnow()

        await db.commit()
        await db.refresh(subscriber)
        return subscriber

    @staticmethod
    async def delete(db: AsyncSession, subscriber_id: int) -> bool:
        """Delete a subscriber (hard delete)"""
        subscriber = await SubscriberService.get(db, subscriber_id)
        if not subscriber:
            return False

        await db.delete(subscriber)
        await db.commit()
        return True

    @staticmethod
    async def bulk_create(
        db: AsyncSession, subscribers_data: List[SubscriberCreate]
    ) -> List[Subscriber]:
        """Bulk create subscribers"""
        subscribers = [Subscriber(**sub.model_dump()) for sub in subscribers_data]
        db.add_all(subscribers)
        await db.commit()

        # Refresh all subscribers
        for subscriber in subscribers:
            await db.refresh(subscriber)

        return subscribers
