from app.db.connect import AsyncDBPool
from typing import Optional
from app.core.security import hash_password
from app.schemas.auth import RegisterRequest


async def create_email_user(
        payload: RegisterRequest
) -> int:
    try:
        user_id = await AsyncDBPool.execute_returning(
            "INSERT INTO public.app_user (uuid) VALUES (uuid_generate_v4()) RETURNING id"
        )

        hashed_pw = hash_password(payload.password1)
        await AsyncDBPool.execute(
            """
            INSERT INTO public.user_info (user_id, email, password_hash, nickname, age, gender)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            (user_id, payload.email, hashed_pw, payload.nickname, payload.age, payload.gender)
        )

        return user_id

    except Exception as e:
        print(f"사용자 생성 오류: {e}")
        raise e

async def is_email_taken(email: str):
    """
    이메일 중복 확인
    """
    sql = """
        SELECT 
            1 
        FROM 
            public.user_info 
        WHERE 
            email = $1
    """
    result = await AsyncDBPool.fetch_one(sql, (email,))
    return result

async def get_user_email_query(email: str):
    """
    로그인 시 유저 정보 조회
    """
    sql = """
        SELECT 
            user_id, 
            password_hash,
            is_active
        FROM public.user_info 
        WHERE email = $1
    """
    result = await AsyncDBPool.fetch_one(sql, (email,))
    return result

async def get_user_info_by_id(user_id: int):
    '''
    내 정보 조회
    '''
    sql = """
        SELECT 
            email, 
            nickname, 
            age, 
            gender
        FROM
            public.user_info
        WHERE user_id = $1
    """
    result = await AsyncDBPool.fetch_one(sql, (user_id,))
    return result

async def update_user_info_by_id(user_id: int, nickname: Optional[str], age: Optional[int], gender: Optional[str]):
    '''
    내 정보 수정
    '''
    updates = []
    values = []

    if nickname is not None:
        updates.append("nickname = $%d" % (len(values) + 1))
        values.append(nickname)
    if age is not None:
        updates.append("age = $%d" % (len(values) + 1))
        values.append(age)
    if gender is not None:
        updates.append("gender = $%d" % (len(values) + 1))
        values.append(gender)

    if not updates:
        return False

    query = f"""
        UPDATE user_info
        SET {', '.join(updates)}
        WHERE user_id = ${len(values) + 1}
    """
    values.append(user_id)

    await AsyncDBPool.execute(query, *values)

    return True

async def get_password_hash_by_user_id(user_id: int):
    '''
    현재 hash 비멀번호 조회
    '''
    query = """
            SELECT 
                password_hash 
            FROM 
                public.user_info
            WHERE
                user_id = $1
    """
    row = await AsyncDBPool.fetch_one(query, (user_id,))

    return row["password_hash"] if row else None

async def update_password_hash_by_user_id(user_id: int, password_hash: str):
    '''
    비밀번호 변경
    '''
    query = """
        UPDATE
            public.user_info
        SET
            password_hash = $1 
        WHERE 
            user_id = $2
    """
    await AsyncDBPool.execute(query, (password_hash, user_id,))

async def is_nickname_taken(nickname: str):
    """
    닉네임 중복 확인
    """
    sql = """
        SELECT 
            1 
        FROM 
            public.user_info 
        WHERE 
            nickname = $1
    """
    result = await AsyncDBPool.fetch_one(sql, (nickname,))
    return result

async def deactivate_user_by_id(user_id: int):
    query = """
        UPDATE
            public.user_info
        SET 
            is_active = FALSE
        WHERE
            user_id = $1
    """
    await AsyncDBPool.execute(query, (user_id,))