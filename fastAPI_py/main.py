from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Custom imports 
from utilities.column_map import column_render_map
from utilities.fetch_data import fetch_noaa_data, lifespan

### Global in-memory cache ** Remove if caching not needed ###
griddap_data_cache = None  
tabledap_data_cache = None
info_data_cache = None
##############################################################

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(lifespan=lifespan) # "lifespan=lifespan" add for periodic tasks 

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    total_dataset_count = len(info_data_cache['table']['rows'])
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_dataset_count": total_dataset_count})

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
        "row_count": len(rows),
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
        "row_count": len(rows),
        "column_render_map": column_render_map,
        "zip":zip})

@app.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    global info_data_cache
    if not info_data_cache:
        table_data = await fetch_noaa_data(url="https://www.ncei.noaa.gov/erddap/info/index.json")
        info_data_cache = table_data
    else:
        table_data = info_data_cache
    columns = table_data['table']['columnNames']
    rows = table_data['table']['rows']
    return templates.TemplateResponse("info/index.html", {
        "request": request,
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "column_render_map": column_render_map,
        "zip":zip})

