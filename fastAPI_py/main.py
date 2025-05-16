import httpx
import asyncio
from fastapi import FastAPI
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Custom imports 
from templates.griddap.column_map import column_render_map

noaa_data_cache = None  # Global in-memory cache ** Remove if caching not needed

async def fetch_noaa_data():
    """Fetch NOAA data from the URL and store it in memory or return cached data."""
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
            noaa_data = response.json()
            noaa_data_cache = noaa_data  # Store in global cache
            print("NOAA data pulled.")
            return noaa_data
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

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(lifespan=lifespan) # "lifespan=lifespan" add for periodic tasks 

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/griddap", response_class=HTMLResponse)
async def griddap_page(request: Request):
    if not noaa_data_cache:
        table_data = await fetch_noaa_data()
    else:
        table_data = noaa_data_cache
    columns = table_data['table']['columnNames']
    rows = table_data['table']['rows']
    return templates.TemplateResponse("griddap/index.html", {
        "request": request,
        "columns": columns,
        "rows": rows,
        "column_render_map": column_render_map,
        "zip":zip})