from backend.app.db.connect import AsyncDBPool
import json

async def insert_parking_lot_base(data: dict):
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

async def insert_resident_parking_lot(val: tuple):
    sql = """
        INSERT INTO public.resident_parking_lot 
            (id, owner_id, total_spaces, operating_hours, price_policy)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id;
    """
    return await AsyncDBPool.execute_returning(sql, val)

async def update_resident_parking_lot(parking_lot_id: int, user_id: int, updates: dict):
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

async def delete_resident_parking_lot(parking_lot_id: int, user_id: int):
    sql = """
        UPDATE public.resident_parking_lot
        SET is_active = FALSE
        WHERE id = $1 AND owner_id = $2 AND is_active = TRUE
        RETURNING id;
    """
    return await AsyncDBPool.execute_returning(sql, (parking_lot_id, user_id))