from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, auth, profiles, macro_goals, food_logs, emails

# Create FastAPI app
app = FastAPI(
    title="Macro Tracking App",
    description="A FastAPI app with organized routers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(macro_goals.router)
app.include_router(food_logs.router)
app.include_router(emails.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 