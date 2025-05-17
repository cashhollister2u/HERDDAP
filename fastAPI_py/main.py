import httpx
import asyncio
from fastapi import FastAPI
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Custom imports 
from utilities.column_map import column_render_map

### Global in-memory cache ** Remove if caching not needed ###
griddap_data_cache = None  
tabledap_data_cache = None
##############################################################

async def fetch_noaa_data(url, page=1, items_per_page=100):
    """Fetch NOAA data from the URL and store it in memory or return cached data."""
    
    url = f"{url}?page={page}&itemsPerPage={items_per_page}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            noaa_data = response.json()
            print(f"NOAA data pulle: {url}.")
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
    await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/griddap/index.json")
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
    global griddap_data_cache
    if not griddap_data_cache:
        table_data = await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/griddap/index.json")
        griddap_data_cache = table_data  # Store in global cache
    else:
        table_data = griddap_data_cache
    columns = table_data['table']['columnNames']
    rows = table_data['table']['rows']
    return templates.TemplateResponse("griddap/index.html", {
        "request": request,
        "columns": columns,
        "rows": rows,
        "column_render_map": column_render_map,
        "zip":zip})

@app.get("/tabledap", response_class=HTMLResponse)
async def tabledap_page(request: Request):
    global tabledap_data_cache
    if not tabledap_data_cache:
        table_data = await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/tabledap/index.json")
        tabledap_data_cache = table_data  # Store in global cache
    else:
        table_data = tabledap_data_cache
    columns = table_data['table']['columnNames']
    rows = table_data['table']['rows']
    return templates.TemplateResponse("tabledap/index.html", {
        "request": request,
        "columns": columns,
        "rows": rows,
        "column_render_map": column_render_map,
        "zip":zip})