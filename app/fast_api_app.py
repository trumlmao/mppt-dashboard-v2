# app/fast_api_app.py

# TODO 1: Import the main tool.
from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles 
from .data_manager import DataManager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
# TODO 2: Create an application instance.
app = FastAPI()
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_folder = os.path.join(project_root, 'app/templates')
templates = Jinja2Templates(directory=template_folder)
state_file_path = os.path.join(project_root, 'latest_state.json')
data_manager = DataManager(state_file=state_file_path)
static_folder = os.path.join(project_root, 'app/static')
app.mount("/static", StaticFiles(directory=static_folder), name="static")
# TODO 3: Define a route for GET requests to "/".
# The function should return a Python dictionary.
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request): # Dùng async def theo quy ước
    # Bây giờ 'templates' là một đối tượng và có phương thức .TemplateResponse
    return templates.TemplateResponse("index.html", {"request": request})
@app.get('/api/latest-data')
async def get_latest_data():
    return data_manager.get_latest_data()

@app.get('/api/historical-data')
async def get_historical_data():
    return data_manager.query_historical_data(time_range='-5m')
# ... (các route khác)

# ---- Authentication Endpoints (Placeholders) ----
# Chúng ta sẽ tạo các phiên bản "giả" để template không bị lỗi
# Logic thực sự sẽ được thêm vào sau.

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Tạm thời chỉ trả về một thông báo đơn giản
    return templates.TemplateResponse("login.html", {"request": request, "form": "TODO", "title": "Sign In"})

@app.get("/logout")
async def logout():
    # Tạm thời chỉ trả về một message
    return {"message": "User logged out"}

@app.get("/register")
async def register_page():
    return {"message": "Register page placeholder"}

