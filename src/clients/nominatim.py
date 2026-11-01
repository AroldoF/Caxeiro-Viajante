import asyncio
import httpx


URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
}


async def get_city(client: httpx.AsyncClient, city: str) -> tuple[float, float]:
    params = {
        "city": city,
        "country": "Brazil",
        "format": "jsonv2",
        "limit": 1,
    }

    response = await client.get(URL, params=params)
    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(f"Cidade não encontrada: {city}")

    place = results[0]

    return float(place["lat"]), float(place["lon"])


async def get_cords() -> list[tuple[float, float]]:
    cities = ["Fortaleza", "São Paulo", "Brasília", "Luís Gomes"]

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=10.0,
    ) as client:
        return await asyncio.gather(*(get_city(client, city) for city in cities))

if __name__ == "__main__":
    asyncio.run(get_cords())