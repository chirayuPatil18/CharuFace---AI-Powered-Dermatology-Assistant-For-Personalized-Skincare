from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.routes.analyze import router as analyze_router
from backend.routes.chat import router as chat_router
from backend.routes.auth import router as auth_router

app = FastAPI(title="CharuFace AI")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(analyze_router)
app.include_router(chat_router)
app.include_router(auth_router)

def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
def login():
    return load_html("templates/login.html")


@app.get("/signup", response_class=HTMLResponse)
def signup():
    return load_html("templates/signup.html")


@app.get("/details", response_class=HTMLResponse)
def details():
    return load_html("templates/details.html")


@app.get("/capture", response_class=HTMLResponse)
def capture():
    return load_html("templates/capture.html")


@app.get("/result", response_class=HTMLResponse)
def result():
    return load_html("templates/result.html")


@app.get("/chat", response_class=HTMLResponse)
def chat():
    return load_html("templates/chat.html")