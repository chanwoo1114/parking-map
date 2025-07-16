from backend.app.db.connect import AsyncDBPool

async def insert_parking_lot(data: dict):
    query = """
        INSERT INTO public.parking_lot (
            owner_id, name, lot_type, address,
            geom, total_spaces, available_spaces,
            operating_hours, price_policy, description, external_id
        ) VALUES (
            $1, $2, $3, $4,
            ST_SetSRID(ST_MakePoint($5, $6), 4326), $7, $8,
            $9, $10, $11, $12
        ) RETURNING id;
    """
    return await AsyncDBPool.execute_returning(query, (
        data.get("owner_id"),
        data["name"],
        data["lot_type"],
        data.get("address"),
        data["longitude"],
        data["latitude"],
        data["total_spaces"],
        data["available_spaces"],
        data.get("operating_hours"),
        data.get("price_policy"),
        data.get("description"),
        data.get("external_id")
    ))