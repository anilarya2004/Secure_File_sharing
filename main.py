from fastapi import FastAPI
from auth.routes import router as auth_router
from files.routes import router as files_router

app = FastAPI(title="Secure File Sharing System")

app.include_router(auth_router, prefix="/auth")
app.include_router(files_router)
