import re
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


def extract_mentions(text: str) -> List[str]:
    """Extract @username mentions from text."""
    pattern = r'@(\w+)'
    return re.findall(pattern, text)


async def resolve_mentions(db: AsyncSession, usernames: List[str]) -> List[User]:
    """Resolve usernames to User objects."""
    if not usernames:
        return []
    result = await db.execute(
        select(User).where(User.username.in_(usernames))
    )
    return list(result.scalars().all())


def format_text_with_mentions(text: str) -> str:
    """Convert @mentions to clickable links (for frontend processing)."""
    return text
