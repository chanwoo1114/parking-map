from app.db.connect import AsyncDBPool
import json

'''
Insert: 주차장 정보
'''
async def insert_parking_lot_base(
    data: dict
):
    sql = """
            INSERT INTO public.parking_lot_base (external_id, name, lot_type, address, geom, description)
            SELECT $1, $2, $3, $4, ST_SetSRID(ST_MakePoint($5, $6), 4326), $7 
            WHERE NOT EXISTS (
            SELECT 1 FROM public.parking_lot_base
            WHERE external_id = $1::VARCHAR AND name = $2::VARCHAR
            )
            RETURNING id;
            """
    return await AsyncDBPool.execute_returning(sql, (
        data.get("external_id"),
        data["name"],
        data["lot_type"],
        data.get("address"),
        data["x"],
        data["y"],
        data["description"]
    ))

'''
Insert: 거주자 우선구역
'''
async def insert_resident_parking_lot(
    val: tuple
):
    sql = """
        INSERT INTO public.resident_parking_lot 
            (id, owner_id, total_spaces, operating_hours, price_policy)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id;
    """
    return await AsyncDBPool.execute_returning(sql, val)

'''
Update: 거주자 우선구역
'''
async def update_resident_parking_lot(
    parking_lot_id: int,
    user_id: int,
    updates: dict
):
    set_clauses = []
    values = []

    for i, (key, value) in enumerate(updates.items(), start=1):
        set_clauses.append(f"{key} = ${i}")
        values.append(json.dumps(value) if isinstance(value, dict) else value)

    sql = f"""
        UPDATE public.resident_parking_lot
        SET {', '.join(set_clauses)}
        WHERE id = ${len(values)+1} AND owner_id = ${len(values)+2} AND is_active = TRUE
        RETURNING id;
    """

    values.append(parking_lot_id)
    values.append(user_id)

    return await AsyncDBPool.execute_returning(sql, tuple(values))

'''
Delete: 거주자 우선구역
'''
async def delete_resident_parking_lot(
    parking_lot_id: int,
    user_id: int
):
    sql = """
        UPDATE public.resident_parking_lot
        SET is_active = FALSE
        WHERE id = $1 AND owner_id = $2 AND is_active = TRUE
        RETURNING id;
    """
    return await AsyncDBPool.execute_returning(sql, (parking_lot_id, user_id))

async def fetch_public_parking_lots(
    lng: float,
    lat: float,
    radius: int
):
    sql = """
    SELECT
      b.id,
      b.lot_type,
      ST_AsGeoJSON(b.geom)::jsonb      AS geom,
      CASE
        WHEN (p.price_policy->>'base_charge_won')::int = 0
          THEN '무료'
        ELSE (p.price_policy->>'base_charge_won')
      END                              AS base_charge
    FROM public.parking_lot_base   b
    JOIN public.public_private_parking_lot p
      ON p.id = b.id
    WHERE
      b.lot_type    = 'public'
      AND NOT b.is_deleted
      AND (p.price_policy->>'base_charge_won') IS NOT NULL
      AND ST_DWithin(
            b.geom::geography,
            ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
            $3
      );
    """
    rows = await AsyncDBPool.fetch_all(sql, (lng, lat, radius))
    return rows

async def fetch_resident_parking_lots(
    lng: float,
    lat: float,
    radius: int
):
    """거주자 주차장 전용 조회"""
    sql = """
    SELECT
        b.id,
        b.lot_type,
        ST_AsGeoJSON(b.geom)::jsonb AS geom,
        CASE
            WHEN (r.price_policy->>'base_charge_won')::int = 0 THEN '무료'
            ELSE (r.price_policy->>'base_charge_won')
        END AS base_charge,
        r.owner_id,
        EXISTS(
            SELECT 1 FROM monthly_availability_calendar mac
            JOIN parking_slot ps ON ps.id = mac.parking_slot_id
            WHERE ps.parking_lot_id = b.id
              AND mac.target_date = CURRENT_DATE
              AND mac.is_available = TRUE
              AND mac.availability_status = 'OPEN'
        ) AS is_available,
        ST_Distance(b.geom::geometry, ST_SetSRID(ST_MakePoint($1, $2), 4326)) AS distance
    FROM parking_lot_base b
    JOIN resident_parking_lot r ON r.id = b.id
    WHERE
        b.lot_type = 'resident'
        AND NOT b.is_deleted
        AND r.is_active = TRUE
        AND ST_DWithin(b.geom::geography, ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography, $3)
    ORDER BY distance;
    """
    return await AsyncDBPool.fetch_all(sql, (lng, lat, radius))