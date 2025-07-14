from backend.app.db.connect import AsyncDBPool


async def insert_app_user_query():
    """
    사용자 UUID 생성
    """
    sql = """
        INSERT INTO public.app_user (
            uuid
        ) VALUES (uuid_generate_v4()) RETURNING id
    """
    result = await AsyncDBPool.execute_returning(sql)
    return result


async def insert_email_user_query(val: tuple):
    """
    이메일 사용자 생성
    """
    sql = """
        INSERT INTO public.user_info (
            user_id, email, password_hash, nickname, age, gender
        ) VALUES ($1, $2, $3, $4, $5, $6)
    """
    await AsyncDBPool.execute(sql, val)


async def select_user_email_query(val: str):
    """
    이메일 중복 확인
    """
    sql = """
        SELECT 1 
        FROM public.user_info 
        WHERE email = $1
    """
    result = await AsyncDBPool.fetch_one(sql, (val,))
    return result


async def get_user_email_query(val: str):
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
    result = await AsyncDBPool.fetch_one(sql, (val,))
    return result
