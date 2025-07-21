# Macro Tracking App - Backend

A FastAPI-based backend for a macro tracking application.

## Current Status

This is the initial setup with a basic FastAPI application.

## Features

- Basic FastAPI server setup
- Root endpoint (`/`) - Returns hello message
- Health check endpoint (`/health`) - Server status

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python -m app.main
   ```

3. Visit the API:
   - Root: http://localhost:8000/
   - Health: http://localhost:8000/health
   - Docs: http://localhost:8000/docs

## Project Structure

```
macro-tracking-app/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Next Steps

- Add database connection (Supabase)
- Add user authentication
- Add macro tracking endpoints
- Add food logging functionality 