from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(
    title="Macro Tracking App",
    description="A simple FastAPI app",
    version="1.0.0"
)

# Simple endpoint
@app.get("/")
async def root():
    """Root endpoint - just to test if FastAPI is working."""
    return {
        "message": "Hello! FastAPI is working!",
        "status": "success"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check - tells us if the server is running."""
    return {
        "status": "healthy", 
        "message": "Server is running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 