import httpx
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager


async def fetch_noaa_data(url, page=1, items_per_page=1000):
    """Fetch NOAA data from the URL and store it in memory or return cached data."""
    
    url = f"{url}?page={page}&itemsPerPage={items_per_page}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            noaa_data = response.json()
            print(f"NOAA data pulled: {url}.")
            return noaa_data
        except httpx.HTTPError as e:
            print(f"Failed to fetch NOAA data: {e}")

async def refresh_data_periodically():
    """Background task to refresh NOAA data every 5 minutes."""
    global griddap_data_cache, tabledap_data_cache, info_data_cache
    while True:
        griddap_data_cache = await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/griddap/index.json")
        info_data_cache = await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/info/index.json")
        info_data_cache = await asyncio.sleep(600)  # 5 minutes = 300 seconds

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background refresh task
    refresh_task = asyncio.create_task(refresh_data_periodically())
    yield
    refresh_task.cancel()  # Stop the task on shutdown