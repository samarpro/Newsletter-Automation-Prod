"""
Subscriber API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import math

from ...database import get_db
from ...services import SubscriberService
from ...schemas import (
    Subscriber,
    SubscriberCreate,
    SubscriberUpdate,
    SubscriberList,
    SubscriberImport,
)

router = APIRouter()


@router.post("/", response_model=Subscriber, status_code=201)
async def create_subscriber(
    subscriber_data: SubscriberCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new subscriber"""
    # Check if subscriber already exists
    existing = await SubscriberService.get_by_email(db, subscriber_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Subscriber with this email already exists")

    subscriber = await SubscriberService.create(db, subscriber_data)
    return subscriber


@router.get("/{subscriber_id}", response_model=Subscriber)
async def get_subscriber(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get subscriber by ID"""
    subscriber = await SubscriberService.get(db, subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber


@router.get("/", response_model=SubscriberList)
async def list_subscribers(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """List subscribers with pagination"""
    skip = (page - 1) * page_size

    subscribers, total = await SubscriberService.list(
        db,
        skip=skip,
        limit=page_size,
        active_only=active_only,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return SubscriberList(
        items=subscribers,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put("/{subscriber_id}", response_model=Subscriber)
async def update_subscriber(
    subscriber_id: int,
    subscriber_data: SubscriberUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a subscriber"""
    subscriber = await SubscriberService.update(db, subscriber_id, subscriber_data)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber


@router.post("/{subscriber_id}/unsubscribe", response_model=Subscriber)
async def unsubscribe_subscriber(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Unsubscribe a subscriber (soft delete)"""
    subscriber = await SubscriberService.unsubscribe(db, subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber


@router.delete("/{subscriber_id}", status_code=204)
async def delete_subscriber(
    subscriber_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete a subscriber (hard delete)"""
    success = await SubscriberService.delete(db, subscriber_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return None


@router.post("/import", response_model=list[Subscriber], status_code=201)
async def bulk_import_subscribers(
    import_data: SubscriberImport,
    db: AsyncSession = Depends(get_db),
):
    """Bulk import subscribers"""
    subscribers = await SubscriberService.bulk_create(db, import_data.subscribers)
    return subscribers
