from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from database import get_db
from models import User, Scan
from schemas import StatsOut

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", response_model=StatsOut)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Public endpoint: live platform-wide statistics."""
    user_count_result = await db.execute(select(func.count()).select_from(User))
    total_users = user_count_result.scalar() or 0

    scan_count_result = await db.execute(select(func.count()).select_from(Scan))
    total_scans = scan_count_result.scalar() or 0

    return StatsOut(
        total_users=total_users,
        total_scans=total_scans,
        accuracy_rate=94.2,  # Pre-calculated from model validation set
    )
