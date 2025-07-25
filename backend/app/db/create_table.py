from backend.app.db.connect import AsyncDBPool
import asyncio


async def create_app_user_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.app_user (
            id SERIAL PRIMARY KEY,
            uuid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4()
        );
    """)


async def create_user_info_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_info (
            user_id INTEGER PRIMARY KEY REFERENCES app_user(id) ON DELETE CASCADE,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            nickname VARCHAR(50),
            age INTEGER,
            gender VARCHAR(10),
            is_active BOOLEAN DEFAULT TRUE,
            is_staff BOOLEAN DEFAULT FALSE,
            is_social BOOLEAN DEFAULT FALSE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)


async def create_user_social_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_social (
            user_id INTEGER PRIMARY KEY REFERENCES app_user(id) ON DELETE CASCADE,
            provider VARCHAR(50) NOT NULL,
            provider_id VARCHAR(255) NOT NULL,
            UNIQUE (provider, provider_id)
        );
    """)


async def create_parking_lot_base_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_lot_base (
            id SERIAL PRIMARY KEY,
            external_id VARCHAR(100),
            name VARCHAR(100) NOT NULL,
            lot_type VARCHAR(20) NOT NULL, -- 'resident', 'public', 'private'
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
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.resident_parking_lot (
            id INTEGER PRIMARY KEY REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            owner_id INTEGER REFERENCES app_user(id) ON DELETE SET NULL,
            total_spaces INTEGER CHECK (total_spaces > 0),
            operating_hours JSONB,
            price_policy JSONB,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)


async def create_public_private_parking_lot_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.public_private_parking_lot (
            id INTEGER PRIMARY KEY REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            total_spaces INTEGER CHECK (total_spaces > 0),
            available_spaces INTEGER CHECK (available_spaces >= 0),
            operating_hours JSONB,
            price_policy JSONB,
            managing_agency TEXT,
            contact TEXT,
            is_realtime_available BOOLEAN DEFAULT FALSE
        );
    """)


async def create_parking_lot_user_assignment_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_lot_user_assignment (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER NOT NULL REFERENCES resident_parking_lot(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            UNIQUE (parking_lot_id, user_id, start_time, end_time),
            CHECK (start_time < end_time)
        );
    """)


async def create_parking_lot_image_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_lot_image (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            image_url TEXT NOT NULL,
            is_cover BOOLEAN DEFAULT FALSE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ
        );
    """)


async def create_parking_slot_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_slot (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            slot_number VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            UNIQUE (parking_lot_id, slot_number)
        );
    """)


async def create_parking_availability_history_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.parking_availability_history (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            available_spaces INTEGER NOT NULL,
            recorded_at TIMESTAMPTZ DEFAULT now()
        );
    """)
    await AsyncDBPool.execute("""
        CREATE INDEX IF NOT EXISTS idx_avail_lot_time
        ON public.parking_availability_history (parking_lot_id, recorded_at DESC);
    """)


async def create_parking_reservation_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.reservation (
            id SERIAL PRIMARY KEY,
            parking_slot_id INTEGER REFERENCES parking_slot(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES app_user(id) ON DELETE CASCADE,
            start_time TIMESTAMPTZ NOT NULL,
            end_time TIMESTAMPTZ NOT NULL,
            total_price NUMERIC(10, 2),
            status VARCHAR(20) DEFAULT 'PENDING',
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            CHECK (end_time > start_time)
        );
    """)
    await AsyncDBPool.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_reservation_unique_slot
        ON reservation (parking_slot_id, start_time, end_time)
        WHERE status IN ('PENDING', 'CONFIRMED');
    """)


async def create_parking_review_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.review (
            id SERIAL PRIMARY KEY,
            parking_lot_id INTEGER REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES app_user(id) ON DELETE CASCADE,
            rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            UNIQUE (parking_lot_id, user_id)
        );
    """)


async def create_user_favorite_table():
    await AsyncDBPool.execute("""
        CREATE TABLE IF NOT EXISTS public.user_favorite (
            user_id INTEGER REFERENCES app_user(id) ON DELETE CASCADE,
            parking_lot_id INTEGER REFERENCES parking_lot_base(id) ON DELETE CASCADE,
            is_deleted BOOLEAN DEFAULT FALSE,
            deleted_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT now(),
            PRIMARY KEY (user_id, parking_lot_id)
        );
    """)


async def create_all_tables():
    await create_app_user_table()
    await create_user_info_table()
    await create_user_social_table()
    await create_parking_lot_base_table()
    await create_resident_parking_lot_table()
    await create_public_private_parking_lot_table()
    await create_parking_lot_user_assignment_table()
    await create_parking_lot_image_table()
    await create_parking_slot_table()
    await create_parking_availability_history_table()
    await create_parking_reservation_table()
    await create_parking_review_table()
    await create_user_favorite_table()


if __name__ == "__main__":
    async def run():
        await AsyncDBPool.init_pool()
        await create_all_tables()
        await AsyncDBPool.close_pool()

    asyncio.run(run())
