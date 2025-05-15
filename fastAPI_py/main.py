from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
            #noaa_data_cache = noaa_data  # Store in global cache
            print("NOAA data pulled.")
            return noaa_data
        except httpx.HTTPError as e:
            print(f"Failed to fetch NOAA data: {e}")

## Uncomment the lifespan function and add lifespan param to "FastAPI()" to enable periodic data fetching ##

'''
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
    refresh_task.cancel()  # Stop the task on shutdown'''

app = FastAPI() # "lifespan=lifespan" add for periodic tasks 


def render_link(value, data_label):
    return f"<a href='{value}'>{data_label}</a>"

def render_img(value, src):
    return f"<a href='{value}'><img src='{src}'></a>"

def render_button(value, data_label):
    return f"<button>{data_label}</button>"

def truncate_string(value, length=20):
    if len(value) > length:
        return value[:length] + "..."
    return value

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/griddap", response_class=HTMLResponse)
async def griddap_page(request: Request):
    table_data = await fetch_noaa_data()
    columns = table_data['table']['columnNames']
    print(columns)
    rows = table_data['table']['rows']
    column_render_map = {
        "griddap": {
            "label": "Griddap", 
            "class": "content",
            "render": render_link,
            "render_param": "data",
            },
        "Subset": {
            "label": "Subset", 
            "class": ""
            },
        "tabledap": {
            "label": "Table DAP Data", 
            "class": ""
            },
        "Make A Graph": {
            "label": "Make A Graph", 
            "class": "",
            "render": render_link,
            "render_param": "graph"
            },
        "wms": {
            "label": "WMS", 
            "class": ""
            },
        "files": {
            "label": "Source Data Files", 
            "class": ""
            },
        "Title": {
            "label": "Title", 
            "class": "content"
            },
        "Summary": {
            "label": "Summary", 
            "class": "",
            "render": render_button,
            "render_param": "Summary"
            },
        "Info": {
            "label": "Meta Data", 
            "class": "",
            "render": render_link,
            "render_param": "M"
            },
        "Background Info": {
            "label": "Background Info", 
            "class": "",
            "render": render_link,
            "render_param": "background"
            },
        "RSS": {
            "label": "RSS", 
            "class": "",
            "render": render_img,
            "render_param": "/static/images/rss.gif"
            },
        "Institution": {
            "label": "Institution", 
            "class": "",
            "render": truncate_string,
            "render_param": 15
            },
        "Dataset ID": {
            "label": "Dataset ID", 
            "class": "content"
            },

    }
    return templates.TemplateResponse("griddap/index.html", {
        "request": request,
        "columns": columns,
        "rows": rows,
        "column_render_map": column_render_map,
        "zip":zip})