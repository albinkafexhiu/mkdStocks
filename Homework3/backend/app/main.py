from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, stocks, technical, fundamental  
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(technical.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(fundamental.router, prefix="/api/fundamental", tags=["fundamental"])  

@app.get("/")
async def root():
    return {"message": "MSE API is running"}