from app.db.connect import AsyncDBPool
from typing import Optional

async def get_social_user(
    provider: str,
    provider_id: str
):
    sql = """
    SELECT
        u.id           AS id,
        ui.email       AS email,
        ui.nickname    AS nickname
    FROM public.user_social AS us
    JOIN public.app_user   AS u  ON us.user_id = u.id
    LEFT JOIN public.user_info AS ui ON ui.user_id = u.id
    WHERE us.provider    = $1
      AND us.provider_id = $2
    """
    return await AsyncDBPool.fetch_one(sql, (provider, provider_id))

async def create_social_user(
    provider: str,
    provider_id: str,
    email: str | None,
    nickname: str | None,
):
    result = await AsyncDBPool.execute_returning(
        "INSERT INTO public.app_user (uuid) VALUES (uuid_generate_v4()) RETURNING id"
    )
    user_id = result["id"] if isinstance(result, dict) else result

    await AsyncDBPool.execute(
        """
        INSERT INTO public.user_info (user_id, email, nickname)
        VALUES ($1, $2, $3)
        """,
        (user_id, email, nickname),
    )

    await AsyncDBPool.execute(
        """
        INSERT INTO public.user_social (user_id, provider, provider_id)
        VALUES ($1, $2, $3)
        """,
        (user_id, provider, provider_id),
    )

    return user_id