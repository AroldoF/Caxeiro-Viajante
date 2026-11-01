import asyncio

import httpx

from .nominatim import get_cords


URL = "https://router.project-osrm.org"


async def main():
    coordinates = await get_cords()

    coordinate_string = ";".join(f"{lon},{lat}" for lon, lat in coordinates)

    params = {
        "sources": "0",
        "destinations": "1;2",
        "annotations": "duration,distance",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{URL}/table/v1/driving/{coordinate_string}",
            params=params,
        )
        response.raise_for_status()
        result = response.json()

    if result["code"] != "Ok":
        raise RuntimeError(f"Erro do OSRM: {result}")

    print("Durações (segundos):", result["durations"])
    print("Distâncias (metros):", result["distances"])


if __name__ == "__main__":
    asyncio.run(main())
