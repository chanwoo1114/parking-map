from typing import Optional
from dataclasses import dataclass
from app.db.connect import AsyncDBPool


async def get_social_user(provider: str, provider_id: str):
    """
    provider, provider_id 로 연동된 사용자 정보 조회
    """
    row = await AsyncDBPool.fetch_one(
        """
        SELECT u.id, ui.email, ui.nickname
        FROM user_social us
        JOIN app_user u ON us.user_id = u.id
        JOIN user_info ui ON ui.user_id = u.id
        WHERE us.provider = $1 AND us.provider_id = $2
        """,
        (provider, provider_id),
    )
    if not row:
        return None
    return SocialUser(id=row["id"], email=row["email"], nickname=row["nickname"])