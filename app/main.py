from fastapi import FastAPI
from app.routers import health, auth, profiles, macro_goals, food_logs

# Create FastAPI app
app = FastAPI(
    title="Macro Tracking App",
    description="A FastAPI app with organized routers",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(macro_goals.router)
app.include_router(food_logs.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 