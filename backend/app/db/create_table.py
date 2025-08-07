import asyncio
from.app.db.connect import AsyncDBPool

async def create_app_user_table():
    """기본 사용자 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.app_user (
            id SERIAL PRIMARY KEY,
            uuid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4()
        );
    """)

async def create_user_info_table():
    """사용자 상세 정보 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_info (
            user_id INTEGER PRIMARY KEY REFERENCES public.app_user(id) ON DELETE CASCADE,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            nickname VARCHAR(50),
            age INTEGER,
            gender VARCHAR(10),
            is_active BOOLEAN DEFAULT TRUE,
            is_social BOOLEAN DEFAULT FALSE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)

async def create_user_social_table():
    """소셜 로그인 정보 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_social (
            user_id INTEGER PRIMARY KEY REFERENCES public.app_user(id) ON DELETE CASCADE,
            provider VARCHAR(50) NOT NULL,
            provider_id VARCHAR(255) NOT NULL,
            UNIQUE (provider, provider_id)
        );
    """)

async def create_parking_lot_base_table():
    """주차장 기본 정보 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_lot_base (
            id SERIAL PRIMARY KEY,
            external_id VARCHAR(100),
            name VARCHAR(100),
            lot_type VARCHAR(20) NOT NULL,
            address TEXT,
            geom GEOGRAPHY(POINT, 4326),
            description TEXT,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        );
    """)

async def create_resident_parking_lot_table():
    """거주자 전용 주차장 테이블 - 구역번호 추가"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.resident_parking_lot (
            id INTEGER PRIMARY KEY REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            owner_id INTEGER REFERENCES public.app_user(id) ON DELETE SET NULL,
            zone_number VARCHAR(50),
            total_spaces INTEGER CHECK (total_spaces > 0),
            operating_hours JSONB,
            price_policy JSONB,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)

async def create_resident_document_table():
    """거주자 서류 제출 및 유효기간 관리 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.resident_document (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES public.app_user(id) ON DELETE CASCADE,
            parking_lot_id INTEGER NOT NULL REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            document_image VARCHAR(255) NOT NULL,
            valid_from DATE NOT NULL,
            valid_until DATE NOT NULL,
            status VARCHAR(20) DEFAULT 'PENDING',
            approved_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            UNIQUE(user_id, parking_lot_id, status) DEFERRABLE INITIALLY DEFERRED,
            CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED'))
        );
    """)

async def create_public_private_parking_lot_table():
    """공공/민간 주차장 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.public_private_parking_lot (
            id INTEGER PRIMARY KEY REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            total_spaces INTEGER CHECK (total_spaces > 0),
            operating_hours JSONB,
            price_policy JSONB,
            is_realtime_available BOOLEAN DEFAULT FALSE
        );
    """)

async def create_parking_slot_table():
    """주차 슬롯 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_slot (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            slot_number VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            UNIQUE (parking_lot_id, slot_number)
        );
    """)

async def create_resident_weekly_pattern_table():
    """거주자 주간 기본 패턴 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.resident_weekly_pattern (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER NOT NULL REFERENCES public.parking_slot(id) ON DELETE CASCADE,
            owner_id INTEGER NOT NULL REFERENCES public.app_user(id) ON DELETE CASCADE,
            day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            pattern_name VARCHAR(50), -- '평일근무', '주말외출' 등 패턴명
            effective_from DATE DEFAULT CURRENT_DATE,
            effective_until DATE,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now(),
            CHECK (start_time < end_time),
            CHECK (EXTRACT(MINUTE FROM start_time)::int % 30 = 0),
            CHECK (EXTRACT(MINUTE FROM end_time)::int % 30 = 0)
        );
    """)

async def create_monthly_availability_calendar_table():
    """월간 가용성 캘린더 테이블 - 핵심 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.monthly_availability_calendar (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER NOT NULL REFERENCES public.parking_slot(id) ON DELETE CASCADE,
            owner_id INTEGER NOT NULL REFERENCES public.app_user(id) ON DELETE CASCADE,
            target_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            availability_status VARCHAR(20) DEFAULT 'OPEN',
            source_type VARCHAR(20) DEFAULT 'AUTO',
            modification_reason TEXT,
            price_override NUMERIC(10, 2), -- 특정 시간대 가격 조정
            last_modified_at TIMESTAMPTZ DEFAULT now(),
            created_at TIMESTAMPTZ DEFAULT now(),
            CHECK (start_time < end_time),
            CHECK (EXTRACT(MINUTE FROM start_time)::int % 30 = 0),
            CHECK (EXTRACT(MINUTE FROM end_time)::int % 30 = 0),
            CHECK (target_date >= CURRENT_DATE - INTERVAL '1 day'),
            UNIQUE (parking_slot_id, target_date, start_time, end_time)
        );
    """)

async def create_availability_modification_log_table():
    """사용자 수정 이력 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.availability_modification_log (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER NOT NULL REFERENCES public.parking_slot(id) ON DELETE CASCADE,
            owner_id INTEGER NOT NULL REFERENCES public.app_user(id) ON DELETE CASCADE,
            target_date DATE NOT NULL,
            start_time TIME,
            end_time TIME,
            old_status BOOLEAN,
            new_status BOOLEAN,
            modification_type VARCHAR(30),
            affected_slots_count INTEGER DEFAULT 1,
            reason TEXT,
            ip_address INET,
            user_agent TEXT,
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)

async def create_locked_time_slots_table():
    """예약 제약 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.locked_time_slots (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER NOT NULL REFERENCES public.parking_slot(id) ON DELETE CASCADE,
            target_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            reservation_id INTEGER REFERENCES public.reservation(id) ON DELETE CASCADE,
            lock_reason VARCHAR(50) DEFAULT 'RESERVED',
            locked_by_user_id INTEGER REFERENCES public.app_user(id),
            locked_at TIMESTAMPTZ DEFAULT now(),
            expires_at TIMESTAMPTZ, -- 임시 잠금의 경우 만료시간
            UNIQUE (parking_slot_id, target_date, start_time, end_time)
        );
    """)

async def create_reservation_table():
    """예약 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.reservation (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER NOT NULL REFERENCES public.parking_slot(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES public.app_user(id) ON DELETE CASCADE,
            start_time TIMESTAMPTZ NOT NULL,
            end_time TIMESTAMPTZ NOT NULL,
            total_price NUMERIC(10, 2),
            status VARCHAR(20) DEFAULT 'PENDING',
            payment_status VARCHAR(20) DEFAULT 'UNPAID',
            reservation_code VARCHAR(20) UNIQUE,
            special_requests TEXT,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now(),
            CHECK (start_time < end_time),
            CHECK (EXTRACT(MINUTE FROM start_time AT TIME ZONE 'Asia/Seoul')::int % 30 = 0),
            CHECK (EXTRACT(MINUTE FROM end_time AT TIME ZONE 'Asia/Seoul')::int % 30 = 0)
        );
    """)

async def create_parking_lot_image_table():
    """주차장 이미지 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_lot_image (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            image_url TEXT NOT NULL,
            image_type VARCHAR(20) DEFAULT 'GENERAL',
            is_cover BOOLEAN DEFAULT FALSE,
            display_order INTEGER DEFAULT 0,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)

async def create_review_table():
    """리뷰 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.review (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES public.app_user(id) ON DELETE CASCADE,
            reservation_id INTEGER REFERENCES public.reservation(id) ON DELETE SET NULL,
            rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            helpful_count INTEGER DEFAULT 0,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            UNIQUE (parking_lot_id, user_id)
        );
    """)

async def create_user_favorite_table():
    """사용자 즐겨찾기 테이블"""
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_favorite (
            user_id INTEGER REFERENCES public.app_user(id) ON DELETE CASCADE,
            parking_lot_id INTEGER REFERENCES public.parking_lot_base(id) ON DELETE CASCADE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            PRIMARY KEY (user_id, parking_lot_id)
        );
    """)



async def create_all_tables():
    """모든 테이블과 관련 요소들 생성 - 올바른 순서"""
    try:
        await create_app_user_table()
        await create_user_info_table()
        await create_user_social_table()
        await create_parking_lot_base_table()
        await create_resident_parking_lot_table()
        await create_resident_document_table()
        await create_public_private_parking_lot_table()
        await create_parking_slot_table()
        await create_resident_weekly_pattern_table()
        await create_monthly_availability_calendar_table()
        await create_availability_modification_log_table()
        await create_reservation_table()
        await create_locked_time_slots_table()
        await create_parking_lot_image_table()
        await create_review_table()
        await create_user_favorite_table()


    except Exception as e:
        print(e)
        raise

if __name__ == "__main__":
    async def run():
        await AsyncDBPool.init_pool()
        await create_all_tables()
        await AsyncDBPool.close_pool()

    asyncio.run(run())
