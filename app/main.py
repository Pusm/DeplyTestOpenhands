from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="/workspace/DeplyTestOpenhands/app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="/workspace/DeplyTestOpenhands/app/templates")

@app.get("/api/hello")
async def hello():
    return {"message": "Hello, World!"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})