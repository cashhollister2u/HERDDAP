from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware

noaa_data_cache = None  # Global in-memory cache

async def fetch_noaa_data():
    """Fetch NOAA data from the URL and store it in memory."""
    # params
    page=1
    itemsPerPage=100
    url="https://www.ncei.noaa.gov/erddap/griddap/index.json"

    global noaa_data_cache
    url = f"{url}?page={page}&itemsPerPage={itemsPerPage}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            noaa_data_cache = response.json()
            print("NOAA data refreshed.")
        except httpx.HTTPError as e:
            print(f"Failed to fetch NOAA data: {e}")

async def refresh_data_periodically():
    """Background task to refresh NOAA data every 5 minutes."""
    while True:
        await fetch_noaa_data()
        await asyncio.sleep(600)  # 5 minutes = 300 seconds

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initial fetch
    await fetch_noaa_data()
    # Start background refresh task
    refresh_task = asyncio.create_task(refresh_data_periodically())
    yield
    refresh_task.cancel()  # Stop the task on shutdown

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-noaa-data")
async def get_noaa_data():
    if noaa_data_cache is None:
        return {"error": "Data not yet available"}
    return noaa_data_cache