from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from data import get_data

router = APIRouter()

# Load Jinja2 templates
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


@router.get("/", response_class=HTMLResponse)
async def redirecthome(request: Request):
    return RedirectResponse("/dynamic")




@router.get("/index", response_class=HTMLResponse)
async def read_data(request: Request):
    # Render the template with the data
    data = await get_data()
    template = env.get_template("index.html")
    return template.render(request=request, data=data)

@router.get("/dynamic", response_class=HTMLResponse)
async def dynamic_site(request: Request):
    # Render the template with the data
    template = env.get_template("dynamic.html")
    return template.render(request=request)